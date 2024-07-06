# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RecurringSubscriptionCredit(models.Model):
    _name = "recurring.subscription.credit"
    _description = "Recurring Subscription Credit"
    _rec_name = "recurring_subscription_id"
    _inherit = "mail.thread"

    recurring_subscription_id = fields.Many2one('recurring.subscription',
                                                string="Recurring Subscription")
    partner_id = fields.Many2one('res.partner',
                                 related="recurring_subscription_id.partner_id",
                                 string="Partner", readonly=False, store=True)
    subscription_amount = fields.Float(related="recurring_subscription_id"
                                               ".recurring_amount",
                                       string="Subscription Amount", store=True)
    credit_amount = fields.Float(string="Credit Amount")
    state = fields.Selection(
        string="State",
        selection=[('pending', 'Pending'), ('confirmed', 'Confirmed'),
                   ('first_approved', 'First approved'),
                   ('fully_approved', 'Fully approved'),
                   ('rejected', 'Rejected')], tracking=True, default='pending')
    period_date = fields.Date(string="Period Date")
    company_id = fields.Many2one('res.company',
                                 related="recurring_subscription_id.company_id",
                                 string="Company")
    establishment = fields.Char(
        related="recurring_subscription_id.establishment",
        string="Establishment Id")
    due_date = fields.Date(related="recurring_subscription_id.due_date",
                           string="Due date")
    subscription_image = fields.Image(related="recurring_subscription_id.subscription_image",string="Image")

    @api.onchange('credit_amount')
    def change_credit_amount(self):
        if self.credit_amount == 0 or self.credit_amount > self.subscription_amount:
            self.recurring_subscription_id = False
