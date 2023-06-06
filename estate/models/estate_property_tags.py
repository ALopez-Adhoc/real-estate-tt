from odoo import _, api, fields, models


class PropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Property tags'

    name = fields.Char(string='Tag', required=True)

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','The name must be unique')
    ]
