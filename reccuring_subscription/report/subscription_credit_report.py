# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import UserError


class SubscriptionReport(models.AbstractModel):
    _name = "report.reccuring_subscription.report_subscription_credit"

    @api.model
    def _get_report_values(self, docids, data=None):
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
        data['records'] = values
        if not values:
            raise UserError("No Records has been found")

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': self,
            'data': data
        }
