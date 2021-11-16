# -*- coding: utf-8 -*-
# from odoo import http


# class Uninstall(http.Controller):
#     @http.route('/uninstall/uninstall/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uninstall/uninstall/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('uninstall.listing', {
#             'root': '/uninstall/uninstall',
#             'objects': http.request.env['uninstall.uninstall'].search([]),
#         })

#     @http.route('/uninstall/uninstall/objects/<model("uninstall.uninstall"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uninstall.object', {
#             'object': obj
#         })
