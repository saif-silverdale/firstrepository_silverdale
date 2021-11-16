# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Doctor(models.Model):  # original name : dap_doctor
    _name = 'dap.doctor'
    _description = 'Table for Doctor'

    name = fields.Char("Doctor Name")
    speciality = fields.Char("Speciality")
    attendant_id = fields.One2many('dap.attendant', 'doc_id', "Attendant")
    doctor_apt = fields.One2many('dap.appointment', 'doctor_id')

    appointment_number = fields.Integer(string='Appointment Number', compute='compute_appointment_number')

    def name_get(self):
        """
        This function implements name_get orm method
        :return: returns appended name of the doctor as well as its speciality
        """
        res = []
        for rec in self:
            res.append((rec.id, '%s-%s' % (rec.name, rec.speciality)))
        return res

    def compute_appointment_number(self):
        """
        This function computes the number of appointments each doctor have
        """
        for rec in self:
            appointment_number = self.env['dap.appointment'].search_count([('pat_specie', '=', rec.speciality)])
            rec.appointment_number = appointment_number

    def action_open_appointments(self):
        """
        This function co-relates with the compute_appointment_function
        :return: returns a view when the button is clicked
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'appointments_call',
            'res_model': 'dap.appointment',
            'domain': [('pat_specie', '=', self.speciality)],
            'view_mode': 'tree,form',
            'target': 'current'
        }

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        THis function is used for implementing name_search orm method of name_search
        :return:
        """
        if args is None:
            args = []
        domain = args + ['|', ('name', operator, name), ('speciality', operator, name)]
        return super(Doctor, self)._search(domain, limit=limit)


class Attendant(models.Model):  # original : dap_attendant
    _name = 'dap.attendant'
    _description = 'Table for Attendant'

    name = fields.Char("Name")
    regnum = fields.Char("Registration Number")
    doc_id = fields.Many2one('dap.doctor')


class Appointment(models.Model):  # original : dap_appointment
    _name = 'dap.appointment'
    _description = 'Table for Appointments'
    _rec_name = 'animal_id'

    animal_id = fields.Many2one('vetapp.animals', string="Patient Name")
    apt_time = fields.Datetime("Time of Appointment")
    doctor_id = fields.Many2one('dap.doctor')
    pat_specie = fields.Many2one(related="animal_id.specie_id")
    pat_doc_speciality = fields.Char(related="doctor_id.speciality")
    pat_image = fields.Binary(related="animal_id.image_hold", store=True, readonly=False)


class Patient(models.Model):  # original : dap_patient
    _inherit = 'vetapp.animals'
    _description = 'Table for Patient'


class TestSecurity(models.Model):  # original : security_test
    _name = "dap.testsecurity"

    name = fields.Char(string="Name")
    responsible = fields.Many2one("res.users")
    active = fields.Boolean("Active")
    phone = fields.Char("Phone")
    email_id = fields.Char("Email Id")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')],
                             default='draft', string="Status")

    def action_confirm(self):
        """
        function for changing state to confirm
        """
        self.state = 'confirm'

    def action_draft(self):
        """
        function for changing state to draft
        """
        self.state = 'draft'

    def action_done(self):
        """
        function for changing state to done
        """
        self.state = 'done'

    def action_cancel(self):
        """
        function for changing state to cancel
        """
        self.state = 'cancel'

    _sql_constraints = [('sale_order_not_null', 'CHECK(phone IS NOT NULL)', 'phone cannot be null')]

    def action_send_email(self):
        """
        function for sending email
        """
        template_id = self.env.ref('dap.patient_card_email_template').id
        print("Template Id is", template_id)
        template = self.env['mail.template'].browse(template_id)
        print("Template is", template)
        template.send_mail(self.id, force_send=True)

    def orm_method(self):
        """
        function where orm methods were implemented
        """
        # the search method
        search = self.env["dap.testsecurity"].search([])
        print("The result of search query is...", search)
        search1 = self.env["dap.testsecurity"].search([('name', '=', 'Test1')])
        print("The result of search1 query is...", search1)
        # the search-count method
        searchcount = self.env["dap.testsecurity"].search_count([])
        print("The result of searchcount query is...", searchcount)
        searchcount1 = self.env["dap.testsecurity"].search_count([('name', '=', 'Test1')])
        print("The result of searchcount1 query is...", searchcount1)
        # the ref method
        refer = self.env.ref('dap.dap_securitytest')
        print("The result of refer is...", refer.id)
        # filtered Method
        filter_search = self.env['dap.testsecurity'].search([]).filtered(lambda a: a.name == 'Test2')
        print("Filtered Search..", filter_search)
        # Mapped Method
        mapped_search = self.env['dap.testsecurity'].search([]).mapped('name')
        print("Mapped Search..", mapped_search)
        # Sorted Method
        sorted_mapped_search = self.env['dap.testsecurity'].search([]).sorted(key='name', reverse=True).mapped('name')
        print("Sorted Mapped Search..", sorted_mapped_search)
        # get_default function

    @api.model
    def default_get(self, fields):
        """
        function for getting some data by default in field
        """
        res = super(TestSecurity, self).default_get(fields)
        print("Test....")
        res['name'] = 'Write your name here'
        return res

    @api.onchange('responsible')
    def onchange_responsible(self):
        """
        function for automatically entering the phone number of the admin selected
        """
        if self.responsible:
            if self.responsible.phone:
                self.phone = self.responsible.phone
            else:
                self.phone = ''

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
