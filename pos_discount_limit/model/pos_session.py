# -*- coding: utf-8 -*-

from odoo import models, fields


class PosSession(models.Model):
    _inherit = 'pos.session'

    discount_limit = fields.Float(string='Discount limit',
                                  related='config_id.discount_limit',
                                  store=True)
    session_discount_limit = fields.Boolean(string='Session Discount limit',
                                            related='config_id'
                                                    '.session_discount_limit',
                                            help='Check this field for '
                                                 'enabling discount limit')

    def get_discount_limit(self):
        return [self.discount_limit, self.session_discount_limit]

    def update_discount_limit(self, balance):
        self.discount_limit = balance

