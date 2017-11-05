# -*- coding: utf-8 -*-
#    2015 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name'          : 'GPS - base functions',
	'version'       : '10.0.1.0.0',
	'category'      : 'Extra Tools',
	'summary'       : 'Base functionalities for the use of GPS coordinates',
	'description'   : """
Base GPS functions\n\n
- creates gps.coords records that can be associated to models
- coords are saved in the decimal degrees format
- users can choose wich coordinate format to use throughout Odoo
                        
PS: 
- map widget is based on Dorin Hongu's web_gmaps module
- JavaScript had an invaluable help from Dinil UD

MAKE SURE YOU CHECK MY OTHER MODULES AT... https://goo.gl/TteO1F
                        """,
	'author'        : 'Odooveloper (Rui Franco)',
	'website'       : 'http://www.odooveloper.com',
	'depends'       : ['web'],
	'data'          : [
                        'security/ir.model.access.csv',
                        'views/gps_base_view.xml',
                        'views/res_users_view.xml',
                        'views/web_gmaps_assets.xml',
                        ],
    'qweb'          : ['static/src/xml/resource.xml'],
    'installable'   : True,
    'active'        : False,
}
