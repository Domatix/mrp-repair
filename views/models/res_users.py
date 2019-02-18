from odoo import models, fields


class User(models.Model):
    _inherit = 'res.users'

    rep = fields.One2many(
        comodel_name='mrp.repair',
        inverse_name='resp',
        string='Repairs')
