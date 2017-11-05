#! -*- encoding: utf-8 -*-
#    2015 Rui Pedrosa Franco All Rights Reserved
#    http://pt.linkedin.com/in/ruipedrosafranco
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

# from __future__ import division
from odoo import api, fields, models, _
from odoo.exceptions import Warning as UserWarning
from decimal import Decimal
import math


class gps_base_base(models.Model):
    _name='gps_base.base'

    #in wich format has the user decided to see/insert coordinates?
    def _get_user_coords_format(self):
        user_res=self.env['res.users'].read('coords_format')
        user_coords_format=user_res['coords_format'] and user_res['coords_format'] or 'dd'
        return user_coords_format


    #**********************************************************
    # conversion functions
    #**********************************************************

    def convert_dd_ddm(self, lat=False, long=False):
        res=[(0,0),(0,0)]
        if lat and long:
            res=[lat, long]
            for i in range(2):
                degrees=int(res[i])
                minutes=(res[i]-degrees)*60
                res[i]=(degrees,minutes)
        return res

    def convert_dd_dms(self, lat=False, long=False):
        res=[(0,0,0),(0,0,0)]
        if lat and long:
            res=[lat, long]
            for i in range(2):
                degrees=int(res[i])
                minutes=int(60*(res[i]-degrees))
                seconds=3600*(res[i]-degrees-minutes/60)
                res[i]=(degrees,minutes,seconds)
        return res

    # TO DO
    def convert_ddm_dd(self, lat=False, long=False):
        res=[0,0]
        
        #Degrees Minutes.m to Decimal Degrees
        #.d = M.m / 60
        #Decimal Degrees = Degrees + .d
        """
        if lat and long:
            res=[lat, long]
            for i in range(2):
        """
        
        #raise osv.except_osv(_('Error'),_(res))
        return res

    # TO DO
    def convert_dms_dd(self, lat=False, long=False):
        res=[0,0]
        return res


    #**********************************************************
    # format functions
    #**********************************************************


    def latChar(self, coord):
        char='N'
        if coord<0:
            char='S'
        return char + ' '

    def longChar(self, coord):
        char='W'
        if coord>0:
            char='E'
        return char + ' '
    
    def dd_format(self, lat=False, long=False):
        #decimal degrees: N 40.446°, W 79.982°
        res=''
        if lat and long:
            res=self.latChar(lat) + str(abs(lat)) + 'º, ' + self.longChar(long) + str(abs(long)) + 'º'
        return res
    
    def ddm_format(self, lat=False, long=False):
        #degrees decimal minutes: N 40° 26.767′, W 79° 58.933′
        res=''
        if lat and long:
            conv=self.convert_dd_ddm(lat, long)
            
            lat=self.latChar(conv[0][0]) + str(abs(conv[0][0])) + 'º ' + str(abs(conv[0][1]))
            long=self.longChar(conv[1][0]) + str(abs(conv[1][0])) + 'º ' + str(abs(conv[1][1]))
            res=lat +', '+long
        return res
    
    def dms_format(self, lat=False, long=False):
        #degrees minutes seconds: N 40° 26′ 46″, W 79° 58′ 56″
        res=''
        if lat and long:
            conv=self.convert_dd_dms(lat, long)
            lat=self.latChar(conv[0][0]) + str(abs(conv[0][0])) + 'º ' + str(abs(conv[0][1])) + "' " + str(abs(conv[0][2])) + '"'
            long=self.longChar(conv[1][0]) + str(abs(conv[1][0])) + 'º ' + str(abs(conv[1][1])) + "' " + str(abs(conv[1][2])) + '"'
            res=lat +', '+long
        return res
     

    #**********************************************************
    # validation functions
    #**********************************************************
     
    """
    Gets a coord (in "natural" input format) and returns an array with its parts converted to elements.
    Thus, N 30.356 becomes [30,356] and W 1º 33' 10.8 becomes [1,33,10,8].
    """
    def clean_coords(self, coord):
        res=[]
        if coord:
            aux=str(coord).strip()
            for c in ['º','"',"'"]:
                aux=aux.replace(c,'.')

            for c in [' ','N','n','W','w']:
                aux=aux.replace(c,'')
                
            res=aux.split('.')
            last_pos=len(res)-1
            if not res[last_pos]:
                del res[last_pos]
                
            res=[int(i) for i in res]
                
        return res


    #validation of input in the dd format - N 40.446°, W 79.982°
    def dd_validate(self, lat=False, long=False):
        res=True
        
        if lat and long:
            lat=self.clean_coords(lat)

            if len(lat)==1:
                lat.append(0)
            
            if len(lat)==2:
                #degrees
                if lat[0]<-90 or lat[0]>90:
                    res=False

                #decimals
                lat[1]=str(abs(lat[1]))
                if len(lat[1])>8:
                    res=False
            else:
                res=False

            long=self.clean_coords(long)
            if len(long)==1:
                long.append(0)

            if len(long)==2:
                #degrees
                if long[0]<-180 or long[0]>180:
                    res=False

                #decimals
                long[1]=str(abs(long[1]))
                if len(long[1])>8:
                    res=False
            else:
                res=False
        else:
            res=False

        if not res:
            error_msg='Coordinates are not in the right format (DD).'
            error_msg+='\n\nExamples:\n'
            error_msg+='N 40.446°, W 79.982°\nN40.446°, W 79.982\n40.446, W79.982º'
            raise osv.except_osv(_('Error'),_(error_msg))
        else:
            #if coords are alright, the method returns a clean version of them
            aux_lat=float(str(lat[0]) + '.' + str(lat[1])) 
            aux_long=float(str(long[0]) + '.' + str(long[1]))
            res=[aux_lat, aux_long]
            
        return res


    
    def ddm_validate(self, lat=False, long=False):
        return True
    
    def dms_validate(self, lat=False, long=False):
        return True




class gps_base_coords(models.Model):

    _name = 'gps_base.coords'


    def name_get(self, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]

        reads = self.read(ids, ['user_coords', 'country_id'], context=context)
        res = []
        for record in reads:
            name = record['user_coords']
            if record['country_id']:
                name = name + ' (' + record['country_id'][1] + ')'
            res.append((record['id'], name))
        return res

    #this shows coords in the format the user has defined in his preferences
    def _get_user_coords(self, ids):
        res={}
        
        for i in ids:
            this=self.browse(i)
            res[i]=eval('this.' + self.env['gps_base.base']._get_user_coords_format() + '_coords')
        return res  

        
    def _get_dd_coords(self, ids):
        res={}
        for i in ids:
            this=self.browse(i)
            res[i]=self.env['gps_base.base'].dd_format(this.latitude, this.longitude)
        return res    
    
    def _get_ddm_coords(self, ids, field_name, arg, context):
        res={}
        for i in ids:
            this=self.browse(i)
            res[i]=self.env['gps_base.base'].ddm_format(this.latitude, this.longitude)
        return res    

    def _get_dms_coords(self,ids, field_name, arg, context):
        res={}
        for i in ids:
            this=self.browse(i)
            res[i]=self.env['gps_base.base'].dms_format(this.latitude, this.longitude)
        return res    

    def create(self, vals, context=None):
    
        user_coords_format = self.env['gps_base.base']._get_user_coords_format()
        user_coords_format = vals.get('format_aux', user_coords_format)
        method_to_use = "self.pool.get('gps_base.base')." + user_coords_format + '_validate'

        latitude_aux = vals['latitude_aux']
        longitude_aux = vals['longitude_aux']
        
        #validation of the user input
        val_res=eval(method_to_use)(cr, uid, latitude_aux, longitude_aux)


        #if coordinates are ok
        #we convert the coordinates to dd format so that they can be saved
        if val_res:
            #no need to convert if coords are already in dd format
            if user_coords_format == 'dd':
                vals['latitude'], vals['longitude'] = val_res
            else:
                method_to_use="self.env['gps_base.base']." + 'convert_' + user_coords_format + '_dd'

                #raise osv.except_osv(_('Warning!'),_(method_to_use))

                vals['latitude'], vals['longitude'] = eval(method_to_use)(latitude_aux, longitude_aux)


            vals['latitude_aux']  = vals['latitude']
            vals['longitude_aux'] = vals['longitude']
            vals['format_aux']    = 'dd'
        

        #raise osv.except_osv(_('Warning!'),_(vals) + '\n' + _(val_res))
        
        try:
            aux=super(gps_base_coords, self).create(cr, uid, vals, context=context)
        except:
            raise UserWarning(_('Error!'), _('Check if you entered the coordinates in the right format (%s)') % (user_coords_format))
        
        return aux


    def write(self, ids, vals, context=None):
    
        if not isinstance(ids,(list,tuple)):
            ids=[ids]
    
        #how to do the validation of the user input
        user_coords_format=self.env['gps_base.base']._get_user_coords_format()
        if 'format_aux' in vals:
            user_coords_format=vals.get('format_aux', user_coords_format)
        method_to_use="self.pool.get('gps_base.base')." + user_coords_format + '_validate'

        for this in self.browse(ids):

            latitude_aux=this.latitude_aux
            if 'latitude_aux' in vals:
                latitude_aux=vals['latitude_aux']
                
            longitude_aux=this.longitude_aux
            if 'longitude_aux' in vals:
                longitude_aux=vals['longitude_aux']
        
            #validation of the user input
            val_res=eval(method_to_use)(latitude_aux, longitude_aux)

            #if coordinates are ok
            #we convert the coordinates to dd format so that they can be saved
            if val_res:
                #no need to convert if coords are already in dd format
                if user_coords_format == 'dd':
                    vals['latitude'], vals['longitude'] = val_res
                else:
                    method_to_use="self.env['gps_base.base']." + 'convert_' + user_coords_format + '_dd'
                    vals['latitude'], vals['longitude'] = eval(method_to_use)(latitude_aux, longitude_aux)


                vals['latitude_aux']  = vals['latitude']
                vals['longitude_aux'] = vals['longitude']
                vals['format_aux']    = 'dd'
        
            #raise osv.except_osv(_('Warning!'),_(vals) + '\n' + _(val_res))
        
        return super(gps_base_coords, self).write(ids, vals, context=context)


    country_id = fields.Many2one(comodel_name='res.country', string='Country')
        
        #***********************************************************
        # fields for entering data
        #***********************************************************
    latitude_aux = fields.Char(string='Latitude (N)',size=15, required=True)
    longitude_aux = fields.Char(string='Longitude (W)',size=15, required=True)
    format_aux = fields.Selection(selection=[
        ('dd','Decimal degrees: N 40.446°, W 79.982°'),
        ('ddm',"Degrees decimal minutes: N 40° 26.767′, W 79° 58.933′"),
        ('dms',"Degrees minutes seconds: N 40° 26′ 46″, W 79° 58′ 56''"),
        ], default='dd', help='This is the format against wich coordinates '
                              'will be validated',string='Coordinate format')
        #coordinates are always saved in the decimal degrees format (N 40.446°, W 79.982°)
    latitude = fields.Float(string='Latitude',digits=(9,6), readonly=True, help='Decimal degrees format')
    longitude = fields.Float('Longitude',digits=(9,6), readonly=True, help='Decimal degrees format')
    #coordinates in the format the user has chosen
    user_coords = fields.Float(compute=_get_user_coords, type='char', method=True, string='Coords')

        #***********************************************************
        # functional fields to show coordinates in all three formats
        #***********************************************************
    dd_coords = fields.Float(compute=_get_dd_coords,  type='char', method=True, string='Decimal degrees format')
    ddm_coords = fields.Float(compute=_get_ddm_coords, type='char', method=True, string='Degrees decimal minutes format')
    dms_coords = fields.Float(compute=_get_dms_coords, type='char', method=True, string='Degrees minutes seconds format')




