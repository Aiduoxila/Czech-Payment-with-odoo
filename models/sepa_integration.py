import requests
from odoo import models, fields, api

class SepaIntegration(models.Model):
    _name = 'payment.sepa'
    _description = 'SEPA Payment Integration'

    def initiate_sepa_transfer(self, iban, bic, amount, currency, recipient_name):
        """Initiates a SEPA Credit Transfer."""
        sepa_url = 'https://example-sepa-provider.com/api/transfer'
        headers = {
            'Authorization': 'Bearer YOUR_SEPA_API_KEY',
            'Content-Type': 'application/json'
        }
        payload = {
            'iban': iban,
            'bic': bic,
            'amount': int(amount * 100),  # Convert to minor units (e.g., cents)
            'currency': currency,
            'recipient_name': recipient_name,
        }
        response = requests.post(sepa_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"SEPA API error: {response.text}")
    
    def initiate_sepa_direct_debit(self, mandate_id, amount, currency):
        """Initiates a SEPA Direct Debit."""
        sepa_url = 'https://example-sepa-provider.com/api/direct_debit'
        headers = {
            'Authorization': 'Bearer YOUR_SEPA_API_KEY',
            'Content-Type': 'application/json'
        }
        payload = {
            'mandate_id': mandate_id,
            'amount': int(amount * 100),  # Convert to minor units
            'currency': currency,
        }
        response = requests.post(sepa_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"SEPA API error: {response.text}")
