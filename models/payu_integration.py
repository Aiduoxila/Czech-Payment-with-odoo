import requests
from odoo import models, fields

class PayUIntegration(models.Model):
    _name = 'payment.payu'
    _description = 'PayU Payment Integration'

    def initiate_payment(self, order_id, amount, currency):
        """Initiates a payment with PayU."""
        payu_url = 'https://secure.payu.com/api/v2_1/orders'
        headers = {
            'Authorization': 'Bearer YOUR_PAYU_API_KEY',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_id': order_id,
            'amount': int(amount * 100),  # Convert to minor units
            'currency': currency,
            'notify_url': 'https://your-odoo-instance/payment/payu/notification'
        }
        response = requests.post(payu_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"PayU API error: {response.text}")
