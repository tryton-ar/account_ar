# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields, Workflow
from trytond.modules.currency.fields import Monetary
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval


class Line(metaclass=PoolMeta):
    __name__ = 'account.move.line'

    related_statement_line = fields.Many2One('account.statement.line',
        'Statement Line', readonly=True)

    @classmethod
    def __setup__(cls):
        super(Line, cls).__setup__()
        cls._check_modify_exclude.update(['related_statement_line'])


class Statement(metaclass=PoolMeta):
    __name__ = 'account.statement'

    @classmethod
    @Workflow.transition('validated')
    def validate_statement(cls, statements):
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        StatementLine = Pool().get('account.statement.line')

        super(Statement, cls).validate_statement(statements)
        # Remove created draft moves when line is related to move lines
        lines = [l for s in statements for l in s.lines
            if isinstance(l.related_to, MoveLine)]
        StatementLine.delete_move(lines)


class StatementLine(metaclass=PoolMeta):
    __name__ = 'account.statement.line'

    abs_amount = fields.Function(Monetary(
        "Absolute Amount", currency='currency', digits='currency'),
        'on_change_with_abs_amount')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.related_to.domain['account.move.line'] = ['OR',
            [('related_statement_line', '=', Eval('id', -1))],
            [('move.company', '=', Eval('company', -1)),
                ('party', '=', None),
                ('related_statement_line', '=', None),
                ('move.state', 'in', ['posted']),
                ('account', '=', Eval('account', -1)),
                ['OR',
                    ('debit', '=', Eval('abs_amount', 0)),
                    ('credit', '=', Eval('abs_amount', 0))],
            ]]
        cls.related_to.search_order['account.move.line'] = [
            ('debit', 'ASC'),
            ]

    @fields.depends('amount')
    def on_change_with_abs_amount(self, name=None):
        return abs(self.amount)

    @classmethod
    def _get_relations(cls):
        return super()._get_relations() + ['account.move.line']

    @property
    @fields.depends('related_to')
    def move_line(self):
        pool = Pool()
        MoveLine = pool.get('account.move.line')
        related_to = getattr(self, 'related_to', None)
        if isinstance(related_to, MoveLine) and related_to.id >= 0:
            return related_to

    @move_line.setter
    def move_line(self, value):
        self.related_to = value

    @fields.depends('statement', methods=['move_line'])
    def on_change_related_to(self):
        super().on_change_related_to()
        if self.move_line:
            self.account = self.move_line.account

    @classmethod
    def write(cls, *args):
        pool = Pool()
        MoveLine = pool.get('account.move.line')

        actions = iter(args)
        to_update = {}
        for lines, values in zip(actions, actions):
            if 'related_to' in values:
                if values['related_to'] is None:
                    if isinstance(lines[0].related_to, MoveLine):
                        to_update[lines[0].related_to.id] = None
                elif values['related_to'].split(',')[0] == MoveLine.__name__:
                    line_id = int(values['related_to'].split(',')[1])
                    to_update[line_id] = lines[0].id
        super(StatementLine, cls).write(*args)
        cls.update_move_lines(to_update)

    def update_move_lines(to_update):
        pool = Pool()
        MoveLine = pool.get('account.move.line')

        lines = []
        for key in to_update:
            line = MoveLine(key)
            line.related_statement_line = to_update[key]
            lines.append(line)
        MoveLine.save(lines)
