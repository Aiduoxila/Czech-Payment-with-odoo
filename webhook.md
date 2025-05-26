the webhook handling code in the controllers directory of your Czech-Payment-with-odoo module. Based on your repository's structure, the best approach would be:

1. Create the Controller File
Navigate to your module's root directory and create the folder:

mkdir controllers
touch controllers/pays_webhook.py
Then, update your controllers/pays_webhook.py file with the webhook handling code:

python
from odoo import http
import json

class PaysWebhookController(http.Controller):
    @http.route('/pays/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **post):
        """ Process Pays webhook event """
        data = json.loads(http.request.httprequest.data)

        transaction_id = data.get("transaction_id")
        status = data.get("status")

        payment = http.request.env["pays.integration"].search([("transaction_id", "=", transaction_id)], limit=1)
        if payment:
            payment.status = status
            return {"message": "Status updated successfully"}
        return {"error": "Transaction not found"}
2. Register the Controller
Modify your __init__.py file in the root directory to load the new controller:

python
from . import controllers.pays_webhook
3. Ensure the Module Recognizes the Controller
Odoo loads controllers dynamically, so after making these changes, restart your Odoo server and update the module:

bash
./odoo-bin -u czech_payment_integration --db-filter=my_database
4. Set Your Webhook in Pays Dashboard
Go to Pays.cz Webhook Settings.

Add the webhook URL:

https://yourdomain.com/pays/webhook
This setup ensures Odoo properly handles webhook notifications from Pays. Would you like me to add logging for better debugging? 🚀

yes
To enhance debugging, I’ll integrate logging into the webhook handler so you can track incoming requests and identify potential issues.

1. Add Logging to Webhook Handler
Modify your controllers/pays_webhook.py file to include logging:

python
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
2. Logging Levels
INFO: Logs received webhook data and successful updates.

WARNING: Logs when a transaction is missing.

ERROR: Logs unexpected issues.

3. Enable Logging in Odoo
Make sure logging is enabled by setting log_level in your Odoo configuration file (odoo.conf):

[options]
log_level = info
After implementing this, you can monitor logs in your Odoo instance:

bash
tail -f odoo.log | grep "PaysWebhookController"
This will help you debug webhook requests effectively!

does gopay and payu and sepa have webhook
Yes! GoPay, PayU, and SEPA all support webhooks for real-time payment updates:

GoPay allows merchants to configure webhook notifications in their Merchant Center settings. These webhooks notify businesses about payment status changes.

PayU provides webhook support for payments, sending server-to-server (S2S) callbacks to merchants when transactions succeed or fail. Merchants can configure webhooks via the PayU dashboard.

SEPA payments, when processed through Stripe, require webhooks to notify merchants about transaction status updates. Since SEPA Direct Debit payments can take days to settle, webhooks ensure businesses receive timely updates.

Would you like help setting up webhooks for one of these providers in Odoo? 🚀





could you coding it for each
Absolutely! I'll provide webhook integration code for GoPay, PayU, and SEPA in Odoo.

1. GoPay Webhook Integration (gopay_webhook.py)
GoPay sends webhook notifications when payment statuses change. Here's how to handle them in Odoo:

python
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
GoPay sends webhook notifications when payments succeed or fail.

You need to register your webhook URL in the GoPay Merchant Center.

2. PayU Webhook Integration (payu_webhook.py)
PayU provides server-to-server (S2S) callbacks for payment updates.

python
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
PayU requires merchants to register their webhook URL in the PayU dashboard.

This ensures real-time updates for payment success or failure.

3. SEPA Webhook Integration (sepa_webhook.py)
SEPA payments (via Stripe) require webhook handling for payment_intent.succeeded and payment_intent.payment_failed.

python
import logging
from odoo import http
import json

_logger = logging.getLogger(__name__)

class SEPAWebhookController(http.Controller):
    @http.route('/sepa/webhook', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_webhook(self, **post):
        """ Process SEPA webhook event """
        try:
            data = json.loads(http.request.httprequest.data)
            _logger.info(f"Received SEPA webhook: {data}")

            transaction_id = data.get("id")
            status = data.get("status")

            payment = http.request.env["sepa.integration"].search([("transaction_id", "=", transaction_id)], limit=1)
            if payment:
                payment.status = status
                _logger.info(f"Updated SEPA transaction {transaction_id} to status: {status}")
                return {"message": "Status updated successfully"}

            _logger.warning(f"SEPA transaction {transaction_id} not found")
            return {"error": "Transaction not found"}

        except Exception as e:
            _logger.error(f"Error processing SEPA webhook: {str(e)}")
            return {"error": "Internal server error"}
SEPA payments via Stripe require webhook registration in the Stripe Dashboard.

Webhooks notify merchants when payments succeed or fail.

Next Steps
Register Webhooks – Add your webhook URLs in GoPay, PayU, and Stripe dashboards.

Enable Logging – Monitor webhook events using tail -f odoo.log | grep "WebhookController".

Test Webhooks – Use sandbox environments to verify webhook responses.
