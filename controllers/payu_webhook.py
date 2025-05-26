import logging
from odoo import http
import json

_logger = logging.getLogger(__name__)

class PayUWebhookController(http.Controller):
    @http.route('/payu/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **post):
        """ Process PayU webhook event """
        try:
            data = json.loads(http.request.httprequest.data)
            _logger.info(f"Received PayU webhook: {data}")

            transaction_id = data.get("transaction_id")
            status = data.get("status")

            payment = http.request.env["payu.integration"].search([("transaction_id", "=", transaction_id)], limit=1)
            if payment:
                payment.status = status
                _logger.info(f"Updated PayU transaction {transaction_id} to status: {status}")
                return {"message": "Status updated successfully"}

            _logger.warning(f"PayU transaction {transaction_id} not found")
            return {"error": "Transaction not found"}

        except Exception as e:
            _logger.error(f"Error processing PayU webhook: {str(e)}")
            return {"error": "Internal server error"}
