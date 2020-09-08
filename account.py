# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool


class TaxGroup(metaclass=PoolMeta):
    __name__ = 'account.tax.group'

    tribute_id = fields.Char("Tribute ID",
        states={
            'invisible': Eval('afip_kind') == 'gravado',
            'required': Eval('afip_kind') != 'gravado',
            },
        depends=['afip_kind'])
    afip_kind = fields.Selection([
        ('gravado', 'Gravado'),
        ('nacional', 'Nacional'),
        ('provincial', 'Provincial'),
        ('municipal', 'Municipal'),
        ('interno', 'Interno'),
        ('other', 'Other'),
        ], 'AFIP Kind', required=True, sort=False)


class TaxTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.template'

    iva_code = fields.Char("IVA Code")

    def _get_tax_value(self, tax=None):
        value = super()._get_tax_value(tax=tax)
        if not tax or tax.iva_code != self.iva_code:
            value['iva_code'] = self.iva_code
        return value


class Tax(metaclass=PoolMeta):
    __name__ = 'account.tax'

    iva_code = fields.Char("IVA Code",
        states={
            'readonly': (Bool(Eval('template', -1))
                & ~Eval('template_override', False)),
            },
        depends=['template', 'template_override'])

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.group.required = True
