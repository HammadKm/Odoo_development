# -*- coding: utf-8 -*-


from werkzeug import urls
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_payu.controllers.main import PayUController
from odoo import _, fields, models
from odoo.exceptions import ValidationError


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'payu':
            return res
        from_currency = self.company_id.currency_id
        to_currency = self.env['res.currency'].search([('name', '=', "INR")])
        order_amount = from_currency._convert(
            self.amount,
            to_currency,
            self.env.company.id,
            fields.Date.context_today(self)
        )

        first_name, last_name = payment_utils.split_partner_name(
            self.partner_id.name)
        api_url = 'https://test.payu.in/_payment'
        payu_values = {
            'key': self.provider_id.payu_merchant_key,
            'txnid': self.reference,
            'amount': order_amount,
            'productinfo': self.reference,
            'firstname': first_name,
            'lastname': last_name,
            'email': self.partner_email,
            'phone': self.partner_phone,
            'return_url': urls.url_join(self.get_base_url(),
                                        PayUController._return_url),
            'api_url': api_url,
        }
        payu_values['hash'] = self.provider_id._payu_generate_sign(payu_values,
                                                                   incoming=False, )
        return payu_values

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code,
                                                    notification_data)
        if provider_code != 'payu' or len(tx) == 1:
            return tx

        reference = notification_data.get('txnid')
        if not reference:
            raise ValidationError(
                "PayU: " + _("Received data with missing reference (%s)",
                             reference))

        tx = self.search(
            [('reference', '=', reference), ('provider_code', '=', 'payu')])
        if not tx:
            raise ValidationError(
                "PayU: " + _("No transaction found matching reference %s.",
                             reference))

        return tx

    def _process_notification_data(self, notification_data):
        print('not', notification_data)
        super()._process_notification_data(notification_data)
        if self.provider_code != 'payu':
            return

        self.provider_reference = notification_data.get('payuId')

        payment_method_type = notification_data.get('bankcode', '')
        payment_method = self.env['payment.method']._get_from_code(
            payment_method_type)
        self.payment_method_id = payment_method or self.payment_method_id

        status = notification_data.get('status')
        if status == 'success':
            self._set_done()
        else:
            error_code = notification_data.get('Error')
            self._set_error(
                "PayU: " + _("The payment encountered an error with code %s",
                             error_code))
