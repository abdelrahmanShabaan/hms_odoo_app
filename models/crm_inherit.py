from odoo import models, fields, api
from odoo.exceptions import UserError


class Customer(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.One2many('hms.patient', 'customer_id')

    def unlink(self):
        if self.related_patient_id:
            raise UserError("Can not delete customer, this customer have related patient")