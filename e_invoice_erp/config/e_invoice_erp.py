from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Core Entities"),
			"items": [

				{
					"type": "doctype",
					"name": "Item",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Customer",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Supplier",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Address",
					"onboard": 1,

				},

			]
		},

		{
			"label": _("Sales Workflow"),
			"items": [

				{
					"type": "doctype",
					"name": "Quotation",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Sales Order",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"onboard": 1,

				},

			]
		},
				{
			"label": _("E-Invoice Operations"),
			"items": [

				{
					"type": "doctype",
					"name": "Sales E Invoice",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Get Document Info",
					"onboard": 1,

				},
				{
					"type": "doctype",
					"name": "Cancel Document",
					"onboard": 1,

				},

			]
		},
		
		
	]
	
	