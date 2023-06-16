from odoo import _, api, fields, models


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Types of properties'
    _order = 'sequence desc, name'

    name = fields.Char(string='Property Type', required=True)
    property_ids = fields.One2many(comodel_name='estate.property', inverse_name='property_type_id')
    sequence = fields.Integer(string='Sequence', default=1)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_type_id')
    offer_count = fields.Integer(compute='compute_offer_count', string=" Offers")

    
    @api.depends('offer_ids')
    def compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)
    

    _sql_constraints = [
        ('unique_name','UNIQUE(name)','The name must be unique')
    ]
