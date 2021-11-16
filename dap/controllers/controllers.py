# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Dap(http.Controller):

    @http.route('/dap/dap/newcustom', auth='public', website=True)
    def index1(self, **kw):
        try:
            sales_orders = http.request.env['sale.order'].search([])
        except:
            return "<h1>Can't Access API</h1>"
        return http.request.render('dap.index2', {'sales2': sales_orders, })
        # output = "<h1>:::Sales Orders:::</h1><ul>"
        # for sale in sales_orders:
        #     output += "<li>"+sale['name']+"</li>"
        # output += "</ul>"
        # return output

    @http.route('/dap/dap/', auth='public', website=True)
    def index(self, **kw):
        # return "Hello, world"
        tests = request.env['dap.testsecurity'].sudo().search([])
        return request.render("dap.patients_page", {'tests': tests})

    @http.route('/dap/dap/custom1', auth='user', website=True)
    def __index__(self, **kw):
        try:
            sales_orders = http.request.env['sale.order'].search([])
        except:
            return "<h1>Can't Access API</h1>"

        return http.request.render('dap.index', {'sales': sales_orders, })

    @http.route('/dap/dap/<model("sale.order"):so>/', auth='public', website=True)
    def displaysalesorder(self, so):
        return http.request.render('dap.sales_order', {'saleorder': so, })

#     @http.route('/dap/dap/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dap.listing', {
#             'root': '/dap/dap',
#             'objects': http.request.env['dap.dap'].search([]),
#         })

#     @http.route('/dap/dap/objects/<model("dap.dap"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dap.object', {
#             'object': obj
#         })
