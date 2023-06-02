from odoo import api, models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'App to manage Properties'
    
    name = fields.Char('Properties', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability')
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price', required=True)
    bedrooms = fields.Integer('Bedrooms')
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