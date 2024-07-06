# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_owner_id = fields.Many2one('res.partner', string='Owner')
