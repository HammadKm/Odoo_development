# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class CompareProductBom(models.TransientModel):
    _name = "compare.product.bom"
    _description = "Compare Product BOM"

    first_bom_id = fields.Many2one('mrp.bom', string='BOM-1')
    second_bom_id = fields.Many2one('mrp.bom', string='BOM-2')

    def action_compare_bom(self):
        if self.first_bom_id.product_tmpl_id != self.second_bom_id.product_tmpl_id:
            raise UserError('invalid')
        BOM1 = self.first_bom_id.display_name
        BOM2 = self.second_bom_id.display_name
        print(BOM1, BOM2)

        products_bom1 = self.first_bom_id.bom_line_ids.mapped('product_id')
        products_bom2 = self.second_bom_id.bom_line_ids.mapped('product_id')

        sales_prices_bom1 = {product.id: product.lst_price for product in products_bom1}
        sales_prices_bom2 = {product.id: product.lst_price for product in products_bom2}

        total_cost_bom1 = sum(
            line.product_qty * sales_prices_bom1[line.product_id.id] for line in self.first_bom_id.bom_line_ids)
        total_cost_bom2 = sum(
            line.product_qty * sales_prices_bom2[line.product_id.id] for line in self.second_bom_id.bom_line_ids)

        if total_cost_bom1 > total_cost_bom2:
            profit = BOM2
        else:
            profit = BOM1

        data = {
            'bom1': BOM1,
            'bom2': BOM2,
            'total_cost_bom1': total_cost_bom1,
            'total_cost_bom2': total_cost_bom2,
            'profit': profit,
        }

        return self.env.ref(
            'compare_bom.action_report_compare_bom').report_action(
            None, data=data)
