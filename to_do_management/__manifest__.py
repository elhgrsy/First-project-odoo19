{
    "name": "To Do App",
    "version": "19.0.0.1.0",
    "category": "",
    "summary": "To Do App",
    "author": "Mohamed Hamdy",
    "depends": ['base','mail','sale_management'
                ],
    "data": [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/to_do_history_action_field.xml',
        'views/base_action_todo.xml',
        'views/to_do_action_field.xml',
        'views/sale_inhirent.xml',
        'wizard/views_wizard.xml',
        'report/report_action.xml'
    ],
    "installable": True,
    "application": True,


}