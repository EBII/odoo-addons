#! -*- encoding: utf-8 -*-
#    2015 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class res_users(models.Model):

    _inherit = 'res.users'
    
    coords_format = fields.Selection(selection=[
        ('dd','Decimal degrees: N 40.446°, W 79.982°'),
        ('ddm',"Degrees decimal minutes: N 40° 26.767′, W 79° 58.933′"),
        ('dms',"Degrees minutes seconds: N 40° 26′ 46″, W 79° 58′ 56''"),
        ], string='Coordinate format', help='This is the format in which coord'
                                            'inates will be shown and entered',
        defaults = 'dd')
