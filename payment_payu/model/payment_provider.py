# -*- coding: utf-8 -*-
import hashlib

from odoo.addons.payment_payu import const
from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', "PayU")], ondelete={'payu': 'set default'})
    payu_merchant_key = fields.Char(
        string="Merchant Key",
        help="The key solely used to identify the account with PayU",
        required_if_provider='payu')
    payu_merchant_salt = fields.Char(
        string="Merchant Salt", required_if_provider='payu',
        groups='base.group_system')

    def _payu_generate_sign(self, values, incoming=True):
        self._setup_provider(self.code)
        sign_values = {
            **values,
            'key': self.payu_merchant_key,
            'salt': self.payu_merchant_salt,
        }
        if incoming:
            keys = ('salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname'
                    '|productinfo|amount|txnid|key')
            sign = '|'.join(
                f'{sign_values.get(k) or ""}' for k in keys.split('|'))
        else:
            keys = ('key|txnid|amount|productinfo|firstname|email|udf1|udf2'
                    '|udf3|udf4|udf5||||||salt')
            sign = '|'.join(
                f'{sign_values.get(k) or ""}' for k in keys.split('|'))
        return hashlib.sha512(sign.encode('utf-8')).hexdigest()

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes."""
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'payu':
            return default_codes
        return const.DEFAULT_PAYMENT_METHODS_CODES
