#This file is part of the account_ar module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
{
    'name': 'Account Argentina',
    'name_es_AR': 'Plan de cuentas Argentino Demo',
    'name_es_ES': 'Plan de cuentas Argentino Demo',
    'version': '2.4.0',
    'author': 'Thymbra - Torre de Hanoi',
    'email': 'info@thymbra.com',
    'website': 'http://www.thymbra.com/',
    'description': '''Define an account chart template for Argentina.
Usefull to create a Argentinian account chart with the wizard in
"Financial Management>Configuration>General Account>Create Chart of Account from Template".
''',
    'description_es_AR': '''Define una plantilla de plan de cuentas para Argentina.
Útil para crear un plan de cuentas Argentino con el wizard en
"Gestión financiera>Configuración>Contabilidad general>Crear plan contable desde una plantilla"
''',
    'description_es_ES': '''Define una plantilla de plan de cuentas para Argentina.
Útil para crear un plan de cuentas Argentino con el wizard en
"Gestión financiera>Configuración>Contabilidad general>Crear plan contable desde una plantilla"
''',
    'depends': [
        'account',
    ],
    'xml': [
        'account_ar.xml',
        'tax_ar.xml',
    ],
}
