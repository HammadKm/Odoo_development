# -*- coding: utf-8 -*-
import requests

from odoo.http import request, Controller, route


class WeatherController(Controller):
    @route('/weather/check', type='json', auth="public",
           methods=['POST'])
    def weather_notification(self):
        weather_data = {'data': False}
        key = request.env['ir.config_parameter'].sudo().get_param(
            'systray_icon_weather.api_key')
        loc = request.env['ir.config_parameter'].sudo().get_param(
            'systray_icon_weather.location')

        url = f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={key}"
        city_req = requests.get(url, timeout=20)
        if city_req.status_code == 200:
            weather_data = city_req.json()

        return weather_data
