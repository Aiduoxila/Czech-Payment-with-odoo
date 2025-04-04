import requests
from odoo import models, fields

    _name = 'payment.gopay'

    def initiate_payment(self, order_id, amount, currency):
        """Fetch the API key from configuration and initiate payment"""
        gopay_api_key = self.env['ir.config_parameter'].sudo().get_param('cz_payment_integration.gopay_api_key')
        gopay_url = 'https://api.gopay.cz/v3/payments'
        headers = {
            'Authorization': f'Bearer {gopay_api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_number': order_id,
            'amount': int(amount * 100),
            'currency': currency,
            'callback_url': 'https://your-odoo-instance/payment/gopay/callback'
        }
        response = requests.post(gopay_url, json=payload, headers=headers)
        return response.json()


    _name = 'payment.gopay'

    def initiate_payment(self, order_id, amount, currency):
        """Fetch the API key from configuration and initiate payment"""
        gopay_api_key = self.env['ir.config_parameter'].sudo().get_param('cz_payment_integration.gopay_api_key')
        gopay_url = 'https://api.gopay.cz/v3/payments'
        headers = {
            'Authorization': f'Bearer {gopay_api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'order_number': order_id,
            'amount': int(amount * 100),
            'currency': currency,
            'callback_url': 'https://your-odoo-instance/payment/gopay/callback'
        }
        response = requests.post(gopay_url, json=payload, headers=headers)
        return response.json()
