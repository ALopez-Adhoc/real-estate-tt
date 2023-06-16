from odoo import _, api, fields, models


class PropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'Property tags'
    _order = 'name'

    name = fields.Char(string='Tag', required=True)
    color = fields.Integer(string='Color', default=1)

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','The name must be unique')
    ]
