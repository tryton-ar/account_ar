# This file is part of the account_ar module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.i18n import gettext
from trytond.model.exceptions import AccessError


class Line(metaclass=PoolMeta):
    __name__ = 'account.move.line'

    @fields.depends('move_origin')
    def on_change_with_party_required(self, name=None):
        if self.move_origin:
            model = str(self.move_origin)
            origin = model[:model.find(',')]
            if origin == 'account.fiscalyear':
                return False
        return super().on_change_with_party_required()

    @classmethod
    def check_account(cls, lines, field_names=None):
        if field_names and not (field_names & {'account', 'party'}):
            return
        for line in lines:
            if not line.account.type or line.account.closed:
                raise AccessError(
                    gettext('account.msg_line_closed_account',
                        account=line.account.rec_name))
            if bool(line.party) != bool(line.party_required):
                error = 'party_set' if line.party else 'party_required'
                raise AccessError(
                    gettext('account.msg_line_%s' % error,
                        account=line.account.rec_name,
                        line=line.rec_name))
