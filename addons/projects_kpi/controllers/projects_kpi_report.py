import io

import xlsxwriter

from odoo import http
from odoo.http import request, content_disposition


class ProjectsKPIReport(http.Controller):
    @http.route('/projects/excel_report/', type='http', auth="user")
    def generate_report(self, **kwargs):
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Projects_KPI_report' + '.xlsx'))
            ]
        )
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        merge_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        sheets = request.env['project.project'].get_report_field()
        for sheet_name in sheets:
            sheet = workbook.add_worksheet(sheet_name)
            col = 0
            for parent_head in sheets[sheet_name]:
                delta = len(sheets[sheet_name][parent_head]) - 1
                text = '' if isinstance(parent_head, int) else parent_head

                sheet.merge_range(0, col, 0, col + delta, text, merge_format)

                for d, child_head in enumerate(sheets[sheet_name][parent_head]):
                    sheet.write(1, col + d, child_head)

                col += delta + 1

            for d, rec in enumerate(request.env['project.project'].get_report_lines()):
                for c in range(len(rec)):
                    sheet.write(2 + d, c, rec[c])

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

        return response
