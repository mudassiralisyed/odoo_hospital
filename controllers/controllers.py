# -*- coding: utf-8 -*-
from odoo import http

# class LearningHospital(http.Controller):
#     @http.route('/learning_hospital/learning_hospital/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/learning_hospital/learning_hospital/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('learning_hospital.listing', {
#             'root': '/learning_hospital/learning_hospital',
#             'objects': http.request.env['learning_hospital.learning_hospital'].search([]),
#         })

#     @http.route('/learning_hospital/learning_hospital/objects/<model("learning_hospital.learning_hospital"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('learning_hospital.object', {
#             'object': obj
#         })