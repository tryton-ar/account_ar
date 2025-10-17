# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.transaction import Transaction


class BalanceDeferralStart(ModelView):
    'Balance Deferral'
    __name__ = 'account.fiscalyear.balance_deferral.start'

    fiscalyear = fields.Many2One('account.fiscalyear', 'Fiscal Year',
        required=True, domain=[('state', '=', 'open')])
    company = fields.Function(fields.Many2One('company.company', 'Company'),
        'on_change_with_company')
    journal = fields.Many2One('account.journal', 'Journal', required=True,
        domain=[
            ('type', '=', 'situation'),
            ],
        context={
            'company': Eval('company', -1),
            },
        depends={'company'})
    period = fields.Many2One('account.period', 'Period', required=True,
        domain=[
            ('fiscalyear', '=', Eval('fiscalyear')),
            ('type', '=', 'adjustment'),
            ])

    @fields.depends('fiscalyear')
    def on_change_with_company(self, name=None):
        return self.fiscalyear.company if self.fiscalyear else None


class BalanceDeferral(Wizard):
    'Balance Deferral'
    __name__ = 'account.fiscalyear.balance_deferral'

    start = StateView('account.fiscalyear.balance_deferral.start',
        'account_ar.fiscalyear_balance_deferral_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('OK', 'balance', 'tryton-ok', default=True),
            ])
    balance = StateAction('account.act_move_form')

    def get_move_line(self, account):
        pool = Pool()
        Line = pool.get('account.move.line')

        balance = account.balance
        if account.company.currency.is_zero(balance):
            return
        line = Line()
        line.account = account
        if balance >= 0:
            line.credit = abs(balance)
            line.debit = 0
        else:
            line.credit = 0
            line.debit = abs(balance)
        return line

    def create_move(self):
        pool = Pool()
        Account = pool.get('account.account')
        Move = pool.get('account.move')

        with Transaction().set_context(fiscalyear=self.start.fiscalyear.id,
                date=None, cumulate=True, journal=None):
            accounts = Account.search([
                    ('company', '=', self.start.fiscalyear.company.id),
                    ('deferral', '=', True),
                    ('type', '!=', None),
                    ('closed', '!=', True),
                    ])
        lines = []
        for account in accounts:
            line = self.get_move_line(account)
            if line:
                lines.append(line)
        if not lines:
            return
        amount = sum(l.debit - l.credit for l in lines)
        if not self.start.fiscalyear.company.currency.is_zero(amount):
            return None
        move = Move()
        move.period = self.start.period
        move.journal = self.start.journal
        move.date = self.start.period.end_date
        move.origin = self.start.fiscalyear
        move.company = self.start.fiscalyear.company
        move.lines = lines
        move.save()
        return move

    def do_balance(self, action):
        move = self.create_move()
        if move:
            action['views'].reverse()
        return action, {'res_id': move.id if move else None}
