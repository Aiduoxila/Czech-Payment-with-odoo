<odoo>
    <record id="view_czech_payment_config_settings" model="ir.ui.view">
        <field name="name">czech.payment.config.settings</field>
        <field name="model">res.config.settings</field>
        <field name="arch" type="xml">
            <form string="Czech Payment Integration Settings">
                <sheet>
                    <group>
                        <field name="gopay_api_key" string="GoPay API Key"/>
                        <field name="payu_api_key" string="PayU API Key"/>
                        <field name="sepa_api_key" string="SEPA API Key"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
