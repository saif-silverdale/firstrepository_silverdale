from odoo import models, fields, api
import io, base64


class DownloadWizard(models.TransientModel):  # original name : dap_download_wiz
    _name = "dap.download.wiz"

    # get_default
    @api.model
    def default_get(self, fields):
        res = super(DownloadWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    patient_id = fields.Many2one('dap.appointment', string="Patient Name")
    appointment_date = fields.Datetime(related="patient_id.apt_time")
    pat_image = fields.Binary(related="patient_id.pat_image", store=True, readonly=False)
    pat_doc_speciality = fields.Char(related='patient_id.pat_doc_speciality')

    # The below method is for generating pdf report
    def download(self):
        """
        This function generates pdf report whenever the button is pressed
        """
        data = {}  # {'ids': [self.patient_id.id]}
        return self.env.ref('dap.report_dap_appointment').report_action(self.patient_id, data=data)

    # The below method is for generating xlsx report
    def action_generate_xlsx_report(self):
        """
        This function is used for generating report in xls format
        """
        data = {}
        return self.env.ref('dap.report_dap_appointment_excel_wiz').report_action(self, data=data)


class PartnerReportXlsx(models.AbstractModel):
    _name = 'report.dap.generate_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, appointment):

        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})

        for obj in appointment:
            sheet = workbook.add_worksheet("Appointment Report")
            row = 3
            col = 3
            sheet.set_column('D:D', 12)
            sheet.set_column('E:E', 13)

            row += 1
            sheet.merge_range(row, col, row, col+1, 'Patient Card', format_1)

            row += 1
            if obj.pat_image:
                patient_image = io.BytesIO(base64.b64decode(obj.pat_image))
                sheet.insert_image(row, col, "image.png", {'image_data': patient_image, 'x_scale': 0.5, 'y_Scale': 0.5})
                row += 6

            for line in obj.patient_id:
                row += 1
                sheet.write(row, col, 'P.Name', bold)
                sheet.write(row, col + 1, line.animal_id.name)

            row += 1
            sheet.write(row, col, 'Time', bold)
            sheet.write(row, col + 1, obj.appointment_date)
            row += 1
            sheet.write(row, col, 'Doctor Speciality', bold)
            sheet.write(row, col + 1, obj.pat_doc_speciality)

            row += 2
            sheet.merge_range(row, col, row+1, col+1, '', format_1)
