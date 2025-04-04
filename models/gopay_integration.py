import requests
from odoo import models, fields

class GoPayIntegration(models.Model):
    _name = 'payment.gopay'
    _description = 'GoPay Payment Integration'

    def initiate_payment(self, order_id, amount, currency):
        """Initiates a payment with GoPay."""
        gopay_url = 'https://api.gopay.cz/v3/payments'
        headers = {
            'Authorization': 'Bearer YOUR_GOPAY_API_KEY',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_number': order_id,
            'amount': int(amount * 100),  # Convert to minor units
            'currency': currency,
            'callback_url': 'https://your-odoo-instance/payment/gopay/callback'
        }
        response = requests.post(gopay_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"GoPay API error: {response.text}")
