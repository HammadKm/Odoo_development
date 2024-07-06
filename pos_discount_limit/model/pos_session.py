# -*- coding: utf-8 -*-

from odoo import models, fields


class PosSession(models.Model):
    _inherit = 'pos.session'

    discount_limit = fields.Float(string='Discount limit',
                                  related='config_id.discount_limit')

    # def _loader_params_res_config_settings(self):
    #     result = super()._loader_params_res_config_settings()
    #     result['search_params']['fields'].append(
    #         ['session_discount_limit', 'discount_limit'])
    #     print(result)
    #     return result
