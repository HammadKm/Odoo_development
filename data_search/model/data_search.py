# -*- coding: utf-8 -*-

from odoo import fields, models, api


class DataSearch(models.Model):
    _name = "data.search"
    _description = "Data Search"
    _rec_name = "search"

    search = fields.Char(string='Search')
    models_ids = fields.Many2many('ir.model', string='Model', )
    field_id = fields.Many2one('ir.model.fields', string='fields', domain="[('ttype','!=','boolean')]")

    @api.model
    def get_values(self):
        if self.models_ids:
            self.update({
                'model_ids': [(fields.Command.set())]
            })

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(DataSearch, self).create(vals_list)
    #     search_index = self.env['data.search'].search_count(
    #         [('user_id', '=', self.env.user.id)])
    #     if search_index > 10:
    #         last_search = self.env['data.search'].search(
    #             [('id', '!=', res.id), ('user_id', '=', self.env.user.id)],
    #             order="create_date asc", limit=1)
    #         last_search.unlink() if last_search else False
    #     return res

    def action_search(self):
        print(self.models_ids.model)
        val = self.models_ids.read()
        print(val[0]['model'])
        data = self.env[val[0]['model']].search([])
        print(data)
        # self.update()
        print(val, 'hi')
        active_qry = """ and obj.active in ({},{}) 
                    """.format("'FALSE'", "'TRUE'")
        print(active_qry)

    def action_clear_search(self):
        self.search = ""
        print('helo')

    # def _search_query(self, key):
    #     """ search for the model with given key and update result """
    #     company_id = self.env.user.company_id.id
    #     active_qry = """ and obj.active in ({},{})
    #         """.format("'FALSE'", "'TRUE'")
    #     print()




# def action_unlink_search(self):
#     print('dadgfd')
