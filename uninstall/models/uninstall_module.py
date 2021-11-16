from odoo import models, fields, api


class Module(models.Model):
    _inherit = 'ir.module.module'

    def action_uninstall(self):
        var = self.browse(self.env.context.get('active_ids')).button_immediate_uninstall()
        print(var)
