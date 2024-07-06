# -*- coding: utf-8 -*-

import re

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class RecurringSubscription(models.Model):
    _name = "recurring.subscription"
    _description = "Recurring Subscription"
    _inherit = 'mail.thread'

    order_id = fields.Char(string='Order Id')
    name = fields.Char(string="Name", required=True)
    establishment = fields.Char(string="Establishment Id")
    date = fields.Date(string="Date")
    due_date = fields.Date(string="Due Date",
                           default=fields.Date.add(fields.Date.today(),
                                                   days=15))
    next_billing = fields.Date(string="Next billing")
    is_lead = fields.Boolean(string="Is Lead")
    product_id = fields.Many2one('product.product', string="Product",
                                 required=True)
    partner_id = fields.Many2one('res.partner', string="Customer",
                                 required=True)
    recurring_amount = fields.Float(string="Recurring Amount", required=True)
    state = fields.Selection(
        string="State",
        selection=[('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'),
                   ('cancel', 'Cancel')], default='draft', tracking=True)
    description = fields.Text(string='Description')
    terms_and_condition = fields.Html(string="Terms&Conditions")
    reference_no = fields.Char(string="Reference number", readonly=True,
                               default='New')
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company,
                                 readonly=True)
    subscription_ids = fields.One2many('recurring.subscription.credit',
                                       'recurring_subscription_id', )
    billing_schedule_id = fields.Many2one('billing.schedule',
                                          string='Billing Schedule')
    total = fields.Float(string="Total", compute='_compute_total_credit',
                         store=True)
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  string='Currency', readonly=True)
    max_credit = fields.Float(string='Max Credit',
                              compute='_compute_max_credit', store=True)

    subscription_image = fields.Image(string='Image')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'recurring.subscription') or 'New'
        res = super(RecurringSubscription, self).create(vals_list)
        return res

    @api.constrains('establishment')
    def check_establishment(self):
        """validate the field establishment_id with 3 alphabets , 3 numbers
        and 2 hyphens"""
        for rec in self:
            if rec.establishment:
                if not re.match(r"^(?=.*[a-zA-Z].*[a-zA-Z].*[a-zA-Z])("
                                r"?=.*\d.*\d.*\d)(?=.*-.*-)[a-zA-Z\d-]*",
                                rec.establishment):
                    raise ValidationError(_(
                        "Establishment id must contain 3 alphabets ,3 numbers"
                        " and 2 hyphens"))

    def confirm_button(self):
        return self.write({'state': 'confirm'})

    def cancel_button(self):
        return self.write({'state': 'cancel'})

    def done_button(self):
        if self.partner_id.email:
            template = self.env.ref(
                'reccuring_subscription.recurring_email_template')
            template.send_mail(self.id, force_send=True)
        return self.write({'state': 'done'})

    @api.onchange('establishment')
    def _onchange_establishment_id(self):
        if self.establishment:
            partner = self.env['res.partner'].search(
                [('establishment', '=', self.establishment)])
            if partner:
                self.partner_id = partner
            else:
                raise ValidationError("No partner found")

    @api.depends('subscription_ids')
    def _compute_total_credit(self):
        self.total = sum(self.subscription_ids.filtered(
            lambda rec: rec.credit_amount > 0).mapped('credit_amount'))

    @api.depends('subscription_ids.credit_amount')
    def _compute_max_credit(self):
        if self.subscription_ids:

            self.max_credit = max(self.subscription_ids.filtered(
                lambda x: x.state == 'fully_approved').mapped('credit_amount'))
        else:
            self.max_credit = 0
        # print(self.subscription_ids)
        # print(self.subscription_ids.filtered(
        #     lambda x: x.state == 'fully_approved').mapped('credit_amount'))
        # print(self.subscription_ids.search([('state','=','fully_approved')]).mapped('credit_amount'))
