# -*- coding: utf-8 -*-

from odoo import fields, models


class MaterialOrderLine(models.Model):
    _name = "material.order.line"
    _description = "Material Order Line"
    _rec_name = "request_id"

    product_id = fields.Many2one('product.product', string="Material")
    material_qty = fields.Integer(string="Quantity", required=True, default=1)
    operation_type = fields.Selection(string="Operation Type", selection=[
        ('internal transfer', 'Internal Transfer'),
        ('purchase order', 'Purchase Order')],required=True)
    src_location_id = fields.Many2one('stock.location', string="Source location")
    dest_location_id = fields.Many2one('stock.location',
                                        string="Destination Location")
    request_id = fields.Many2one('material.request', string="Request")
