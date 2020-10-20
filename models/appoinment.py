from odoo import api, models, _, fields


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Patient Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # for making tree view of record in descending order
    # _order = 'id desc'
    # or if we want to make an other field for order sequence
    _order = 'appointment_date desc'
    _rec_name = "patient_id"

    def get_default_note(self):
        return "please be on time"

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    appointment_count = fields.Integer(string='Total number of appointments', compute="get_count")
    patient_age = fields.Integer(string='AGE', related='patient_id.patient_age')
    notes = fields.Text(string='REGISTRATION NOTES', default=get_default_note)
    d_notes = fields.Text(string='doctor NOTE')
    p_notes = fields.Text(string='medical NOTE')
    # for patient id
    patient_id = fields.Many2one('hospital.patient', string='Patient Name', context={}, required=True)
    appointment_date = fields.Date(string='DATE', required=True)
    # One2Many Relation with PatientAppointmentLines

    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointments_id', string='Appointment lines')
    # appointment_line = fields.One2many('hospital.appointment.lines', 'appointments_id', string='Appointment lines')
    # appointment_line = fields.Text(string='name')
    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('conform', 'Conform'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')
    doctor_id = fields.Many2many('hospital.doctor', 'hospital_patient_rel', 'appointment_id', 'doctor_id',
                                 string='Doctor')

    def conform_appointment(self):
        for rec in self:
            rec.state = 'conform'
            if rec.state == 'conform':

                rec.env['res.users'].create({
                    'name': rec.patient_id.patient_name,
                    'login': rec.patient_id.patient_name,
                })


    def done_appointment(self):
        for rec in self:
            rec.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    def get_count(self):
        for rec in self:
            appointments_count = rec.search_count([])
            if appointments_count:
                rec.appointment_count = appointments_count


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Patient Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string='Quantity')
    appointments_id = fields.Many2one('hospital.appointment', string='Appointment ID')
