# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    pos_session_discount_limit = fields.Boolean(string='Session Discount limit',
                                                related='pos_config_id.session_discount_limit',
                                                config_parameter='pos_discount_limit.session_discount_limit',
                                                help='Check this field for '
                                                     'enabling discount limit',
                                                readonly=False)
    pos_discount_limit = fields.Float(string='Limit amount',
                                      related='pos_config_id.discount_limit',
                                      config_parameter='pos_discount_limit'
                                                       '.discount_limit',
                                      help='The discount limit amount in '
                                           'percentage ', readonly=False,
                                      default=100)

    # @api.onchange('pos_session_discount_limit')
    # def _onchange_discount_limit(self):
    #     if self.pos_session_discount_limit == False:
    #         self.pos_discount_limit = 0

