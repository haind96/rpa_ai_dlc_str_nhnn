import httpx
from typing import Dict, Any, List, Optional
from loguru import logger
from src.config import AppConfig

class ECMClient:
    """Client for interacting with the ECM APIs."""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = httpx.Client(timeout=30.0)
        self.token: Optional[str] = None

    def authenticate(self) -> None:
        """Authenticate and retrieve token using client credentials."""
        logger.info("Authenticating with ECM...")
        data = {
            "grant_type": "client_credentials",
            "client_id": "rpa_user2",
            "client_secret": self.config.ecm_client_credential
        }
        logger.info(f"ECM Auth Request - URL: {self.config.ecm_auth_url}, Data: {data}")
        response = self.client.post(self.config.ecm_auth_url, data=data)
        logger.info(f"ECM Auth Response - Status: {response.status_code}, Body: {response.text}")
        response.raise_for_status()
        
        token_data = response.json()
        self.token = token_data.get("access_token")
        if not self.token:
            raise ValueError("Failed to retrieve access token from response")
            
        logger.info("Authenticated successfully.")

    def search_files(self, business_code: str, customer_code: str) -> List[Dict[str, Any]]:
        """Search files for a specific customer and business code."""
        if not self.token:
            self.authenticate()

        url = self.config.ecm_search_url.format(business_code=business_code)
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "metadata": {
                "customerCode": {
                    "type": "eq",
                    "value": customer_code
                }
            },
            "pagination": {
                "page": 1,
                "size": 100
            }
        }
        
        logger.info(f"ECM Search Request - URL: {url}, Payload: {payload}")
        response = self.client.post(url, headers=headers, json=payload)
        logger.info(f"ECM Search Response - Status: {response.status_code}, Body: {response.text}")
        
        if response.status_code == 401:
            logger.info("Token might be expired, re-authenticating...")
            self.authenticate()
            headers["Authorization"] = f"Bearer {self.token}"
            logger.info(f"ECM Search Request (Retry) - URL: {url}, Payload: {payload}")
            response = self.client.post(url, headers=headers, json=payload)
            logger.info(f"ECM Search Response (Retry) - Status: {response.status_code}, Body: {response.text}")
            
        response.raise_for_status()
        
        response_data = response.json()
        # Ensure we return a list of files from data.result
        data_obj = response_data.get("data") or {}
        return data_obj.get("result", [])

    def download_file(self, file_id: str) -> bytes:
        """Download file content by file_id."""
        if not self.token:
            self.authenticate()

        url = self.config.ecm_content_url.format(file_id=file_id)
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        
        logger.info(f"ECM Download Request - URL: {url}")
        response = self.client.get(url, headers=headers)
        logger.info(f"ECM Download Response - Status: {response.status_code}, Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 401:
            logger.info("Token might be expired, re-authenticating...")
            self.authenticate()
            headers["Authorization"] = f"Bearer {self.token}"
            logger.info(f"ECM Download Request (Retry) - URL: {url}")
            response = self.client.get(url, headers=headers)
            logger.info(f"ECM Download Response (Retry) - Status: {response.status_code}, Content-Length: {len(response.content)} bytes")
            
        response.raise_for_status()
        return response.content

    def close(self):
        """Close the underlying HTTP client."""
        self.client.close()
