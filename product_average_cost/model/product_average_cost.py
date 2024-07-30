# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    average_cost = fields.Float(string="Average Cost",
                                compute="_compute_avg_cost")

    def _compute_avg_cost(self):
        """computing average cost of the product based on the previous purchases
        Avg_cost = former_qty * former_avg_cost + incoming_qty * incoming_price
         / total_qty """
        for rec in self:
            purchase_history = self.env['purchase.order.line'].search(
                [('state', '=', 'purchase'), ('product_id', '=', rec.id)])
            if purchase_history:
                total_quantity = sum(purchase_history.mapped('product_uom_qty'))
                incoming_rec = max(purchase_history, key=lambda x: x.date_approve)
                former_rec = purchase_history.filtered(
                    lambda y: y.id != incoming_rec.id)
                former_qty = sum(former_rec.mapped('product_uom_qty'))
                if len(former_rec) >= 1:
                    cost = 0
                    for recs in former_rec[::-1]:
                        cost += recs.product_uom_qty * recs.price_unit
                    amount = cost / former_qty
                    avg = (former_qty * amount + incoming_rec.product_uom_qty *
                           incoming_rec.price_unit) / total_quantity
                    rec.average_cost = avg
                else:
                    rec.average_cost = (purchase_history.product_uom_qty *
                                         purchase_history.price_unit) / purchase_history.product_uom_qty
            else:
                rec.average_cost = False


