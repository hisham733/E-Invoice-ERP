from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from e_invoice_erp.e_invoice_erp.doctype.sales_e_invoice.API_E_invoice import APIAccessToken
import requests

class CancelDocument(Document):
#     def on_update(self):
#         uuid = self.uuid
#         frappe.msgprint(f"Submission UID: {uuid}")

    def on_submit(self):
        uuid = self.uuid
        # frappe.msgprint(f"Submission UID before save: {uuid}")
        response_data = self.cancel_document()
        # frappe.msgprint(f"Response Data: {response_data}")

        if response_data:
            try:
                # self.status = response_data.get("status")
                # self.save()
                frappe.msgprint("Document cancelled successfully.",response_data)
            except Exception as e:
                frappe.log_error(message=str(e), title="E-Invoice Response Error")
                frappe.msgprint(f"Error saving document: {str(e)}")
        else:
            frappe.throw("No data returned from e-invoice service. Please check logs list for details.")

    def cancel_document(self):
        try:
            generated_access_token = APIAccessToken.create_api_token_instance().getToken()

            headers = {
                "Content-Type": "application/json",
                "User-Agent": "ERPNextPythonClient/1.0",
                "Authorization": f"Bearer {generated_access_token}",
                "Accept": "application/json",
                "Accept-Language": "en",
            }

            body = {
                "status": "cancelled",
                "reason": self.reason  # Assuming self.reason is set correctly
            }

            cancel_document_url = f"https://preprod-api.myinvois.hasil.gov.my/api/v1.0/documents/state/{self.uuid}/state"

            response = requests.put(cancel_document_url, headers=headers, json=body)

            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                raise Exception(
                    f"Failed to cancel document with status code {response.status_code}: {response.text}"
                )

        except Exception as e:
            frappe.log_error(message=str(e), title="E-Invoice API Error")
            frappe.msgprint(f"Failed to cancel document. Error: {str(e)}")