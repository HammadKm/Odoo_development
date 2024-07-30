# -*- coding: utf-8 -*-
from odoo import Command
from odoo.http import request, Controller, route


class WebFormController(Controller):
    @route('/material_request', auth='public', website=True)
    def material_request(self):
        products = request.env['product.product'].sudo().search([])
        customer = request.env['res.users'].sudo().search([])
        location = request.env['stock.location'].sudo().search([])
        datas = {
            'products': products,
            'customer': customer,
            'location': location,
        }

        return request.render('material_request.web_machine_request_template',
                              datas)

    @route('/material/submit', type='json', auth='public', website=True, )
    def request_submit(self, **post):
        order = []
        for recs in post['data']:
            if recs['operation'] == 'purchase order':
                dicts = {'product_id': int(recs.get('material')),
                         'material_qty': int(recs.get('quantity')),
                         'operation_type': recs.get('operation')}
            else:
                dicts = {'product_id': int(recs.get('material')),
                         'material_qty': int(recs.get('quantity')),
                         'operation_type': recs.get('operation'),
                         'src_location_id': int(recs.get('source')),
                         'dest_location_id': int(recs.get('destination'))
                         }
            order.append(dicts)
        record = request.env['material.request'].sudo().create({
            'employee_id': int(post.get('partner')),
            'date': post.get('date'),
            'material_order_ids': [Command.create(rec) for rec in order],
        })
        record.state = 'submitted'
        user = request.env['res.users'].sudo().browse(int(post.get('partner')))
        print(record.reference_no)
        if user.email:
            template = request.env.ref(
                'material_request.material_mail_template')
            template.send_mail(record.id, force_send=True)

        return record.reference_no

    @route('/thank-you/<string:ref>', auth='public', website=True, type='http')
    def thank_form(self, ref):
        print(ref)
        # material = request.env['material.request'].sudo().search_read([], [
        #     'reference_no'], order='create_date DESC', limit=1)
        # print(material)
        data = {
            'sequence': ref
        }

        return request.render('material_request.web_thank_template', data)
