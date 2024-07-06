# -*- coding: utf-8 -*-

from odoo import api, models, fields, Command
from datetime import datetime


class BillingSchedule(models.Model):
    _name = "billing.schedule"
    _description = "Billing Schedule"

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique')
    ]

    name = fields.Char(string="Name", required=True)
    simulation = fields.Boolean(string="Simulation")
    period = fields.Date(string="Period")
    restrict_customer_ids = fields.Many2many('res.partner',
                                             string="Restrict Customer")
    active = fields.Boolean(string="Active", default=True)
    recurring_subscription_ids = fields.Many2many('recurring.subscription',
                                                  string="Recurring "
                                                         "Subscription")
    total_credit_amount = fields.Float(string="Total Credit Amount",
                                       compute='check_credit')
    due_date = fields.Date(related="recurring_subscription_ids.due_date",
                           string="Due date")
    subscription_count = fields.Integer(compute='compute_count')
    credits_ids = fields.Many2many('recurring.subscription.credit',
                                   string='Credits', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer',
                                 related="recurring_subscription_ids.partner_id")
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  string='Currency')

    def subscription(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'billing subscription',
            'view_mode': 'tree,form',
            'res_model': 'recurring.subscription',
            'domain': [('billing_schedule_id', '=', self.name)]
        }

    def compute_count(self):
        for rec in self:
            rec.subscription_count = self.env[
                'recurring.subscription'].search_count(
                [('billing_schedule_id', '=', rec.name)])

    @api.onchange('recurring_subscription_ids')
    def check_credit(self):
        self.update({
            'credits_ids': [(fields.Command.clear())]
        })
        if self.recurring_subscription_ids:
            for rec in self.env['recurring.subscription.credit'].search(
                    [('recurring_subscription_id', 'in',
                      self.recurring_subscription_ids.ids),
                     ('state', '=', 'fully_approved')],
                    order='create_date ASC'):
                self.update({
                    'credits_ids': [(fields.Command.link(rec.id))]
                })
            self.total_credit_amount = sum(
                self.credits_ids.mapped('credit_amount'))
        else:
            self.total_credit_amount = False

    def invoice_btn(self):
        for rec in self:
            recurring_invoice = [Command.create({
                'product_id': record.product_id.id,
                'price_unit': record.recurring_amount,
            }) for record in rec.recurring_subscription_ids]
            if rec.credits_ids:
                max_amount_date = min(recs.create_date for recs in
                                      filter(lambda p: p.credit_amount == max(
                                          [recs.credit_amount for recs in
                                           rec.credits_ids]),
                                             rec.credits_ids))
                recurring_invoice += [
                    Command.create({
                        'name': f'{max_amount_date} credits',
                        'price_unit': -(
                            max(rec.credits_ids.mapped(
                                'credit_amount')) if rec.credits_ids else False)
                    })]
            if self.env['account.move'].search([('name_id', '=', rec.id)]):
                self.env['account.move'].search(
                    [('name_id', '=', rec.id)]).update({
                        'invoice_line_ids': [(fields.Command.clear())]

                    })
                self.env['account.move'].search(
                    [('name_id', '=', rec.id)]).write({
                        'invoice_line_ids': recurring_invoice
                    })
                invoice = self.env['account.move'].search(
                    [('name_id', '=', rec.id)])
            else:
                invoice = self.env['account.move'].create([
                    {
                        'move_type': 'out_invoice',
                        'invoice_date': fields.Date.context_today(rec),
                        'partner_id': rec.partner_id.id,
                        'currency_id': rec.currency_id.id,
                        'name_id': rec.id,
                        'invoice_line_ids': recurring_invoice
                    }
                ])

            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'domain': [('name_id', '=', rec.name)]

            }

    def action_subscription(self):
        for rec in self.env['billing.schedule'].search([]):
            if not self.env['account.move'].search(
                    [('name_id', '=', rec.name)]):
                date = datetime.today().date()
                # for record in rec.recurring_subscription_ids:
                #     if record.due_date <= date and record.state == 'confirm':
                #         rec.invoice_btn()
                if rec.recurring_subscription_ids.filtered(
                        lambda x: x.due_date <= date and x.state == 'confirm'):
                    rec.invoice_btn()


class AccountMove(models.Model):
    _inherit = 'account.move'

    name_id = fields.Many2one('billing.schedule', string='Name')
