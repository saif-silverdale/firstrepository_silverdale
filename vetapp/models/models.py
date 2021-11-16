# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class Animals(models.Model):  # Original Name : vetapp_animals
    _name = 'vetapp.animals'

    @api.depends('birthdate')
    def _compute_age(self):
        """
        This is a function for computing age of the record
        :return: It doesn't return anything
        """
        for rec in self:
            if rec.birthdate:
                rec.age = (fields.date.today() - rec.birthdate) / timedelta(days=365.2425)
            else:
                rec.age = False

    _description = 'vetapp.animal and it can be different from name'
    name = fields.Char(string="Animal Name", required=True)
    specie_id = fields.Many2one("vetapp.specie", required=True)
    breed_id = fields.Many2one("vetapp.breed", domain="[('species_id','=',specie_id)]")
    owner_id = fields.Many2one("res.partner", domain="[('active','=',True)]")
    diagnosis_id = fields.One2many("vetapp.animal_diagnosis", "an_animal_id", "Diagnosis")
    ownerphone = fields.Char(related="owner_id.phone", store=True)
    age = fields.Float(compute=_compute_age)
    birthdate = fields.Date(help="if you don't know the exact one write the close one")
    note = fields.Text(default="write note here")
    spayorneuter = fields.Boolean("SpayedorNeutered")
    firstvisit = fields.Datetime('First Visit', default=lambda self: fields.Datetime.now())
    image_hold = fields.Binary("medium_sized image", attachment=True, help="Medium_sized Image of this Provider"
                                                                           "It is automatically Resized as a 128x128px"
                                                                           " image, with aspect ratio preserved"
                                                                           "Use this field in form views or some "
                                                                           "kanban views.")
    aggressive = fields.Boolean("Aggressive Behaviour")
    aggressionnotes = fields.Text("Aggression Notes")
    specialdiet = fields.Boolean("Special Diet")
    primaryvet_id = fields.Many2one("res.users")
    speciespic = fields.Binary(related='specie_id.Image')


class AnimalDiagnosis(models.Model):  # Original Name : vetapp_animal_diagnosis
    _name = "vetapp.animal_diagnosis"

    an_diagnosis_id = fields.Many2many('vetapp.diagnosis')
    an_animal_id = fields.Many2one('vetapp.animals')
    an_vet_id = fields.Many2one('res.users')
    diagnosis_date = fields.Date('Diagnosis Date')
    an_symptom_id = fields.Many2many('vetapp.symptom')
    notes = fields.Text('Notes')


class Specie(models.Model):  # Original Name : vetapp_specie
    _name = "vetapp.specie"

    name = fields.Char("Animal Specie")
    animal_id = fields.One2many("vetapp.animals", "specie_id", "Name")
    notes = fields.Text()
    Image = fields.Binary("Image")


class Breed(models.Model):  # Original Name : vetapp_breed
    _name = "vetapp.breed"

    name = fields.Char("Animal Breed")
    species_id = fields.Many2one("vetapp.specie")
    animal_ids = fields.One2many('vetapp.animals', 'breed_id')
    notes = fields.Text()


class ResPartner(models.Model):  # Original Name : vetapp_res_partner
    _inherit = "res.partner"

    orientation_res = fields.Boolean("Orientation Done")
    orientation_staff_id = fields.Many2one("res.users")
    pets_ids = fields.One2many('vetapp.animals', 'owner_id', 'Pets')

    def process_animals(self):
        """
        applied to a button placed in res.partner table to check that whether the animal is linked with customer
        :return: Return the name of the animal associated with the customer
        """
        for rec in self.pets_ids:
            print("Processing the field", rec.name)


class Diagnosis(models.Model):  # Original Name : vetapp_diagnosis
    _name = "vetapp.diagnosis"

    name = fields.Char(string="Name")
    code = fields.Char("Diagnosis Code")
    type = fields.Char("what is type")
    symptom_id = fields.Many2many('vetapp.symptom')
    treatment_id = fields.Many2many('vetapp.treatment')
    notes = fields.Text()


class Symptom(models.Model):  # Original Name : vetapp_symptom
    _name = "vetapp.symptom"

    code = fields.Char("Symptom Code")
    type = fields.Char()
    diagnosis_ids = fields.Many2many("vetapp.diagnosis")
    notes = fields.Text()


class Treatment(models.Model):  # Original Name : vetapp_treatment
    _name = "vetapp.treatment"

    code = fields.Char("Treatment Code")
    type = fields.Char()
    notes = fields.Text()
    product_ids = fields.Many2many("product.template")
    diagnosis_ids = fields.Many2many("vetapp.diagnosis")


class Products(models.Model):  # Original Name : vetapp_products
    _inherit = "product.template"

    treatment_ids = fields.Many2many("vetapp.treatment")


class AggressiveWizard(models.TransientModel):  # Original Name : vetapp_aggressive_wiz
    _name = "vetapp.aggressive.wiz"

    vet_id = fields.Many2one('res.users', string='Vet')
    notes = fields.Text('Notes')

    def report_aggression(self):
        animals_ids = self.env['vetapp.animals'].browse(self._context.get('active_ids'))
        for animals in animals_ids:
            animals.aggressive = True
            animals.aggressionnotes = self.notes

#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
