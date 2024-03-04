from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError, UserError
from datetime import date


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    email = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    CR_ratio = fields.Float()
    blood_type = fields.Selection([('a', 'A'), ('b', 'B'), ('o', 'O')])
    PCR = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer()
    department_id = fields.Many2one('hms.department')
    capacity = fields.Integer(related='department_id.capacity')
    doctors_id = fields.Many2many('hms.doctors')
    customer_id = fields.Many2one('res.partner')
    log_history_id = fields.One2many('hms.logging', 'patient_id')
    state = fields.Selection(
        [('undetermined', 'Undetermined'), ('good', 'Good'), ('fair', 'Fair'), ('serious', 'Serious'), ],
        default='undetermined')

    @api.onchange('birth_date')
    def _age_birth_date(self):
        if self.birth_date:
            self.age = date.today().year - self.birth_date.year

    @api.onchange('email')
    def validation_email(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match is None:
                raise ValidationError('this Email Is Not Valid')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique.'), ]

    @api.model
    def create(self, vals_list):
        if not vals_list['email']:
            vals_list['email'] = f"{vals_list['first_name']}@gmail.com"
        patient = self.search([('email', '=', vals_list['email'])])
        if patient:
            raise UserError(f"{vals_list['email']} already exists")

        return super().create(vals_list)

    def patient_statue(self):
        if self.state == 'undetermined':
            self.state = 'good'
        elif self.state == 'good':
            self.state = 'fair'
        elif self.state == 'fair':
            self.state = 'serious'
        elif self.state == 'serious':
            self.state = 'undetermined'
        self.create_log()

    def create_log(self):
        self.env['hms.logging'].create({
            'created_by': self.first_name,
            'date': date.today(),
            'description': f'State changed to {self.state} ',
            'patient_id': self.id
        })

    @api.onchange('age')
    def pcr_check(self):
        if self.age < 30:
            self.PCR = True
            return {
                'warning': {
                    'title': 'PCR',
                    'message': 'pcr has been checked.'
                }
            }
