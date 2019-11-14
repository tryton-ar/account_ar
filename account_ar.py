# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from datetime import datetime

from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.report import Report
from trytond.transaction import Transaction
from trytond.pyson import Eval, Bool
from trytond.pool import PoolMeta, Pool

__all__ = ['PrintChartAccountStart', 'PrintChartAccount', 'ChartAccount',
    'TaxTemplate', 'Tax', 'TaxGroup']

AFIP_KINDS = [
    ('gravado', 'Gravado'),
    ('nacional', 'Nacional'),
    ('provincial', 'Provincial'),
    ('municipal', 'Municipal'),
    ('interno', 'Interno'),
    ('other', 'Other'),
    ]


class TaxGroup(metaclass=PoolMeta):
    __name__ = 'account.tax.group'

    tribute_id = fields.Char("Tribute ID", states={
            'invisible': Eval('afip_kind') == 'gravado',
            'required': Eval('afip_kind') != 'gravado',
            })
    afip_kind = fields.Selection(AFIP_KINDS, 'AFIP Kind', required=True)


class TaxTemplate(metaclass=PoolMeta):
    __name__ = 'account.tax.template'

    iva_code = fields.Char("IVA Code")

    def _get_tax_value(self, tax=None):
        value = super(TaxTemplate, self)._get_tax_value(tax=tax)
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
        super(Tax, cls).__setup__()
        cls.group.required = True


class PrintChartAccountStart(ModelView):
    'Print Chart Account'
    __name__ = 'account.print_chart_account.start'
    company = fields.Many2One('company.company', 'Company', required=True)

    @staticmethod
    def default_company():
        return Transaction().context.get('company')


class PrintChartAccount(Wizard):
    'Print Chart Account'
    __name__ = 'account.print_chart_account'
    start = StateView('account.print_chart_account.start',
        'account_ar.print_chart_account_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Print', 'print_', 'tryton-print', default=True),
            ])
    print_ = StateAction('account_ar.report_chart_account')

    def do_print_(self, action):
        data = {
            'company': self.start.company.id,
            }
        return action, data

    def transition_print_(self):
        return 'end'


class ChartAccount(Report):
    __name__ = 'account.chart_account'

    @classmethod
    def _compute_level(cls, account):
        if not account.parent:
            return 0
        return 1 + cls._compute_level(account.parent)

    @classmethod
    def get_context(cls, records, data):
        pool = Pool()
        Account = pool.get('account.account')
        Company = pool.get('company.company')
        report_context = super(ChartAccount, cls).get_context(records, data)

        company = Company(data['company'])

        accounts = Account.search([
                ('company', '=', data['company']),
                ])

        report_accounts = []
        for account in accounts:
            report_accounts.append({
                    'code': account.code,
                    'name': account.name,
                    'level': cls._compute_level(account),
                    })

        report_context['accounts'] = report_accounts
        report_context['company'] = company
        report_context['time'] = datetime.now()
        return report_context
