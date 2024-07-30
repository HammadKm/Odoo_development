# -*- coding: utf-8 -*-

from odoo import fields, models, Command, api


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = "Material Request"
    _rec_name = "employee_id"
    _inherit = "mail.thread"

    request = fields.Char(string="Reference", )
    employee_id = fields.Many2one('res.users', string="Name", required=True)
    date = fields.Date(string="Date", default=fields.Date.today())
    company_id = fields.Many2one('res.company', string="Company",
                                 default=lambda self: self.env.company,
                                 readonly=True)
    state = fields.Selection(string='status',
                             selection=[('draft', 'Draft'),
                                        ('submitted', 'Submitted'),
                                        ('first approved', 'First Approved'),
                                        ('fully approved', ' Fully Approved'),
                                        ('rejected', 'Rejected')],
                             default='draft', tracking=True)
    user_id = fields.Many2one('res.users', string='User',
                              default=lambda self: self.env.user, readonly=True)
    material_order_ids = fields.One2many('material.order.line', 'request_id')
    reference_no = fields.Char(string="Reference number", readonly=True,
                               default='New')
    purchase_count = fields.Integer(compute='_compute_purchase_count')

    transfer_count = fields.Integer(compute='_compute_transfer_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'material.request') or 'New'
        res = super(MaterialRequest, self).create(vals_list)
        return res

    def submit_button(self):
        return self.write({'state': 'submitted'})

    def manager_approve_button(self):
        return self.write({'state': 'first approved'})

    def head_approve_button(self):
        for rec in self:
            print(rec.reference_no)
            for records in rec.material_order_ids:
                if records.operation_type == 'purchase order':
                    vendor = records.product_id.seller_ids
                    for recs in vendor:
                        self.env['purchase.order'].create([
                            {
                                'partner_id': recs.partner_id.id,
                                'origin': rec.reference_no,
                                'company_id': rec.company_id.id,
                                'currency_id': rec.company_id.currency_id.id,
                                'date_order': fields.Date.today(),
                                'order_line': [Command.create({
                                    'product_id': records.product_id.id,
                                })]
                            }
                        ])
                else:
                    self.env['stock.picking'].create([
                        {
                            'location_id': records.src_location_id.id,
                            'origin': rec.reference_no,
                            'location_dest_id': records.dest_location_id.id,
                            'picking_type_id': self.env.ref(
                                'stock.picking_type_internal').id,
                            'move_ids': [Command.create({
                                'name': '/',
                                'product_id': records.product_id.id,
                                'product_uom_qty': records.material_qty,
                                'location_id': records.src_location_id.id,
                                'location_dest_id': records.dest_location_id.id,

                            })]
                        }
                    ])

        return self.write({'state': 'fully approved'})

    def reject_button(self):
        return self.write({'state': 'rejected'})

    def _compute_purchase_count(self):
        count = self.env['purchase.order'].search_count(
            [('origin', '=', self.reference_no)])
        self.purchase_count = count

    def action_purchase_order(self):
        print(self.material_order_ids.mapped('product_id').ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase orders',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [
                ('origin', '=', self.reference_no)]
        }

    def _compute_transfer_count(self):
        t_count = len(self.material_order_ids.filtered(
            lambda x: x.operation_type == 'internal transfer').mapped(
            'operation_type'))
        self.transfer_count = t_count

    def action_internal_transfer(self):
        print('hi')
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase orders',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [
                ('origin', '=', self.reference_no)]
        }
