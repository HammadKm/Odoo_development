# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    session_discount_limit = fields.Boolean(string='Session Discount limit',
                                            help='Check this field for '
                                                 'enabling discount limit')
    discount_limit = fields.Float(string='Limit amount')
