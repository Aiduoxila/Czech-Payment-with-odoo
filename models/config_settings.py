from odoo import models, fields

class CzechPaymentConfigSettings(models.TransientModel):
    _name = 'res.config.settings'
    _inherit = 'res.config.settings'
    _description = 'Czech Payment Configuration Settings'

    gopay_api_key = fields.Char(string="GoPay API Key")
    payu_api_key = fields.Char(string="PayU API Key")
    sepa_api_key = fields.Char(string="SEPA API Key")

    def set_values(self):
        super(CzechPaymentConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('cz_payment_integration.gopay_api_key', self.gopay_api_key)
        self.env['ir.config_parameter'].sudo().set_param('cz_payment_integration.payu_api_key', self.payu_api_key)
        self.env['ir.config_parameter'].sudo().set_param('cz_payment_integration.sepa_api_key', self.sepa_api_key)

    def get_values(self):
        res = super(CzechPaymentConfigSettings, self).get_values()
        res.update({
            'gopay_api_key': self.env['ir.config_parameter'].sudo().get_param('cz_payment_integration.gopay_api_key'),
            'payu_api_key': self.env['ir.config_parameter'].sudo().get_param('cz_payment_integration.payu_api_key'),
            'sepa_api_key': self.env['ir.config_parameter'].sudo().get_param('cz_payment_integration.sepa_api_key'),
        })
        return res
