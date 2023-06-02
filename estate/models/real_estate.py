from odoo import api, models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'App to manage Properties'
    
    name = fields.Char('Properties', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3, day=1))
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price', required=True, readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area(m^2)')
    garden_orientation = fields.Selection(selection=[
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ],  string='Garden Orientation')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('o_r', 'Offer Received'),
        ('o_a', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string='State', required=True, copy=False, default='new')