import logging
from odoo import http
import json

_logger = logging.getLogger(__name__)  # Define logger

class PaysWebhookController(http.Controller):
    @http.route('/pays/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **post):
        """ Process Pays webhook event with logging """
        try:
            data = json.loads(http.request.httprequest.data)
            _logger.info(f"Received webhook data: {data}")  # Log incoming request

            transaction_id = data.get("transaction_id")
            status = data.get("status")

            payment = http.request.env["pays.integration"].search([("transaction_id", "=", transaction_id)], limit=1)
            if payment:
                payment.status = status
                _logger.info(f"Updated transaction {transaction_id} to status: {status}")  # Log successful update
                return {"message": "Status updated successfully"}

            _logger.warning(f"Transaction {transaction_id} not found")  # Log missing transaction
            return {"error": "Transaction not found"}

        except Exception as e:
            _logger.error(f"Error processing webhook: {str(e)}")  # Log errors
            return {"error": "Internal server error"}
