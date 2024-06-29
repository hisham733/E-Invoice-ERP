# my_custom_app/my_custom_app/doctype/token_fetcher.py
import frappe
import requests
 
class APIAccessToken:

    api_token_object = None
    __api_access_token = None

    def __init__(self):
        pass

    @classmethod
    def __fetch_access_token(cls):
        api_base_url = "https://preprod-api.myinvois.hasil.gov.my"
        token_url = f"{api_base_url}/connect/token"

        client_id = "04f01055-4488-459e-9b54-84266eecfb6a"
        client_secret = "a18150d4-59d5-4dbb-b8ef-6d01e03aaf86"
        grant_type = "client_credentials"
        scope = "InvoicingAPI"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "ERPNextPythonClient/1.0",
            "Accept": "*/*",
        }

        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
            "scope": scope,
        }

        response = requests.post(token_url, headers=headers, data=payload)

        if response.status_code == 200:
            token_data = response.json()
            frappe.logger().info(f"Access Token: {token_data['access_token']}")
            return token_data["access_token"]
        else:
            frappe.logger().error(f"Error: {response.status_code}")
            frappe.logger().error(response.text)
            return None
        
    @classmethod
    def __update_api_access_token(cls):
        cls.__api_access_token = cls.__fetch_access_token()

    @staticmethod
    def create_api_token_instance():
        if APIAccessToken.api_token_object is None:
            APIAccessToken.api_token_object = APIAccessToken()
        APIAccessToken.api_token_object.__update_api_access_token()
        return APIAccessToken.api_token_object

    @staticmethod
    def get_api_token_object():
        if APIAccessToken.api_token_object is None:
            raise ValueError("API token object is not initialized")
        return APIAccessToken.api_token_object

    @classmethod
    def getToken(cls):
        return cls.__api_access_token
    
    