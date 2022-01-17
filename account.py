# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields, Unique
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Bool
from trytond.transaction import Transaction


class TaxGroup(metaclass=PoolMeta):
    __name__ = 'account.tax.group'

    tribute_id = fields.Char("Tribute ID",
        states={
            'invisible': Eval('afip_kind').in_([
                'gravado', 'no_gravado', 'exento']),
            'required': ~Eval('afip_kind').in_([
                'gravado', 'no_gravado', 'exento']),
            },
        depends=['afip_kind'])
    afip_kind = fields.Selection([
        ('gravado', 'Gravado'),
        ('no_gravado', 'No gravado'),
        ('exento', 'Exento'),
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


class Account(metaclass=PoolMeta):
    __name__ = 'account.account'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        t = cls.__table__()
        cursor = Transaction().connection.cursor()
        cursor.execute('SELECT code '
            'FROM "' + cls._table + '" '
            'GROUP BY code '
            'HAVING COUNT(*) > 1')
        if not cursor.fetchall():
            cls._sql_constraints += [
                ('company_code_uniq', Unique(t, t.company, t.code),
                    'account_ar.msg_account_company_code_unique'),
                ]

    @classmethod
    def copy(cls, records, default=None):
        if default is None:
            default = {}
        current_default = default.copy()

        new_records = []
        for record in records:
            current_default['code'] = '%s (copy)' % record.code
            new_record, = super().copy([record], default=current_default)
            new_records.append(new_record)
        return new_records
