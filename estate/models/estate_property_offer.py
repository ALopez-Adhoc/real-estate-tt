from odoo import _, api, fields, models, exceptions


class Offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'List of offers'

    name = fields.Char(string='')
    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', selection=[
        ('accepted', 'Accepted'), 
        ('refused', 'Refused')])
    partner_id = fields.Many2one(comodel_name='res.partner', string='Client', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Date Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', default=lambda self: fields.Date.today())

    _sql_constraints = [
        ('check_price','CHECK(price>=0)','You can not use negative prices')
    ]
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = fields.Date.add(rec.create_date, days=rec.validity) if rec.create_date else False

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.create_date:
                delta_days = rec.date_deadline - rec.create_date.date()
                rec.validity = delta_days.days
            else:
                False

    def accept_offer(self):
        for rec in self:
            if 'accepted' in rec.property_id.offer_ids.mapped('status'):
                raise exceptions.UserError('Another offer has been accepted. Cancel it first if you want to accept another offer.')
            else:
                rec.status = 'accepted'
                rec.property_id.selling_price = rec.price
                rec.property_id.buyer_id = rec.partner_id

    def cancel_offer(self):
        for rec in self:
            rec.status = 'refused'