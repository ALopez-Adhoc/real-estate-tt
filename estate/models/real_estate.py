from odoo import api, models, fields, exceptions

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'App to manage Properties'
    _order = 'id desc'
    
    name = fields.Char('Properties', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability', copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3, day=1))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area(m²)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area(m²)')
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
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one(string='Salesperson', comodel_name='res.users', copy=False, default=lambda self: self.env.user)
    tag_ids = fields.Many2many(comodel_name='estate.property.tags', string='Tags')
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (m²)')
    best_price = fields.Integer(compute='_compute_best_price', string='Best Price')
    type_id = fields.Many2one(comodel_name='estate.property.type', string='Property Lines')
    user_id = fields.Many2one(comodel_name='res.users', string='User')

    _sql_constraints = [
        ('check_selling_price','CHECK(selling_price>=0)','Can not use negative prices'),
        ('check_expected_price','CHECK(expected_price>=0)','Can not use negative prices')]
    
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for rec in self:
            expected_price2 = rec.expected_price * 0.9
            if rec.selling_price < expected_price2 and rec.selling_price != 0:
                raise exceptions.ValidationError('The price of the sell is to low')
        
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.garden_area + rec.living_area
    
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped('price')) if rec.offer_ids.mapped('price') else False

    @api.onchange('garden')
    def _onchange_garden(self):
        if  self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def sell_properties(self):
        for rec in self:
            if rec.state != 'canceled':
                rec.state = 'sold'
            else:
                raise exceptions.UserError('Canceled properties can not be sold')
        return True
    
    def cancel_properties(self):
        for rec in self:
            if rec.state != 'sold':
                rec.state = 'canceled'
            else:
                raise exceptions.UserError('Sold properties can not be canceled')
        return True
    
    @api.ondelete(at_uninstall=True)
    def _unlink_except_state(self):
        for rec in self:
            if rec.state not in ['new','canceled']:
                raise exceptions.UserError("Records can be deleted only if are New or Canceled")