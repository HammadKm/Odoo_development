# -*- coding: utf-8 -*-


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    sale_order_ids = fields.One2many('sale.order', 'partner_id',
                                     string="Sale Orders")

    total_product_sold = fields.Integer(compute='_compute_count')

    @api.model
    def get_sale_orders(self):
        for record in self:
            sale_orders = self.env['sale.order'].search(
                [('partner_id', '=', record.id)])
            return sale_orders

    def _compute_count(self):
        count = len(self.sale_order_ids)
        self.total_product_sold = count

    def action_product_count(self):

        print(self.sale_order_ids.order_line.mapped('product_template_id').ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'sold products',
            'view_mode': 'tree',
            'res_model': 'product.template',
            'domain': [('id', 'in', self.sale_order_ids.order_line.mapped('product_template_id').ids)]
        }

