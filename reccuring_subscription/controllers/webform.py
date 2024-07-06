# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import Command
from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/recurring-subscription', auth='public', website=True)
    def web_form(self, **kwargs):
        if request.env.user.has_group(
                "reccuring_subscription.recurring_subscription_manager"):
            subscription_record = request.env[
                'recurring.subscription'].sudo().search([])
        else:
            subscription_record = request.env[
                'recurring.subscription'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id)])
        products = request.env['product.product'].sudo().search([])
        data = {
            'record': subscription_record,
            'product': products,
        }
        return request.render('reccuring_subscription.web_tree_template', data)

    @route('/webform/submit', type='http', auth='public', website=True)
    def web_form_submit(self, **post):
        request.env['recurring.subscription'].sudo().create({
            'name': post.get('subscription'),
            'date': post.get('date'),
            'product_id': post.get('product'),
            'partner_id': post.get('customer'),
            'recurring_amount': post.get('recurring amount')
        })
        return request.redirect('/recurring-subscription')

    @route('/credit', type='http', auth='public', website=True)
    def web_credit_form(self, **post):
        credit_record = request.env['recurring.subscription'].sudo().search([])
        data = {
            'subscription': credit_record,
        }
        return request.render('reccuring_subscription.credit_web_form_template',
                              data)

    @route('/credit_customer', type='json', auth='public', website=True)
    def submit_btn(self, **post):
        print(post)
        valid = request.env['recurring.subscription.credit'].sudo().create({
            'recurring_subscription_id': int(post.get('name')),
            'partner_id': int(post.get('customer')),
            'credit_amount': int(post.get('credit'))
        })
        valid.state = 'fully_approved'
        # return request.redirect('/recurring-subscription')

    @route('/recurring', auth='public', website=True)
    def create_btn(self):
        products = request.env['product.product'].sudo().search([])
        customer = request.env['res.partner'].sudo().search([])
        datas = {
            'products': products,
            'customer': customer,
        }
        return request.render('reccuring_subscription.web_form_template', datas)

    @route('/submit/customer', type='http', auth='public', csrf=False,
           website=True)
    def btn_create(self, **post):
        # print(post)
        request.env['res.partner'].create({
            'name': post.get('name'),
            'email': post.get('email')
        })
        return request.redirect('/recurring')

    @route('/edit', type='json', auth='public', website=True)
    def edit_btn(self):
        products = request.env['product.product'].sudo().search([])
        datas = {
            'products': products.ids,
            'product_name': products.mapped('name')
        }
        return datas

    @route('/billing_schedule', type='json', website=True, )
    def invoice_btn(self, **post):
        print(post.get('name'))
        subscription = (request.env[
            'recurring.subscription'].search(
            [('name', 'in', post.get('name'))]))
        print(subscription)
        for recs in subscription:
            time = str(datetime.now())
            request.env['billing.schedule'].sudo().create({
                'name': recs.name + " " + time,
                'recurring_subscription_ids': [Command.link(recs.id)]
            }).invoice_btn()

    @route('/edit/history', type='http', auth='public', website=True)
    def update_btn(self, **post):
        request.env['recurring.subscription'].sudo().browse(
            int(post.get('ID'))).write({
                'name': post.get('name'),
                'date': post.get('date'),
                'recurring_amount': post.get('recurring amount')
            })
        return request.redirect('/recurring-subscription')

    @route('/credit_cust', type='json', auth='public', website=True)
    def partner_credit(self, **post):
        pat = request.env['recurring.subscription'].sudo().browse(
            int(post.get('cust'))).partner_id.name
        pat_id = request.env['recurring.subscription'].sudo().browse(
            int(post.get('cust'))).partner_id.id
        n_cust = {'customer': pat, 'customer_id': pat_id}
        return n_cust
