"""
Yokoy API Client

Handles communication with Yokoy FX Rates API.
API Documentation: https://developer.yokoy.ai/api-reference#tag/FX-rates/operation/applyFxRate
"""

import requests
from datetime import date
from typing import List, Dict, Any


class YokoyClient:
    """Client for interacting with Yokoy FX Rates API"""
    
    def __init__(self, api_url: str, api_key: str):
        """
        Initialize Yokoy client
        
        Args:
            api_url: Base URL for Yokoy API (e.g., https://app.yokoy.io/public/v1)
            api_key: API key for authentication
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        })
    
    def upload_fx_rates(self, rates_data, target_date: date) -> Dict[str, Any]:
        """
        Upload FX rates to Yokoy
        
        Args:
            rates_data: Exchange rate data from MNB (Day object with rates list)
            target_date: The date for these rates
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.HTTPError: If API request fails
        """
        # Transform MNB data to Yokoy format
        # Yokoy API expects rates relative to a base currency (HUF in our case)
        fx_rates = []
        
        for rate in rates_data.rates:
            fx_rates.append({
                "currency": rate.currency,
                "rate": rate.rate,
                "date": target_date.isoformat() if hasattr(target_date, 'isoformat') else str(target_date)
            })
        
        # Prepare request payload
        payload = {
            "baseCurrency": "HUF",
            "rates": fx_rates,
            "effectiveDate": target_date.isoformat() if hasattr(target_date, 'isoformat') else str(target_date)
        }
        
        # Make API request
        url = f"{self.api_url}/fx-rates"
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "rates_uploaded": len(fx_rates)
            }
            
        except requests.exceptions.HTTPError as e:
            error_detail = ""
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                except:
                    error_detail = e.response.text
            
            return {
                "success": False,
                "status_code": e.response.status_code if e.response else None,
                "error": str(e),
                "error_detail": error_detail
            }
        
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def test_connection(self) -> bool:
        """
        Test if API credentials are valid
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try a simple GET request to verify credentials
            url = f"{self.api_url}/fx-rates"
            response = self.session.get(url, timeout=10)
            return response.status_code in [200, 404]  # 404 is OK, means auth worked
        except:
            return False
