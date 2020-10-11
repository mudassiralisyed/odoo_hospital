from odoo import fields, api, models


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Record'

    name = fields.Char(string='Doctor Name', required=True)
    doc_gender = fields.Selection([('male', 'MALE'), ('female', 'FEMALE')],
                              default='male', string='GENDER')
    user_id = fields.Many2one('res.users', string='Related User')
    patient_id = fields.Many2one('hospital.patient', string='Related Patient')
    # related_patient_id = fields.Many2one('hospital.patient', string='Related Patient ID')
