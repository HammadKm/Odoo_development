# -*- coding: utf-8 -*-

from odoo import fields, models
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError


class ImportOrderLine(models.TransientModel):
    _name = "import.order.line"
    _description = "Import Order Line"

    file_name = fields.Binary(string="File", required=True)
    orders_id = fields.Many2one('sale.order', string="Order")

    def action_import_order(self):
        try:
            book = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file_name)),
                read_only=True)
            sheet = book.active
            for record in sheet.iter_rows(min_row=2, max_row=None, min_col=None,
                                          max_col=None, values_only=True):
                if not self.env['product.product'].search(
                        [('name', '=', record[0])]):
                    self.env['product.product'].create({
                        'name': record[0],
                        'lst_price': record[4]
                    })

                sale_order_line = [fields.Command.create({
                    'order_id': self.orders_id.id,
                    'product_id': self.env['product.product'].search(
                        [('name', '=', record[0])]).id,
                    'name': record[1] if record[1] else self.env[
                        'product.product'].search(
                        [('name', '=', record[0])]).name,
                    'product_uom': self.env['uom.uom'].search(
                        [('name', '=', record[2])]).id or 1,
                    'product_uom_qty': record[3] or 1,
                    'price_unit': record[4] if record[4] else
                    self.env['product.product'].search(
                        [('name', '=', record[0])])[
                        0].lst_price,
                    'customer_lead': 4

                })]
                self.orders_id.update({
                    'order_line': sale_order_line
                })
        except:
            raise UserError('Please insert a valid file')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def import_order_line_btn(self):
        return {
            'name': 'Import Order Line Wizard',
            'res_model': 'import.order.line',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new'
        }
