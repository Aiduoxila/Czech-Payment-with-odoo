import logging
from odoo import http
import json

_logger = logging.getLogger(__name__)

class GoPayWebhookController(http.Controller):
    @http.route('/gopay/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **post):
        """ Process GoPay webhook event """
        try:
            data = json.loads(http.request.httprequest.data)
            _logger.info(f"Received GoPay webhook: {data}")

            transaction_id = data.get("id")
            status = data.get("state")

            payment = http.request.env["gopay.integration"].search([("transaction_id", "=", transaction_id)], limit=1)
            if payment:
                payment.status = status
                _logger.info(f"Updated GoPay transaction {transaction_id} to status: {status}")
                return {"message": "Status updated successfully"}

            _logger.warning(f"GoPay transaction {transaction_id} not found")
            return {"error": "Transaction not found"}

        except Exception as e:
            _logger.error(f"Error processing GoPay webhook: {str(e)}")
            return {"error": "Internal server error"}
