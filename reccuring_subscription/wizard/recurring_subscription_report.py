# -*- coding: utf-8 -*-

import io
import json
import xlsxwriter
from odoo import fields, models
from odoo.exceptions import UserError
from datetime import datetime

from odoo.fields import Date
from odoo.tools import date_utils


class RecurringSubscriptionReport(models.TransientModel):
    _name = "recurring.subscription.report"
    _description = "Recurring Subscription Report"

    subscription_ids = fields.Many2many('recurring.subscription',
                                        string="Subscription")
    period = fields.Selection(string="Period",
                              selection=[('daily', 'Daily'),
                                         ('weekly', 'Weekly'),
                                         ('monthly', 'Monthly'),
                                         ('yearly', 'Yearly'),
                                         ('custom', 'Custom')])
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    def action_subscription_report(self):
        subscriptions = self.mapped('subscription_ids').ids
        terms = self.subscription_ids.mapped('terms_and_condition')
        data = {
            'model': 'recurring.subscription',
            'subscription_ids': subscriptions,
            'period': self.period,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'print_date': datetime.today()
        }
        if self.to_date and self.from_date and self.to_date < self.from_date:
            raise UserError("To date must be less from date")

        return self.env.ref(
            'reccuring_subscription.action_report_recurring_subscription').report_action(
            None, data=data)

    def action_subscription_xsl_report(self):
        subscriptions = self.mapped('subscription_ids').ids
        data = {
            'model': 'recurring.subscription',
            'subscription_ids': subscriptions,
            'period': self.period,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'print_date': datetime.today()
        }
        if self.to_date and self.from_date and self.to_date < self.from_date:
            raise UserError("To date must be less from date")
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'recurring.subscription.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Subscription Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = (f"SELECT rs.name,rs.recurring_amount,rs.total,rs.state,"
                 f"rp.name,pt.name,rs.date,rs.terms_and_condition FROM recurring_subscription as rs INNER JOIN "
                 f"res_partner as rp ON rs.partner_id=rp.id INNER JOIN product_product "
                 f"as pp ON rs.product_id=pp.id INNER JOIN product_template"
                 f" as pt ON pp.product_tmpl_id=pt.id WHERE 0=0")
        if len(data['subscription_ids']) > 1:
            query += f" AND rs.id in {tuple(data['subscription_ids'])}"
        elif data['subscription_ids']:
            query += f" AND rs.id = {tuple(data['subscription_ids'])[0]}"

        if data['period'] == 'daily':
            query += f" AND rs.date=current_date"
        if data['period'] == 'monthly':
            query += f" AND rs.date>=date_trunc('month',current_date)"
        if data['period'] == 'weekly':
            query += f" AND rs.date>=date_trunc('week',current_date)"
        if data['period'] == 'yearly':
            query += f" AND rs.date>=date_trunc('year',current_date)"
        if data['from_date'] and data['to_date']:
            query += f" AND rs.date >= '{data['from_date']}' AND rs.date <= '{data['to_date']}'"
        elif data['from_date']:
            query += f" AND rs.date > '{data['from_date']}'"
        elif data['to_date']:
            query += f" AND rs.date < '{data['to_date']}'"

        self.env.cr.execute(query)
        values = self.env.cr.fetchall()
        if not values:
            raise UserError("No Records has been found")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        term_format = workbook.add_format({'font_size': '12px'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.set_column('A8:H8', 25)
        sheet.merge_range('A1:H2',
                          f"{'SUBSCRIPTION EXCEL REPORT: ' if data['period'] else 'SUBSCRIPTION EXCEL REPORT'} {data['period'].upper() if data['period'] else ''}",
                          head)
        sheet.write('A8:B8', 'SL.NO', cell_format)
        sheet.write('B8:C8', 'Name', cell_format)
        sheet.write('C8:D8', 'Amount', cell_format)
        sheet.write('D8:E8', 'Total Credit Amount', cell_format)
        sheet.write('E8:F8', 'State', cell_format)
        sheet.write('F8:G8', 'Customer', cell_format)
        sheet.write('G8:H8', 'Product', cell_format)
        sheet.write('H8:I8', 'Date', cell_format)
        sheet.merge_range('A3:H6', f"{self.env.company.name}\n "
                                   f"{self.env.company.street}\n"
                                   f"{self.env.company.city}\n"
                                   f"{self.env.company.country_id.name}", txt)
        sheet.write('A7:B7', f"{'Date:'}{(str(Date.today()))}", cell_format)

        row_index = 8
        term = []
        for index, rec in enumerate(values):
            new_rec = list(rec)
            new_rec.insert(0, index + 1)
            new_rec[6] = new_rec[6]['en_US']
            new_rec[7] = str(new_rec[7])
            new_rec[4] = dict(self.env['recurring.subscription']._fields[
                                  'state'].selection).get(new_rec[4])
            terms_condition = new_rec.pop()
            print(terms_condition)
            sheet.write_row(row_index, 0, new_rec, txt)
            row_index += 1
            term.append(terms_condition)
        term_index = row_index + 2
        sheet.write(f"A{term_index}:B{term_index}", 'Terms and Condition :',
                    cell_format)
        term_index += 1
        for index, recs in enumerate(term):
            if recs:
                sheet.write(f"A{term_index}:B{term_index}", index + 1, txt)
                sheet.merge_range(f"B{term_index}:D{term_index}", recs[3:-4],
                                  term_format)
                term_index += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
