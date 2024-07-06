# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeLevel(models.Model):
    _name = "employee.level"
    _description = "Employee Level"
    _rec_name = "emp_level"

    # name = fields.Char(string='Name', reqiured=True)
    emp_level = fields.Char(string='Employee Level')
    salary = fields.Float(string='Salary')
    highest_level = fields.Boolean(string='Is Highest')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_level_id = fields.Many2one('employee.level', string='Employee Level', )
    salary = fields.Float(string='Salary', related='emp_level_id.salary')
    h_level = fields.Boolean(string='High',related='emp_level_id.highest_level')

    def promote_salary_btn(self):
        # print(self.emp_level_id)
        levels = self.env['employee.level'].search([])
        # print(levels)
        for rec in enumerate(levels):
            print(rec)
            if self.emp_level_id.id == rec[1].id and self.emp_level_id.highest_level != True:
                # print(self.env['employee.level'].browse(rec[1].id + 1))
                self.emp_level_id = rec[1].id+1
                break

                # print()

            #     print('hello')

        print('hello')

#
