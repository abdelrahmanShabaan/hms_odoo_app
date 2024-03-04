# -*- coding: utf-8 -*-
{
    'name': "HMS App",
    'description': "HMS App",
    'aurthor': 'Abdelrahman Shaaban',
    'category': "Services",
    'version': "17.0.0.1.0",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/patient/hms_patient.xml',
        'views/patient/patient_menus.xml',
        'views/department/hms_department.xml',
        'views/Doctors/hms_doctors.xml',
        'views/LogHistory/hms_logging.xml',
        'views/Customer/crm_customer_view.xml',
    ]
}
