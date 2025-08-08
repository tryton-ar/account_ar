# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import os
import sys
from pyafipws.wsaa import WSAA
from pyafipws.wsfev1 import WSFEv1
from pyafipws.wsfexv1 import WSFEXv1
from proteus import Model

from trytond.modules.company.tests.tools import get_company
from trytond.modules.party_ar.tests.tools import set_afip_certs
from trytond.modules.party_ar.afip import PyAfipWsWrapper

__all__ = ['get_tax', ]


def get_tax(name='IVA Ventas 21%', config=None):
    "Return tax"
    Tax = Model.get('account.tax', config=config)

    tax, = Tax.find([
        ('name', '=', name),
        ])

    return tax


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
