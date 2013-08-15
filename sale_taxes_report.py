# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp import tools

class sale_taxes_report(osv.osv):
    _name = "account.saletaxes.report"
    _description = "Account Sale Taxes Report"
    _auto = False
    _columns = {
		'invoice_name': fields.char('Invoice Name',size=64),
		'invoice_date': fields.date('Invoice Date'),
		'journal_name': fields.char('Journal Name',size=64),
		'customer_name': fields.char('Customer Name',size=64),
		'customer_vat': fields.char('Customer VAT',size=64),
		'tax_name': fields.char('Tax Name',size=64),
		'tax_amount': fields.float('Tax Amount'),
		'amount_untaxed': fields.float('Amount Untaxed'),
		'amount_total': fields.float('Amount Total')
		}

    def init(self, cr):
        """
        Initialize the sql view for the event registration
        """
        tools.drop_view_if_exists(cr, 'account_saletaxes_report')

        # TOFIX this request won't select events that have no registration
        cr.execute(""" CREATE VIEW account_saletaxes_report AS (
		select e.name as invoice_name,e.date_invoice as date_invoice,g.name as journal_name, 
		f.name as customer_name,f.vat as CUIT,b.name as tax_name,a.tax_amount as tax_amount,
		e.amount_untaxed as amount_untaxed,e.amount_total as amount_total
		from account_invoice_tax a inner join account_tax_code b on a.tax_code_id = b.id
		inner join account_invoice e on e.id = a.invoice_id
		inner join res_partner f on f.id = e.partner_id
		inner join account_journal g on g.id = e.journal_id)""")

sale_taxes_report()
