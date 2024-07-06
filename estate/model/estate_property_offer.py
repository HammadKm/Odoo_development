from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _rec_name = "price"

    price = fields.Float()
    status = fields.Selection(
        selection=[('refused', 'Refused'), ('accepted', 'Accepted')], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

