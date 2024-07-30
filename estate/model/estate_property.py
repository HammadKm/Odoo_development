from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection(
        string='garden orientation type',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                   ('west', 'West')])
    state = fields.Selection(
        string='status',
        selection=[('new', 'New'), ('offer received', 'Offer received'),
                   ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True,
        default='new')
    property_type = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    seller_id = fields.Many2one('res.users', string="Sales person", copy=False,
                                default=lambda self: self.env.user)
    tags_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
