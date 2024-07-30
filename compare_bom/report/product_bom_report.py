# -*- coding: utf-8 -*-

from odoo import models, api


class BomReport(models.AbstractModel):
    _name = "report.compare_bom.report_bom"

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'data': data,
        }
