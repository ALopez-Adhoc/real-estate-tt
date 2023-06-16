from odoo import _, api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='salesperson_id')
