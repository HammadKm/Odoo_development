# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.sql_db import _logger
import cachetools
# Initialize a TTL cache with a maximum size of 100 items and a
# time-to-live of 120 seconds
cache = cachetools.TTLCache(maxsize=100, ttl=120)


class PdfContent(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _run_wkhtmltopdf(
            self,
            bodies,
            report_ref=False,
            header=None,
            footer=None,
            landscape=False,
            specific_paperformat_args=None,
            set_viewport_size=False):
        """
           Generates a PDF from the given HTML bodies using wkhtmltopdf.

           This method attempts to retrieve the result from a cache before
           performing the PDF generation. If the result is not found in the cache,
           it will generate the PDF and store the result in the cache for future
           use.

           :param bodies: HTML content to be converted into PDF.
           :param report_ref: Optional report reference.
           :param header: Optional header content.
           :param footer: Optional footer content.
           :param landscape: Boolean indicating if the PDF should be in landscape orientation.
           :param specific_paperformat_args: Optional arguments for specific paper formatting.
           :param set_viewport_size: Boolean indicating if the viewport size should be set.
           :return: The generated PDF content.
       """
        cache_result = False
        cache_key = f"{bodies}"
        if cache_key:
            cache_result = cache.get(cache_key)
        if cache_result:
            return cache_result
        else:
            result = super()._run_wkhtmltopdf(bodies,
                                              report_ref=report_ref,
                                              header=header,
                                              footer=footer,
                                              landscape=landscape,
                                              specific_paperformat_args=specific_paperformat_args,
                                              set_viewport_size=set_viewport_size)
            cache[cache_key] = result
            return result