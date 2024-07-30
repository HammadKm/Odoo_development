# -*- coding: utf-8 -*-

import hmac
import logging
import pprint

from werkzeug.exceptions import Forbidden

from odoo.http import request, Controller, route

_logger = logging.getLogger(__name__)


class PayUController(Controller):
    _return_url = '/payment/payu/return'

    @route(_return_url, type='http', auth='public', methods=['GET', 'POST'],
           csrf=False,
           save_session=False)
    def payu_return_from_checkout(self, **data):
        _logger.info("handling redirection from PayU money with data:\n%s",
                     pprint.pformat(data))

        tx_sudo = request.env[
            'payment.transaction'].sudo()._get_tx_from_notification_data('payu',
                                                                         data)
        self._verify_notification_signature(data, tx_sudo)
        tx_sudo._handle_notification_data('payu', data)
        return request.redirect('payment/status')

    @staticmethod
    def _verify_notification_signature(notification_data, tx_sudo):
        received_signature = notification_data.get('hash')
        if not received_signature:
            _logger.warning("received notification with missing signature")
            raise Forbidden()
        expected_signature = tx_sudo.provider_id._payu_generate_sign(
            notification_data, incoming=True
        )
        if not hmac.compare_digest(received_signature, expected_signature):
            _logger.warning("received notification with invalid signature")
            raise Forbidden()
