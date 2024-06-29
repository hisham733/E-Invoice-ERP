# -*- coding: utf-8 -*-
# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import logging
# import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
import frappe
import base64
import hashlib
import json
import logging
from bs4 import BeautifulSoup
from e_invoice_erp.e_invoice_erp.doctype.sales_e_invoice.API_E_invoice import APIAccessToken
import pytz
import requests
import time

tax_subtotals = []
tax_subtotal_dict={}
tax_rates =[]
tax_category=""
class SalesEInvoice(Document):
    # def before_save(self):
     #  self.api_access_token = APIAccessToken.create_api_token_instance().getToken()
	
    def on_submit(self):
        sales_invoice_id = self.naming  # Use self.name to get the document name, which is the ID
        print("sales_invoice_id", sales_invoice_id)
            
        try:
            # Fetch the sales invoice document
            sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice_id)
            tax_category = str(sales_invoice_doc.tax_category).strip()

            tax_category = sales_invoice_doc.tax_category

            other_charges_html = sales_invoice_doc.other_charges_calculation
            soup = BeautifulSoup(other_charges_html, 'html.parser')
            tax_table = soup.find('table', {'class': 'table table-bordered table-hover'})

            tax_rates = []
            if tax_table:
                for row in tax_table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    if len(cells) > 2:
                        tax_rate_text = cells[2].text.strip().split()[-1]
                        tax_rates.append(tax_rate_text)
                    else:
                        tax_rates.append('0.00')

            # Get the invoice data by calling get_document_info
            invoice_data = get_document_info(
                sales_invoice_doc.name,
                sales_invoice_doc.customer_name,
                sales_invoice_doc.customer_tin,
                sales_invoice_doc.customer_brn,
                sales_invoice_doc.address_line1,
                sales_invoice_doc.city_customer,
                sales_invoice_doc.state_customer,
                sales_invoice_doc.customer_state_code,
                sales_invoice_doc.customer_postal_code,
                sales_invoice_doc.customer_phone,
                sales_invoice_doc.posting_date,
                sales_invoice_doc.posting_time,
                sales_invoice_doc.e_invoice_type_code,
                sales_invoice_doc.additional_document_reference,
                sales_invoice_doc.company,
                sales_invoice_doc.msic_codes,
                sales_invoice_doc.registration_name,
                sales_invoice_doc.registration_full_name,
                sales_invoice_doc.supplier_tin,
                sales_invoice_doc.supplier_brn,
                sales_invoice_doc.tourism_tax_registration,
                sales_invoice_doc.supplier_location,
                sales_invoice_doc.supplier_city,
                sales_invoice_doc.supplier_state_codes,
                sales_invoice_doc.supplier_postal_code,
                sales_invoice_doc.suplier_mobile,  
                sales_invoice_doc.total_taxes_and_charges,
                sales_invoice_doc.net_total,
                sales_invoice_doc.grand_total,
                sales_invoice_doc.rounded_total,
                sales_invoice_doc.items,
                tax_category=tax_category,
                tax_rates=tax_rates, 
            )

            response = send_einvoice(invoice_data)
            if response:
                            self.submission_uid = response.get("submissionUid")
                            self.uuid = response.get("uuid")
                            self.invoicecodenumber = response.get("invoiceCodeNumber")
                            print(f"submission_uid: {self.submission_uid}")
                            print(f"uuid: {self.uuid}")
                            print(f"invoicecodenumber: {self.invoicecodenumber}")
                            self.save() 
            else:
                    frappe.throw("No data returned from e-invoice service. Please check logs for details.")
        except Exception as e:
            frappe.throw(f"Failed to send e-invoice: ")


@frappe.whitelist()
def fetch_sales_invoice_details(sales_invoice):
    sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice)

    tax_category = str(sales_invoice_doc.tax_category).strip()
    print(f"Fetched tax_category: {tax_category}, type: {type(tax_category)}")

    tax_category = sales_invoice_doc.tax_category


    other_charges_html = sales_invoice_doc.other_charges_calculation
    soup = BeautifulSoup(other_charges_html, 'html.parser')
    tax_table = soup.find('table', {'class': 'table table-bordered table-hover'})

    tax_rates = []
    if tax_table:
        for row in tax_table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) > 2:
                tax_rate_text = cells[2].text.strip().split()[-1]
                tax_rates.append(tax_rate_text)
            else:
                tax_rates.append('0.00')

            
    return {
        #customer information
        "naming": sales_invoice_doc.name,
        "title": sales_invoice_doc.title,
        "customer": sales_invoice_doc.customer,
        "customer_name": sales_invoice_doc.customer_name,
        "customer_tin": sales_invoice_doc.customer_tin,
        "customer_brn": sales_invoice_doc.customer_brn,
        "customer_address": sales_invoice_doc.customer_address,
        "city_customer" :sales_invoice_doc.city_customer,
        "state_customer" :sales_invoice_doc.state_customer,
        "customer_state_code": sales_invoice_doc.customer_state_code,
        "customer_postal_code": sales_invoice_doc.customer_postal_code,
        "customer_phone": sales_invoice_doc.customer_phone,
        "supplier_city": sales_invoice_doc.supplier_city,
        "tax_id": sales_invoice_doc.tax_id,
        "is_pos": sales_invoice_doc.is_pos,
        "pos_profile": sales_invoice_doc.pos_profile,

        #INVOICE INFORMATION
        "naming_series": sales_invoice_doc.naming_series,
        "posting_date": sales_invoice_doc.posting_date,
        "posting_time": sales_invoice_doc.posting_time,
        "e_invoice_type_code": sales_invoice_doc.e_invoice_type_code,
        "additional_document_reference": sales_invoice_doc.additional_document_reference,


        #Supplier information
        "company": sales_invoice_doc.company,
        "msic_codes": sales_invoice_doc.msic_codes,
        "registration_name": sales_invoice_doc.registration_name,
        "registration_full_name": sales_invoice_doc.registration_full_name,
        "supplier_tin": sales_invoice_doc.supplier_tin,
        "supplier_brn": sales_invoice_doc.supplier_brn,
        "tourism_tax_registration": sales_invoice_doc.tourism_tax_registration,


        "supplier_address_name": sales_invoice_doc.supplier_address_name,
        "suplier_mobile": sales_invoice_doc.suplier_mobile,
        "supplier_location": sales_invoice_doc.supplier_location,
        "supplier_city": sales_invoice_doc.supplier_city,
        "supplier_state": sales_invoice_doc.supplier_state,
        "supplier_state_codes" : sales_invoice_doc.supplier_state_codes,
        "supplier_postal_code": sales_invoice_doc.supplier_postal_code,
        "sales_invoice_id": sales_invoice_doc.name,
        "address_line1":sales_invoice_doc.address_line1,
        "description":sales_invoice_doc.description,
        "items": sales_invoice_doc.items,
        "taxes": sales_invoice_doc.taxes,

            # Totals
        "total_qty": sales_invoice_doc.total_qty,
        "base_total": sales_invoice_doc.base_total,
        "base_net_total": sales_invoice_doc.base_net_total,
        "total_net_weight": sales_invoice_doc.total_net_weight,
        "total": sales_invoice_doc.total,
        "net_total": sales_invoice_doc.net_total,
        "base_total_taxes_and_charges": sales_invoice_doc.base_total_taxes_and_charges,
        "total_taxes_and_charges": sales_invoice_doc.total_taxes_and_charges,
        "loyalty_points": sales_invoice_doc.loyalty_points,
        "loyalty_amount": sales_invoice_doc.loyalty_amount,
        "redeem_loyalty_points": sales_invoice_doc.redeem_loyalty_points,
        "loyalty_program": sales_invoice_doc.loyalty_program,
        "loyalty_redemption_account": sales_invoice_doc.loyalty_redemption_account,
        "loyalty_redemption_cost_center": sales_invoice_doc.loyalty_redemption_cost_center,
        "apply_discount_on": sales_invoice_doc.apply_discount_on,
        "base_discount_amount": sales_invoice_doc.base_discount_amount,
        "additional_discount_percentage": sales_invoice_doc.additional_discount_percentage,
        "discount_amount": sales_invoice_doc.discount_amount,
        "base_grand_total": sales_invoice_doc.base_grand_total,
        "base_rounding_adjustment": sales_invoice_doc.base_rounding_adjustment,
        "base_rounded_total": sales_invoice_doc.base_rounded_total,
        "base_in_words": sales_invoice_doc.base_in_words,
        "grand_total": sales_invoice_doc.grand_total,
        "rounding_adjustment": sales_invoice_doc.rounding_adjustment,
        "rounded_total": sales_invoice_doc.rounded_total,
        "in_words": sales_invoice_doc.in_words,
        "total_advance": sales_invoice_doc.total_advance,
        "outstanding_amount": sales_invoice_doc.outstanding_amount,
        "debit_to": sales_invoice_doc.debit_to,
        "other_charges_calculation": sales_invoice_doc.other_charges_calculation,
        "tax_category": sales_invoice_doc.tax_category,
        "name": sales_invoice_doc.name


    }


@frappe.whitelist()
def get_document_info(
    sales_invoice_id,
    customer_name,
    customer_tin,
    customer_brn,
    address_line1,
    city_customer,
    state_customer,
    customer_state_code,
    customer_postal_code,
    customer_phone,

    posting_date,
    posting_time,
    e_invoice_type_code,
    additional_document_reference,

    company,
    msic_codes,
    registration_name,
    registration_full_name,
    supplier_tin,
    supplier_brn,
    tourism_tax_registration,   
    supplier_location,
    supplier_city,
    supplier_state_codes,
    supplier_postal_code,
    suplier_mobile,
    total_taxes_and_charges,
    net_total,
    grand_total,
    rounded_total,
    items,
    tax_category=tax_category,
    tax_rates=tax_rates, 

):
    


    tax_subtotals = []
    print(f"tax_category: {tax_category}, type: {type(tax_category)}")  # Debug print

    for tax_rate in tax_rates:
        try:
            # Remove 'RM' and ',' from tax_rate and then convert to float
            tax_rate_float = float(tax_rate.replace('RM', '').replace(',', ''))
            
            # Create tax_amount_dict
            tax_amount_dict = {
                "_": tax_rate_float,
                "currencyID": "MYR",
            }
            
            # Create tax_subtotal_dict
            tax_subtotal_dict = {
                "TaxableAmount": [{"_":net_total, "currencyID": "MYR"}], #if hasattr('net_total') and isinstance(net_total, (int, float)) else [],
                "TaxAmount": [tax_amount_dict],
                "TaxCategory": [
                    {
                        "ID": [{"_": tax_category}] ,
                        "TaxScheme": [
                            {
                                "ID": [
                                    {
                                        "_": "OTH",
                                        "schemeID": "UN/ECE 5153",
                                        "schemeAgencyID": "6",
                                    }
                                ]
                            }
                        ],
                    }
                ],
            }
            
            tax_subtotals.append(tax_subtotal_dict)

            
        except ValueError as e:
            print(f"Error converting tax_rate '{tax_rate}' to float: {e}")
            # Handle or log the error as needed
        print(tax_subtotal_dict)

       


    item_prices = []

    for index, item in enumerate(items):
        item_tax_subtotal = tax_subtotals[index] if index < len(tax_subtotals) else {}

        invoice_item = {
            "ID": [{"_": str(index + 1)}],
            "Item": [
                {
                    "CommodityClassification": [
                        {
                            "ItemClassificationCode": [
                                {"_": item.classification_codes, "listID": "CLASS"}
                            ]
                        }
                    ]if hasattr(item, 'classification_codes') and isinstance(item.classification_codes, (str)) else [],
                    "Description": [{"_": item.description}]if hasattr(item, 'description') and isinstance(item.description, (str)) else []
                }
            ],
            "LineExtensionAmount": [{"_": item.net_amount, "currencyID": "MYR"}] if hasattr(item, 'net_amount') and isinstance(item.net_amount, (int, float)) else [],
            "TaxTotal": [
                            {
                                "TaxAmount": [{"_": total_taxes_and_charges, "currencyID": "MYR"}],
                                "TaxSubtotal": [
                                    {
                                        "TaxAmount": [{"_": item_tax_subtotal.get("TaxAmount", [{}])[0].get("_", 0), "currencyID": "MYR"}],
                                        "TaxCategory": [
                                            {
                                                "ID": [{"_": tax_category}],
                                                "Percent": [{"_": item_tax_subtotal.get("TaxAmount", [{}])[0].get("_", 0) / item.amount * 100}]if hasattr(item, 'amount') and isinstance(item.amount, (int, float)) else [],
                                                "TaxScheme": [
                                                    {
                                                        "ID": [
                                                            {
                                                                "_": "OTH",
                                                                "schemeID": "UN/ECE 5153",
                                                                "schemeAgencyID": "6",
                                                            }
                                                        ]
                                                    }
                                                ],
                                            }
                                        ],}],}],
            "Price": [{"PriceAmount": [{"_": item.price_list_rate, "currencyID": "MYR"}]}] if hasattr(item, 'price_list_rate') and isinstance(item.price_list_rate, (int, float)) else [],
            "ItemPriceExtension": [{"Amount": [{"_": item.total_amount_before_discount, "currencyID": "MYR"}]}] if hasattr(item, 'total_amount_before_discount') and isinstance(item.total_amount_before_discount, (int, float)) else [],
        }

        item_prices.append(invoice_item) 
   

    # Fetch the Sales Invoice document
    sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice_id)

    # Assuming posting_date and posting_time are given and need to be converted
    posting_date = sales_invoice_doc.get("posting_date")
    posting_time = sales_invoice_doc.get("posting_time")

    if isinstance(posting_date, str):
        posting_date = datetime.strptime(posting_date, "%Y-%m-%d")

    if isinstance(posting_time, str):
        hours, minutes, seconds = map(int, posting_time.split(':'))
        posting_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    if isinstance(posting_time, timedelta):
        posting_time_str = (datetime.min + posting_time).time().strftime("%H:%M:%S")
    else:
        posting_time_str = posting_time.strftime("%H:%M:%S")

    # Combine posting_date and posting_time to a single datetime object
    combined_datetime = datetime.combine(posting_date, datetime.strptime(posting_time_str, "%H:%M:%S").time())

    # Convert combined_datetime to UTC
    local_timezone = pytz.timezone("Asia/Kuala_Lumpur")  # Change this to the appropriate local timezone
    local_datetime = local_timezone.localize(combined_datetime, is_dst=None)
    utc_datetime = local_datetime.astimezone(pytz.utc)

    formatted_posting_date = utc_datetime.strftime("%Y-%m-%d")
    formatted_issue_time = utc_datetime.strftime("%H:%M:%SZ")

    print(f"Formatted Posting Date in UTC: {formatted_posting_date}")
    print(f"Formatted Issue Time in UTC: {formatted_issue_time}")

    

    document_content = {
            
            "_D": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
            "_A": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "_B": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "_E": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
            "Invoice": [
                {
                    "ID": [{"_": sales_invoice_id}],
                    "IssueDate": [{"_": formatted_posting_date}],
                    "IssueTime": [{"_": formatted_issue_time}],
                    "InvoiceTypeCode": [
                        {"_": e_invoice_type_code, "listVersionID": "1.0"}
                    ],
                    "DocumentCurrencyCode": [{"_": "MYR"}],
                    "BillingReference": [
                        {
                            "AdditionalDocumentReference": [
                                {"ID": [{"_": additional_document_reference}]}
                            ]
                        }
                    ],
                    "AccountingSupplierParty": [
                        {
                            "Party": [
                                {
                                    "IndustryClassificationCode": [
                                        {
                                            "_": msic_codes,
                                            "name": company,
                                        }
                                    ],
                                    "PartyIdentification": [
                                        {"ID": [{"_": supplier_tin, "schemeID": "TIN"}]},
                                        {"ID": [{"_": supplier_brn, "schemeID": "BRN"}]},
                                        {
                                            "ID": [
                                                {
                                                    "_": tourism_tax_registration,
                                                    "schemeID": "SST",
                                                }
                                            ]
                                        },
                                    ],
                                    "PostalAddress": [
                                        {
                                            "CityName": [{"_": supplier_city}],
                                            "PostalZone": [{"_": supplier_postal_code}],
                                            "CountrySubentityCode": [
                                                {"_": supplier_state_codes}
                                            ],
                                            "AddressLine": [
                                                {"Line": [{"_": supplier_location}]},
                                            ],
                                            "Country": [
                                                {
                                                    "IdentificationCode": [
                                                        {
                                                            "_": "MYS",
                                                            "listID": "ISO3166-1",
                                                            "listAgencyID": "6",
                                                        }
                                                    ]
                                                }
                                            ],
                                        }
                                    ],
                                    "PartyLegalEntity": [
                                        {
                                            "RegistrationName": [
                                                {"_": registration_full_name}
                                            ]
                                        }
                                    ],
                                    "Contact": [
                                        {
                                            "Telephone": [{"_": suplier_mobile}],
                                            "ElectronicMail": [{"_": "hisham@gmail.com"}],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                    "AccountingCustomerParty": [
                        {
                            "Party": [
                                {
                                    "PostalAddress": [
                                        {
                                            "CityName": [{"_": city_customer}],
                                            "PostalZone": [{"_": customer_postal_code}],
                                            "CountrySubentityCode": [{"_": customer_state_code}],
                                            "AddressLine": [
                                                {"Line": [{"_": address_line1}]},
                                            ],
                                            "Country": [
                                                {
                                                    "IdentificationCode": [
                                                        {
                                                            "_": "MYS",
                                                            "listID": "ISO3166-1",
                                                            "listAgencyID": "6",
                                                        }
                                                    ]
                                                }
                                            ],
                                        }
                                    ],
                                    "PartyLegalEntity": [
                                        {"RegistrationName": [{"_": customer_name}]}
                                    ],
                                    "PartyIdentification": [
                                        {
                                            "ID": [
                                                {"_": customer_tin, "schemeID": "TIN"}
                                            ]
                                        },
                                        {
                                            "ID": [
                                                {"_": customer_brn, "schemeID": "BRN"}
                                            ]
                                        },
                                    ],
                                    "Contact": [
                                        {
                                            "Telephone": [{"_": customer_phone}],
                                            "ElectronicMail": [
                                                {"_": "dummy@maxis.com.my"}
                                            ],
                                        }
                                    ],
                                }
                            ]
                        }
                    ],
                    "TaxTotal": [
                        {
                            "TaxAmount": [{"_": total_taxes_and_charges, "currencyID": "MYR"}],
                            "TaxSubtotal": 
                     		 tax_subtotals
                            
                        }
                    ],
                    "LegalMonetaryTotal": [
                        {
                            "TaxExclusiveAmount": [{"_": net_total, "currencyID": "MYR"}],
                            "TaxInclusiveAmount": [{"_": grand_total, "currencyID": "MYR"}],
                            "PayableAmount": [{"_": rounded_total, "currencyID": "MYR"}],
                        }
                    ],
                    "InvoiceLine": item_prices
                    
                }
            ],
        }

    json_content = json.dumps(document_content, indent=2).encode()


    base64_document = base64.b64encode(json_content).decode("utf-8")

    document_hash = hashlib.sha256(json_content).hexdigest()




    invoice_data =  {
        "format": "JSON",
        "document": base64_document,
        "documentHash": document_hash,
        "invoice_id": sales_invoice_id,
    }
    print("invoice_data",invoice_data)

    return invoice_data

def send_einvoice(invoice_data):

    try:
        # Get the generated access token
        generated_access_token = APIAccessToken.create_api_token_instance().getToken()

        # Headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ERPNextPythonClient/1.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": f"Bearer {generated_access_token}",
            "Accept": "application/json",
            "Accept-Language": "en"
        }

        # Body
        body = {
            "documents": [
                {
                    "document": invoice_data["document"],
                    "codeNumber": invoice_data["invoice_id"],
                    "format": "JSON",
                    "documentHash": invoice_data["documentHash"]
                }
            ]
        }
        # API base URL
        send_api_base_url = "https://preprod-api.myinvois.hasil.gov.my"
        send_document_url = f"{send_api_base_url}/api/v1.0/documentsubmissions"

        # Making the API request
        response = requests.post(send_document_url, headers=headers, json=body)
        print(response)
        
        # Log the response content for debugging
        response_content = response.json()
        print("Response content:", response_content)

        # Check the response
        if response.status_code in [200, 202]:
            response_data = response_content

            # Extract relevant data from the response
            submission_uid = response_data.get('submissionUid')
            accepted_documents = response_data.get('acceptedDocuments', [])

            if accepted_documents:
                # Extracting uuid and invoiceCodeNumber from accepted documents
                uuid = accepted_documents[0].get('uuid')
                invoice_code_number = accepted_documents[0].get('invoiceCodeNumber')
                
                return {
                    "submissionUid": submission_uid,
                    "uuid": uuid,
                    "invoiceCodeNumber": invoice_code_number
                }
            else:
                error_message = "No accepted documents in the response.",response_data
                print(error_message)
                frappe.log_error(error_message, title="E-Invoice Error")
                frappe.throw("No accepted documents returned from e-invoice service. Please check Error logs list for details.")
        else:
            raise Exception(f"Request failed with status code {response.status_code}\n{response.text}")
            
    except Exception as e:
        error_message = f"Error sending e-invoice: {str(e)}"
        # frappe.msgprint(f"Error sending e-invoice: {str(e)}")
        frappe.msgprint(error_message, title="E-Invoice Error", indicator="red")
        # frappe.log_error(error_message, title="E-Invoice Error")
        raise
