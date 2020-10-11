from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def open_patient_appointment(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def get_appointment_count(self):
        for rec in self:
            rec.count = rec.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointments_count = rec.count

    @api.onchange('doctor_id')
    def set_gender_doc(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.doc_gender

    patient_name = fields.Char(string='NAME', required=True, track_visibility='always')
    patient_age = fields.Integer(string='AGE', track_visibility='always', group_operator=False)
    gender = fields.Selection([('male', 'MALE'),
                               ('female', 'FEMALE'), ]
                              , default='male', string="GENDER")
    age_group = fields.Selection([
        ('major', 'MAJOR'),
        ('minor', 'MINOR'),
        ('null', 'NULL'), ],
        string='AGE GROUP', compute='set_age_group')
    notes = fields.Text(string='REGISTRATION NOTES')
    # for patient id
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    appointments_count = fields.Integer(string='Appointments', compute=get_appointment_count)
    # appointments_id = fields.Many2one('hospital.appointment')

    # appointments_id = fields.One2many('hospital.appointment', 'patient_id')

    # function for computing field value by giving depending field vale
    active = fields.Boolean('Active', default=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Consult")
    doctor_gender = fields.Selection([('male', 'MALE'), ('female', 'FEMALE')],
                                     default='male', string='Doc Gender')

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age > 18:
                    rec.age_group = 'major'
                else:
                    rec.age_group = 'minor'
            else:
                rec.age_group = 'null'

    # function for adding error message or constrain

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('AGE MUST BE GREATER THAN 5!'))

    # function for generating sequence number or patient id

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result
