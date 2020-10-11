from odoo import models, fields, api, _


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string="PATIENT")
    appointment_date = fields.Date(string="APPOINTMENT DATE")

    def create_appointment(self):
        val = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date
        }
        self.env['hospital.appointment'].create(val)
