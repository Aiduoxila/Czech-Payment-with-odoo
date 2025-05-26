from odoo import models, fields, api
import requests

class PaysIntegration(models.Model):
    _name = "pays.integration"
    _description = "Integration with Pays Payment Gateway"

    transaction_id = fields.Char(string="Transaction ID")
    amount = fields.Float(string="Amount")
    currency = fields.Char(string="Currency", default="CZK")
    status = fields.Selection([("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")], string="Payment Status")

    def generate_payment_link(self, amount):
        """ Generate a payment link via Pays API """
        url = "https://pays.cz/api/generate_link"
        payload = {
            "amount": amount,
            "currency": self.currency,
            "callback_url": "https://yourdomain.com/payment/callback"
        }
        response = requests.post(url, json=payload)
        return response.json()

    def check_payment_status(self, transaction_id):
        """ Check the payment status of a transaction """
        url = f"https://pays.cz/api/status/{transaction_id}"
        response = requests.get(url)
        data = response.json()
        self.status = data.get("status", "pending")
        return data

