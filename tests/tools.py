# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from proteus import Model


__all__ = ['get_tax', 'get_tax_group']


def get_tax(name='IVA Ventas 21%', config=None):
    "Return tax"
    Tax = Model.get('account.tax', config=config)

    tax, = Tax.find([
        ('name', '=', name),
        ])

    return tax


def get_tax_group(code='IVA', kind='sale', afip_kind='gravado', config=None):
    "Return tax group"
    TaxGroup = Model.get('account.tax.group', config=config)

    group, = TaxGroup.find([
        ('code', '=', code),
        ('kind', '=', kind),
        ('afip_kind', '=', afip_kind),
        ])

    return group


def get_accounts(company, config=None):
    "Return accounts per kind"
    Account = Model.get('account.account', config=config)

    accounts = {}
    accounts['receivable'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'Deudores por ventas'),
        ('closed', '!=', True),
        ], limit=1)
    accounts['payable'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'Proveedores'),
        ('closed', '!=', True),
        ], limit=1)
    accounts['revenue'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'Ingresos por ventas'),
        ('closed', '!=', True),
        ], limit=1)
    accounts['expense'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'Gastos operativos general'),
        ('closed', '!=', True),
        ], limit=1)
    accounts['cash'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'Caja pesos'),
        ('closed', '!=', True),
        ], limit=1)
    accounts['sale_tax'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'IVA débito fiscal'),
        ('closed', '!=', True),
        ], limit=1)
    accounts['purchase_tax'], = Account.find([
        ('company', '=', company.id),
        ('name', '=', 'IVA crédito fiscal'),
        ('closed', '!=', True),
        ], limit=1)

    return accounts
