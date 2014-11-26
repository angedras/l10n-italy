# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#    Copyright 2014 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################
from openerp.osv import orm


class ResPartner(orm.Model):

    # inherit partner because PEC mails are not supposed to be associate to
    # generic models
    _inherit = "res.partner"

    def message_post(
        self, cr, uid, thread_id, body='', subject=None, type='notification',
        subtype=None, parent_id=False, attachments=None, context=None,
        content_subtype='html', **kwargs
    ):
        if context is None:
            context = {}
        import pdb; pdb.set_trace()
        message_pool = self.pool['mail.message']
        msg_id = super(ResPartner, self).message_post(
            cr, uid, thread_id, body=body, subject=subject, type=type,
            subtype=subtype, parent_id=parent_id, attachments=attachments,
            context=context, content_subtype=content_subtype, **kwargs)
        if context.get('main_message_id') and context.get('pec_type'):
            if context['pec_type'] == 'accettazione':
                message_pool.write(
                    cr, uid, [context['main_message_id']], {
                        'reception_message_id': msg_id,
                    }, context=context)
            if context['pec_type'] == 'avvenuta-consegna':
                message_pool.write(
                    cr, uid, [context['main_message_id']], {
                        'delivery_message_id': msg_id,
                    }, context=context)
        return msg_id
