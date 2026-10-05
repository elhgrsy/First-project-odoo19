{
    "name": "App one",
    "version": "19.0.0.1.0",
    "author": "Mohamed Hamdy",
    "summary": "App one",
    "category": "",

    "depends": [
        'base', 'account', 'sale_management', 'mail'
    ],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/property_history_views.xml',
        'views/base_action.xml',
        'views/field_action.xml',
        'views/owner_action.xml',
        'views/tags_action.xml',
        'views/customer_invoices_inharit.xml',
        'wizerd/wizer_change_state_views.xml',
		"report/property_report.xml",
],

    "application": True,
    "installable": True,
}
