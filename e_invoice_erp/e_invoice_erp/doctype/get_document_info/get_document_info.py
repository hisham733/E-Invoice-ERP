# -*- coding: utf-8 -*-
# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import datetime
import frappe
from frappe.model.document import Document
import requests
from e_invoice_erp.e_invoice_erp.doctype.sales_e_invoice.API_E_invoice import APIAccessToken

class GetDocumentInfo(Document):
	def on_update(self):
		uuid = self.submission_uid
		print("submission_uid",uuid)
	def before_save(self):
		uuid = self.submission_uid
		print("submission_uid",self.submission_uid)
		response_data = get_document_status(uuid)
		print("response_data",response_data)
		if response_data:
			try:
				# Assuming you want to store the data in the EInvoiceResponse DocType
				# store_e_invoice_response(response)
				self.overall_status = response_data.get("overallStatus")

				# Extract data from the response
				self.document_count = response_data.get('documentCount')
				self.date_time_received = parse_datetime (response_data.get('dateTimeReceived'))
				self.overall_status = response_data.get('overallStatus')

				document_summary = response_data.get('documentSummary', [])[0]
				self.uuid = document_summary.get('uuid')
				self.submission_uid_summary = document_summary.get('submissionUid')
				self.long_id = document_summary.get('longId')
				self.internal_id = document_summary.get('internalId')
				self.type_name = document_summary.get('typeName')
				self.type_version_name = document_summary.get('typeVersionName')
				self.issuer_tin = document_summary.get('issuerTin')
				self.issuer_name = document_summary.get('issuerName')
				self.receiver_id = document_summary.get('receiverId')
				self.receiver_name = document_summary.get('receiverName')
				self.date_time_issued = parse_datetime (document_summary.get('dateTimeIssued'))
				self.date_time_received_summary = parse_datetime (document_summary.get('dateTimeReceived'))
				self.date_time_validated = parse_datetime (document_summary.get('dateTimeValidated'))
				self.total_payable_amount = document_summary.get('totalPayableAmount')
				self.total_excluding_tax = document_summary.get('totalExcludingTax')
				self.total_discount = document_summary.get('totalDiscount')
				self.total_net_amount = document_summary.get('totalNetAmount')
				self.status = document_summary.get('status')
				self.cancel_date_time = parse_datetime (document_summary.get('cancelDateTime'))
				self.reject_request_date_time = parse_datetime (document_summary.get('rejectRequestDateTime'))
				self.document_status_reason = document_summary.get('documentStatusReason')
				self.created_by_user_id = document_summary.get('createdByUserId')
			except Exception as e:
				frappe.log_error(message=str(e), title="E-Invoice Response Error")
		else:
			frappe.throw("No data returned from e-invoice service. Please check logs for details.")

def get_document_status(uuid):
	try:
		generated_access_token = APIAccessToken.create_api_token_instance().getToken()

		headers = {
			"Content-Type": "application/json",
			"User-Agent": "ERPNextPythonClient/1.0",
			"Accept": "*/*",
			"Accept-Encoding": "gzip, deflate, br",
			"Authorization": f"Bearer {generated_access_token}",
			"Accept": "application/json",
			"Accept-Language": "en",
		}

		send_api_base_url = "https://preprod-api.myinvois.hasil.gov.my"
		get_document_url = f"{send_api_base_url}/api/v1.0/documentsubmissions/{uuid}"

		# Making the API request
		response = requests.get(get_document_url, headers=headers)

		if response.status_code == 200:
			response_data = response.json()

			return response_data
		else:
			raise Exception(
			f"Request failed with status code {response.status_code}\n{response.text}"
			)
	except Exception as e:
		print(f"Error occurred: {e}")
	frappe.log_error(message=str(e), title="E-Invoice API Error")
      	

def parse_datetime(datetime_str):
    if datetime_str:
        try:
            # Parse ISO format datetime string to datetime object
            dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            # Format datetime object as ERPNext datetime string
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            print(f"Error parsing datetime: {e}")
    return None

	# Example usage
	# if __name__ == "__main__":
	#     uuid = "3CNS3GD20NQTH4E9NBJ9CQ0J10"  # Replace with actual UUID
	#     get_document_status(uuid)