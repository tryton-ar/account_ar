# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import account
from . import statement

__all__ = ['register']


def register():
    Pool.register(
        account.TaxTemplate,
        account.Tax,
        account.TaxGroup,
        account.Account,
        module='account_ar', type_='model')
    Pool.register(
        statement.Line,
        statement.Statement,
        statement.StatementLine,
        module='account_ar', type_='model',
        depends=['account_statement'])
