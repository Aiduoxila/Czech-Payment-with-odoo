import requests
from odoo import models, fields, api

class GoPayIntegration(models.Model):
    _name = 'payment.gopay'
    _description = 'GoPay Payment Integration'

    name = fields.Char(default="GoPay Payment")

    def initiate_gopay_payment(self, order_id, amount, currency):
        """Initiate a payment with GoPay."""
        gopay_url = 'https://api.gopay.cz/v3/payments'
        headers = {
            'Authorization': 'Bearer YOUR_GOPAY_API_KEY',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_number': order_id,
            'amount': amount * 100,  # Convert to minor units (e.g., cents)
            'currency': currency,
            'callback_url': 'https://your-odoo-instance/payment/gopay/callback'
        }
        response = requests.post(gopay_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"GoPay API error: {response.text}")

class PayUIntegration(models.Model):
    _name = 'payment.payu'
    _description = 'PayU Payment Integration'

    name = fields.Char(default="PayU Payment")

    def initiate_payu_payment(self, order_id, amount, currency):
        """Initiate a payment with PayU."""
        payu_url = 'https://secure.payu.com/api/v2_1/orders'
        headers = {
            'Authorization': 'Bearer YOUR_PAYU_API_KEY',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_id': order_id,
            'amount': amount,
            'currency': currency,
            'notify_url': 'https://your-odoo-instance/payment/payu/notification'
        }
        response = requests.post(payu_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"PayU API error: {response.text}")
