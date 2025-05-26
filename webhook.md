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
