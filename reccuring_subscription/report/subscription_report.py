# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import UserError


class SubscriptionReport(models.AbstractModel):
    _name = "report.reccuring_subscription.report_subscription"

    @api.model
    def _get_report_values(self, docids, data=None):
        print(data['period'])
        print("ertyu", data['subscription_ids'])
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
            query += f" AND rs.date <'{data['to_date']}'"

        self.env.cr.execute(query)
        values = self.env.cr.fetchall()
        data['records'] = values
        terms = [recs[-1][3:-4] if recs[-1] else False for recs in values]
        data['terms'] = terms
        print(data)
        print(values)
        if not values:
            raise UserError("No Records has been found")

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': self,
            'data': data
        }
