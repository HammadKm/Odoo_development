# -*- coding: utf-8 -*-


from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    total_sale_count = fields.Integer(string='Total Sale Count',
                                      compute='_compute_total_sale_count')

    def _compute_total_sale_count(self):
        for rec in self:
            print(rec)
            sale_history = self.env['sale.order.line'].search(
                [('state', '=', 'sale'), ('product_template_id', '=', rec.id)])
            print(sale_history)
            print(len(sale_history))
            if sale_history:
                print('ghjk')
                rec.total_sale_count = len(sale_history)
            else:
                print('lkj')
                rec.total_sale_count = 0

    @api.onchange('list_price')
    def change_sale_price(self):
        print(self._origin)
        # for rec in self:
        #     sales_history = self.env['sale.order.line'].search(
        #         [('state', '=', 'draft'), ('product_template_id', '=', rec._origin)])
        #     print("dfgh",sales_history)
