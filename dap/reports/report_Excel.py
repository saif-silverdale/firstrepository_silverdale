from odoo import models
import io,base64

class PartnerReportXlsx(models.AbstractModel):
    _name = 'report.dap.report_appointment_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, appointment):

        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True,'align':'center','bg_color':'yellow'})

        for obj in appointment:
            sheet = workbook.add_worksheet("Appointment Report")
            row = 3
            col = 3
            sheet.set_column('D:D',12)
            sheet.set_column('E:E',13)

            row+=1
            sheet.merge_range(row,col,row,col+1,'Patient Card',format_1)

            row+=1
            if obj.pat_image:
                patient_image=io.BytesIO(base64.b64decode(obj.pat_image))
                sheet.insert_image(row,col,"image.png",{'image_data':patient_image,'x_scale':0.5,'y_Scale':0.5})
                row +=6

            for line in obj.animal_id:
                row +=1
                sheet.write(row, col, 'P.Name', bold)
                sheet.write(row, col + 1, line.name)

            row +=1
            sheet.write(row, col, 'Time', bold)
            sheet.write(row, col + 1, obj.apt_time)
            row +=1
            sheet.write(row, col, 'Doctor Speciality', bold)
            sheet.write(row, col + 1, obj.pat_doc_speciality)

            row+=2
            sheet.merge_range(row,col,row+1,col+1,'',format_1)
