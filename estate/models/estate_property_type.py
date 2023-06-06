from odoo import _, api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types of properties'

    name = fields.Char(string='Property Type', required=True)

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','The name must be unique')
    ]
