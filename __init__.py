#This file is part of the account_ar module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

from trytond.pool import Pool
from .account_ar import *


def register():
    Pool.register(
        PrintChartAccountStart,
        module='account_ar', type_='model')
    Pool.register(
        PrintChartAccount,
        module='account_ar', type_='wizard')
    Pool.register(
        ChartAccount,
        module='account_ar', type_='report')
