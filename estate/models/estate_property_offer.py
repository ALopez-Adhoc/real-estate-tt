from odoo import _, api, fields, models


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'List of offers'

    name = fields.Char(string='Offer')
    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', selection=[
        ('accepted', 'Accepted'), 
        ('refused', 'Refused')])
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)