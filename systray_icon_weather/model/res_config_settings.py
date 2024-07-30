# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weather = fields.Boolean(string='Session Discount limit',
                             config_parameter='systray_icon_weather.weather')
    api_key = fields.Char(string='API Key',
                          config_parameter='systray_icon_weather.api_key')
    location = fields.Char(string='Location',
                           config_parameter='systray_icon_weather.location')

    def get_weather(self):
        weather = self.env['ir.config_parameter'].sudo().get_param(
            'systray_icon_weather.weather')
        return weather
