# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from datetime import datetime

from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.report import Report
from trytond.transaction import Transaction
from trytond.pool import Pool

__all__ = ['PrintChartAccountStart', 'PrintChartAccount', 'ChartAccount']


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
