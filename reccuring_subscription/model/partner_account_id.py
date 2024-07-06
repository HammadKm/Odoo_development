# -*- coding: utf-8 -*-

import random
import re
import string
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PartnerAccountID(models.Model):
    _name = "partner.account"
    _description = "Partner Account"
    _rec_name = "account"

    _sql_constraints = [
        ('account_unique', 'unique(account)', 'Account ID must be unique')
    ]
    account = fields.Char(string="Account ID")

    @api.constrains('account')
    def check_account(self):
        """validate the field establishment_id with 3 alphabets , 3 numbers
        and 2 hyphens"""
        for rec in self:
            if not re.match(r"^(?=.*[a-zA-Z].*[a-zA-Z].*[a-zA-Z])("
                            r"?=.*\d.*\d.*\d)(?=.*-.*-)[a-zA-Z\d-]*",
                            rec.account):
                raise ValidationError(
                    "account must contain 3 alphabets ,3 numbers"
                    " and 2 hyphens")


class ResPartners(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [
        ('establishment_unique', 'unique(establishment)',
         'Establishment ID must be unique')
    ]

    account_id = fields.Many2one('partner.account', string='Account ID',
                                 ondelete='cascade')
    establishment = fields.Char(string='Establishment ID', index=True)

    @api.model
    def create(self, vals):
        unique = self.account_id.create({'account': self._genarate_id()})
        vals['account_id'] = unique.id
        return super(ResPartners, self).create(vals)

    def _genarate_id(self):
        chars = string.ascii_letters
        digits = string.digits
        unique_id = ""
        letters = random.choices(chars, k=3)
        numbers = random.choices(digits, k=3)
        unique_id += '-'.join(letters + numbers)
        return unique_id


class CrmLead(models.Model):
    """Sql constrains for the field order ID is not working """
    _inherit = 'crm.lead'
    # _sql_constraints = [
    #     ('check_order_unique', 'unique(order)', 'Order ID must be unique')]
    order = fields.Char(string='Order ID', required=True)
