# -*- coding: utf-8 -*-

from odoo.http import request, Controller, route


class SubscriptionCreditController(Controller):
    @route('/subscription_credits', type="http", auth="public", website=True)
    def subscription_credits(self):
        return request.render('reccuring_subscription.web_credits_template')

    @route(['/customer_credits'], type="json",
           auth="public", website=True)
    def total_credits(self):
        if request.env.user.has_group(
                "reccuring_subscription.recurring_subscription_manager"):
            customer_credit = request.env[
                'recurring.subscription.credit'].sudo().search_read([], [
                    'recurring_subscription_id', 'partner_id', 'credit_amount',
                    'subscription_image'])
        else:
            customer_credit = request.env[
                'recurring.subscription.credit'].sudo().search_read(
                [('partner_id', '=', request.env.user.partner_id.id)],
                ['recurring_subscription_id', 'partner_id',
                 'credit_amount', 'subscription_image'], order='create_date '
                                                               'DESC', limit=4)
        return customer_credit

    @route('/slides/<int:id>', type="http", auth="public", website=True)
    def subscription_details(self, id):
        subscription = request.env['recurring.subscription'].sudo().browse(id)
        data = {
            'record': subscription,
        }
        return request.render('reccuring_subscription.snippet_form_template',
                              data)
