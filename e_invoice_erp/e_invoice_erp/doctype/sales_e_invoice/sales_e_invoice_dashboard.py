from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		'fieldname': 'sales_e_invoice',
		'non_standard_fieldnames': {
			'Get Document Info': 'sales_e_invoice',
			'Cancel Document': 'sales_e_invoice'

		},

		'transactions': [
			{
				'label': _('Get E Invoice Document'),
				'items': ['Get Document Info']
			},
						{
				'label': _('Cancel E Invoce'),
				'items': ['Cancel Document']
			},
			
		]
	}

      