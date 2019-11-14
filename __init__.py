# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import account_ar


def register():
    Pool.register(
        account_ar.PrintChartAccountStart,
        account_ar.TaxTemplate,
        account_ar.Tax,
        account_ar.TaxGroup,
        module='account_ar', type_='model')
    Pool.register(
        account_ar.PrintChartAccount,
        module='account_ar', type_='wizard')
    Pool.register(
        account_ar.ChartAccount,
        module='account_ar', type_='report')
