# -*- coding: utf-8 -*-

import io
import json
import xlsxwriter
from odoo import fields, models
from datetime import datetime
from odoo.exceptions import UserError
from odoo.fields import Date
from odoo.tools import date_utils


class RecurringSubscriptionCreditReport(models.TransientModel):
    _name = "recurring.subscription.credit.report"
    _description = "Recurring Subscription Credit Report"

    subscriptions_id = fields.Many2one('recurring.subscription',
                                       string="Subscription")
    state = fields.Selection(string="State",
                             selection=[('pending', 'Pending'),
                                        ('confirmed', 'Confirmed'),
                                        ('first approved', 'First Approved'),
                                        ('fully approved', 'Fully Approved'),
                                        ('rejected', 'Rejected')])

    def action_subscription_report(self):
        data = {
            'model': 'recurring.subscription',
            'subscriptions_id': self.subscriptions_id.id,
            'state': self.state,
            'print_date': datetime.today()
        }
        return self.env.ref(
            'reccuring_subscription.action_report_recurring_subscription_credit').report_action(
            None, data=data)

    def action_subscription_xsl_report(self):
        data = {
            'model': 'recurring.subscription',
            'subscriptions_id': self.subscriptions_id.id,
            'state': self.state,
            'print_date': datetime.today()
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'recurring.subscription.credit.report',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Subscription Credit Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = (f"select rs.name,rsc.state,rsc.credit_amount,rp.name,"
                 f"rsc.subscription_amount from recurring_subscription_credit"
                 f" as rsc INNER JOIN recurring_subscription as rs ON "
                 f"rsc.recurring_subscription_id=rs.id INNER JOIN "
                 f"res_partner as rp ON rsc.partner_id=rp.id WHERE 0=0")
        if data['subscriptions_id'] and data['state']:
            query += f" AND rs.id='{data['subscriptions_id']}'"
        elif data['subscriptions_id']:
            query += f" AND rs.id='{data['subscriptions_id']}' AND rsc.state='fully_approved' order by rsc.credit_amount desc limit 1"
        if data['state'] == 'pending':
            query += f" AND rsc.state='pending'"
        if data['state'] == 'confirmed':
            query += f" AND rsc.state='confirmed'"
        if data['state'] == 'first approved':
            query += f" AND rsc.state='first_approved'"
        if data['state'] == 'fully approved':
            query += f" AND rsc.state='fully_approved'"
        if data['state'] == 'rejected':
            query += f" AND rsc.state='rejected'"

        self.env.cr.execute(query)
        values = self.env.cr.fetchall()
        print(values)
        if not values:
            raise UserError("No Records has been found")
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.set_column('A8:G8', 25)
        sheet.merge_range('A1:H2',
                          f"{'SUBSCRIPTION CREDIT EXCEL REPORT:' if data['state'] else 'SUBSCRIPTION CREDIT EXCEL REPORT'} {data['state'].upper() if data['state'] else ''}",
                          head)
        sheet.write('A8:B8', 'SL.NO', cell_format)
        sheet.write('B8:C8', 'Subscription', cell_format)
        sheet.write('C8:D8', 'Amount Applied', cell_format)
        sheet.write('D8:E8', 'Pending Amount', cell_format)
        sheet.write('E8:F8', 'Customer', cell_format)
        if not data['state']:
            sheet.write('F8:G8', 'State', cell_format)
        sheet.merge_range('A3:H6', f"{self.env.company.name}\n "
                                   f"{self.env.company.street}\n"
                                   f"{self.env.company.city}\n"
                                   f"{self.env.company.country_id.name}", txt)
        sheet.write('A7:B7', f"{'Date:'}{(str(Date.today()))}", cell_format)
        row_index = 8
        for index, rec in enumerate(values):
            new_rec = list(rec)
            new_rec[4], new_rec[1] = new_rec[1], new_rec[4]
            new_rec[2] = new_rec[1] - new_rec[2]
            new_rec[4] = dict(self.env['recurring.subscription.credit']._fields[
                                  'state'].selection).get(new_rec[4])
            if data['state']:
                new_rec.pop()
            sheet.write(f"A{row_index + 1}:A{row_index + 1}", index + 1, txt)
            sheet.write_row(row_index, 1, new_rec, txt)
            row_index += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
