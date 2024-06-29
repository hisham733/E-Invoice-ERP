
frappe.ui.form.on("Sales E Invoice", {
	refresh: function (frm) {
		if (frm.doc.status !== "Submitted") {
			frm.add_custom_button(__("Fetch Sales Invoice Data"), function () {
				
			let d = new frappe.ui.Dialog({
				method: "frappe.client.get_list",

				title: "Select Sales Invoice",
				fields: [
				{
				label: "Sales Invoice",
				fieldname: "sales_invoice",
				fieldtype: "Link",
				options: "Sales Invoice",
				order_by: "modified DESC",
				reqd: 1,
				},
				],
				primary_action_label: "Fetch",
				primary_action(values) {
				frappe.call({
				method:
					"e_invoice_erp.e_invoice_erp.doctype.sales_e_invoice.sales_e_invoice.fetch_sales_invoice_details",
				args: {
					sales_invoice: values.sales_invoice,
				},
				callback: function (r) {
					if (r.message) {
					// customer information
					frm.set_value("naming", r.message.naming);
					frm.set_value("title", r.message.title);
					frm.set_value("customer", r.message.customer);
					frm.set_value("customer_name", r.message.customer_name);
					frm.set_value("customer_tin", r.message.customer_tin);
					frm.set_value("customer_brn", r.message.customer_brn);
					frm.set_value("customer_address", r.message.customer_address);
					frm.set_value("tax_id", r.message.tax_id);
					frm.set_value("is_pos", r.message.is_pos);
					frm.set_value("pos_profile", r.message.pos_profile);
		
					// INVOICE INFORMATION
					//   frm.set_value("naming_series", r.message.naming_series);
					frm.set_value("posting_date", r.message.posting_date);
					frm.set_value("posting_time", r.message.posting_time);
					frm.set_value(
					"e_invoice_type_code",
					r.message.e_invoice_type_code
					);
					frm.set_value(
					"additional_document_reference",
					r.message.additional_document_reference
					);
		
					//Supplier information
					frm.set_value("company", r.message.company);
					frm.set_value("msic_codes", r.message.msic_codes);
					frm.set_value("registration_name", r.message.registration_name);
					frm.set_value(
					"registration_full_name",
					r.message.registration_full_name
					);
					frm.set_value("supplier_tin", r.message.supplier_tin);
					frm.set_value("supplier_brn", r.message.supplier_brn);
					frm.set_value(
					"tourism_tax_registration",
					r.message.tourism_tax_registration
					);
					frm.set_value(
					"supplier_address_name",
					r.message.supplier_address_name
					);
					frm.set_value("description", r.message.description);
		
					// fetch items
					if (r.message.items && r.message.items.length > 0) {
					frm.clear_table("items");
					r.message.items.forEach(function (item, index) {
						let row = frm.add_child("items");
						frappe.model.set_value(
						row.doctype,
						row.name,
						"barcode",
						item.barcode
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"item_code",
						item.item_code
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"col_break1",
						item.col_break1
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"item_name",
						item.item_name
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"customer_item_code",
						item.customer_item_code
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"description_section",
						item.description_section
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"description",
						item.description
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"item_group",
						item.item_group
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"brand",
						item.brand
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"image_section",
						item.image_section
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"image",
						item.image
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"image_view",
						item.image_view
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"quantity_and_rate",
						item.quantity_and_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"qty",
						item.qty
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"stock_uom",
						item.stock_uom
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"col_break2",
						item.col_break2
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"uom",
						item.uom
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"conversion_factor",
						item.conversion_factor
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"stock_qty",
						item.stock_qty
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"section_break_17",
						item.section_break_17
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"price_list_rate",
						item.price_list_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_price_list_rate",
						item.base_price_list_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"discount_and_margin",
						item.discount_and_margin
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"margin_type",
						item.margin_type
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"margin_rate_or_amount",
						item.margin_rate_or_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"rate_with_margin",
						item.rate_with_margin
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"column_break_19",
						item.column_break_19
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"discount_percentage",
						item.discount_percentage
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"discount_amount",
						item.discount_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_rate_with_margin",
						item.base_rate_with_margin
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"section_break1",
						item.section_break1
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"rate",
						item.rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"amount",
						item.amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"item_tax_template",
						item.item_tax_template
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"col_break3",
						item.col_break3
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_rate",
						item.base_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_amount",
						item.base_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"pricing_rules",
						item.pricing_rules
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"is_free_item",
						item.is_free_item
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"section_break_21",
						item.section_break_21
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"net_rate",
						item.net_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"net_amount",
						item.net_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"column_break_24",
						item.column_break_24
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_net_rate",
						item.base_net_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_net_amount",
						item.base_net_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"drop_ship",
						item.drop_ship
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"delivered_by_supplier",
						item.delivered_by_supplier
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"accounting",
						item.accounting
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"income_account",
						item.income_account
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"is_fixed_asset",
						item.is_fixed_asset
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"asset",
						item.asset
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"finance_book",
						item.finance_book
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"col_break4",
						item.col_break4
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"expense_account",
						item.expense_account
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"deferred_revenue",
						item.deferred_revenue
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"deferred_revenue_account",
						item.deferred_revenue_account
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"service_stop_date",
						item.service_stop_date
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"enable_deferred_revenue",
						item.enable_deferred_revenue
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"column_break_50",
						item.column_break_50
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"service_start_date",
						item.service_start_date
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"service_end_date",
						item.service_end_date
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"section_break_18",
						item.section_break_18
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"weight_per_unit",
						item.weight_per_unit
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"total_weight",
						item.total_weight
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"column_break_21",
						item.column_break_21
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"weight_uom",
						item.weight_uom
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"warehouse_and_reference",
						item.warehouse_and_reference
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"warehouse",
						item.warehouse
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"target_warehouse",
						item.target_warehouse
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"quality_inspection",
						item.quality_inspection
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"batch_no",
						item.batch_no
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"col_break5",
						item.col_break5
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"allow_zero_valuation_rate",
						item.allow_zero_valuation_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"item_tax_rate",
						item.item_tax_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"actual_batch_qty",
						item.actual_batch_qty
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"actual_qty",
						item.actual_qty
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"edit_references",
						item.edit_references
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"sales_order",
						item.sales_order
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"so_detail",
						item.so_detail
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"sales_invoice_item",
						item.sales_invoice_item
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"column_break_74",
						item.column_break_74
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"delivery_note",
						item.delivery_note
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"dn_detail",
						item.dn_detail
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"delivered_qty",
						item.delivered_qty
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"accounting_dimensions_section",
						item.accounting_dimensions_section
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"cost_center",
						item.cost_center
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"dimension_col_break",
						item.dimension_col_break
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"project",
						item.project
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"section_break_54",
						item.section_break_54
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"page_break",
						item.page_break
						);
						frappe.model.set_value(
							row.doctype,
							row.name,
							"classification_codes",
							item.classification_codes
						);
						frappe.model.set_value(
							row.doctype,
							row.name,
							"total_amount_before_discount",
							item.total_amount_before_discount
						);
					});
					frm.refresh_field("items");
					}
		
					// Totals
					frm.set_value("total_qty", r.message.total_qty);
					frm.set_value("base_total", r.message.base_total);
					frm.set_value("base_net_total", r.message.base_net_total);
					frm.set_value("total_net_weight", r.message.total_net_weight);
					frm.set_value("total", r.message.total);
					frm.set_value("net_total", r.message.net_total);
					frm.set_value(
					"base_total_taxes_and_charges",
					r.message.base_total_taxes_and_charges
					);
					frm.set_value(
					"total_taxes_and_charges",
					r.message.total_taxes_and_charges
					);
					frm.set_value("loyalty_points", r.message.loyalty_points);
					frm.set_value("loyalty_amount", r.message.loyalty_amount);
					frm.set_value(
					"redeem_loyalty_points",
					r.message.redeem_loyalty_points
					);
					frm.set_value("loyalty_program", r.message.loyalty_program);
					frm.set_value(
					"loyalty_redemption_account",
					r.message.loyalty_redemption_account
					);
					frm.set_value(
					"loyalty_redemption_cost_center",
					r.message.loyalty_redemption_cost_center
					);
					frm.set_value("apply_discount_on", r.message.apply_discount_on);
					frm.set_value(
					"base_discount_amount",
					r.message.base_discount_amount
					);
					frm.set_value(
					"additional_discount_percentage",
					r.message.additional_discount_percentage
					);
					frm.set_value("discount_amount", r.message.discount_amount);
					frm.set_value("base_grand_total", r.message.base_grand_total);
					frm.set_value(
					"base_rounding_adjustment",
					r.message.base_rounding_adjustment
					);
					frm.set_value(
					"base_rounded_total",
					r.message.base_rounded_total
					);
					frm.set_value("base_in_words", r.message.base_in_words);
					frm.set_value("grand_total", r.message.grand_total);
					frm.set_value(
					"rounding_adjustment",
					r.message.rounding_adjustment
					);
					frm.set_value("rounded_total", r.message.rounded_total);
					frm.set_value("in_words", r.message.in_words);
					frm.set_value("total_advance", r.message.total_advance);
					frm.set_value(
					"outstanding_amount",
					r.message.outstanding_amount
					);
					frm.set_value("debit_to", r.message.debit_to);
					
					frm.set_value("other_charges_calculation", r.message.other_charges_calculation);
					frm.set_value("tax_category", r.message.tax_category);

					if (r.message.taxes && r.message.taxes.length > 0) {
					frm.clear_table("taxes");
					r.message.taxes.forEach(function (tax, index) {
						let row = frm.add_child("taxes");
						frappe.model.set_value(
						row.doctype,
						row.name,
						"charge_type",
						tax.charge_type
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"row_id",
						tax.row_id
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"account_head",
						tax.account_head
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"description",
						tax.description
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"included_in_print_rate",
						tax.included_in_print_rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"cost_center",
						tax.cost_center
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"rate",
						tax.rate
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"tax_amount",
						tax.tax_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"total",
						tax.total
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"tax_amount_after_discount_amount",
						tax.tax_amount_after_discount_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_tax_amount",
						tax.base_tax_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_total",
						tax.base_total
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"base_tax_amount_after_discount_amount",
						tax.base_tax_amount_after_discount_amount
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"item_wise_tax_detail",
						tax.item_wise_tax_detail
						);
						frappe.model.set_value(
						row.doctype,
						row.name,
						"parenttype",
						tax.parenttype
						);
					});
					frm.refresh_field("taxes");
					}
		
					// Set other necessary fields
					// ...
					frappe.msgprint(__("Sales Invoice data fetched successfully."));
					console.log("Sending Document Info Data:", {
					address_line1: r.message.address_line1,
					items: r.message.items,
					classification_table: r.message.classification_table,
					});
					}
				},
				});
				d.hide();
				},
			});
			d.show();
			});
			
			}
		}
	});
		