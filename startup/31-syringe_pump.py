import asyncio
import time
from ophyd import EpicsMotor
from epics import caput
from epics import caget

from ophyd import (EpicsMotor, PVPositioner, Device, EpicsSignal,
                   EpicsSignalRO,PVPositionerPC)
from ophyd import (Component as Cpt, FormattedComponent,
                   DynamicDeviceComponent as DDC)
                  
 
                   
class Syringe_Pump(Device):
    "Syringe pump controller"
    
    vol_sp = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:Vol-SP'%i, {}) for i in range(1, 3)})
    vol_rb = DDC({'p%d' % i: (EpicsSignalRO, '{Pmp:%s}Val:Vol-RB'%i, {}) for i in range(1, 3)})
    
    rate_sp = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:Rate-SP'%i, {}) for i in range(1, 3)})
    rate_rb = DDC({'p%d' % i: (EpicsSignalRO, '{Pmp:%s}Val:Rate-RB'%i, {}) for i in range(1, 3)})
    
    dia_sp = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:Dia-SP'%i, {}) for i in range(1, 3)})
    dia_rb = DDC({'p%d' % i: (EpicsSignalRO, '{Pmp:%s}Val:Dia-RB'%i, {}) for i in range(1, 3)})
    
    dir_sp   =   DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:Dir-Sel'%i, {}) for i in range(1, 3)})
    dir_rb   =   DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:Dir-Sts'%i, {}) for i in range(1, 3)})
    
    vol_unit_sp = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Unit:Vol-Sel'%i, {}) for i in range(1, 3)})
    rate_unit_sp = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Unit:Rate-Sel'%i, {}) for i in range(1, 3)})      
    vol_unit_rb = DDC({'p%d' % i: (EpicsSignalRO, '{Pmp:%s}Unit:Vol-Sel'%i, {}) for i in range(1, 3)})
    rate_unit_rb = DDC({'p%d' % i: (EpicsSignalRO, '{Pmp:%s}Unit:Rate-Sel'%i, {}) for i in range(1, 3)})     
      
    
    Run   =    DDC({'p%s' % i: (EpicsSignal, '{Pmp:%s}Cmd:Run-Cmd'%i, {}) for i in [1,2,'All'] } )  
    Stop   =   DDC({'p%s' % i: (EpicsSignal, '{Pmp:%s}Cmd:Stop-Cmd'%i, {}) for i in [1,2,'All'] } ) 
    Purge  =   DDC({'p%s' % i: (EpicsSignal, '{Pmp:%s}Cmd:Purge-Cmd'%i, {}) for i in [1,2,'All'] } ) 
          
    disI_vol_rb = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:InfDisp-I'%i, {}) for i in [1,2] } ) 
    disI_unit_rb = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:InfDisp-I.EGU'%i, {}) for i in [1,2] } )
    
    disW_vol_rb = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:WdlDisp-I'%i, {}) for i in [1,2] } ) 
    disW_unit_rb = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Val:WdlDisp-I.EGU'%i, {}) for i in [1,2] } )    
    
    Clr = DDC({'p%d' % i: (EpicsSignal, '{Pmp:%s}Cmd:Clr-Cmd'%i, {}) for i in [1,2] } ) 
         
   
    
    p='All'
    run_all = Cpt(EpicsSignal, '{Pmp:%s}Cmd:Run-Cmd'%p)
    purge_all = Cpt(EpicsSignal, '{Pmp:%s}Cmd:Purge-Cmd'%p)
    stop_all = Cpt(EpicsSignal, '{Pmp:%s}Cmd:Stop-Cmd'%p)    
     
    def get_vol( self, pump =1 ):
        if pump==1:
            return self.vol_rb.p1.value
        else:
            return self.vol_rb.p2.value
            
    def get_vol_unit( self, pump =1 ):
        if pump==1:
            return self.vol_unit_rb.p1.value
        else:
            return self.vol_unit_rb.p2.value 
               
    def set_vol_unit( self, pump =1 ):
        if pump==1:
            return self.vol_unit_sp.p1.value
        else:
            return self.vol_unit_sp.p2.value  
            
    def get_rate_unit( self, pump =1 ):
        if pump==1:
            return self.rate_unit_rb.p1.value
        else:
            return self.rate_unit_rb.p2.value 
               
    def set_rate_unit( self, pump =1 ):
        if pump==1:
            return self.rate_unit_sp.p1.value
        else:
            return self.rate_unit_sp.p2.value    
                                           
            
    def set_vol( self, val, pump =1 ):
        if pump==1:
            return self.vol_sp.p1.set( val) 
        else:
            return self.vol_sp.p2.set( val) 
            
    def get_rate( self, pump =1 ):
        if pump==1:
            return self.rate_rb.p1.value
        else:
            return self.rate_rb.p2.value
            
    def set_rate( self, val, pump =1 ):
        if pump==1:
            return self.rate_sp.p1.set( val) 
        else:
            return self.rate_sp.p2.set( val) 
            
    def get_dia( self, pump =1 ):
        if pump==1:
            return self.dia_rb.p1.value
        else:
            return self.dia_rb.p2.value
            
    def set_dia( self, val, pump =1 ):
        if pump==1:
            return self.dia_sp.p1.set( val) 
        else:
            return self.dia_sp.p2.set( val)
            
    def get_dir( self, pump =1 ):
        if pump==1:
            return self.dir_rb.p1.value
        else:
            return self.dir_rb.p2.value
            
    def set_dir( self, val, pump =1 ):
        if pump==1:
            return self.dir_sp.p1.set( val) 
        else:
            return self.dir_sp.p2.set( val)  
            
    def run( self, pump=1 ):
         if pump==1:
            return self.Run.p1.set(1) 
         elif pump==2:
            return self.Run.p2.set(1)                 
         else:
            return sp.Run.pAll.set(1)           
            
    def stop( self, pump=1 ):
         if pump==1:
            return self.Stop.p1.set(1) 
         elif pump==2:
            return self.Stop.p2.set(1)                 
         else:
            return self.Stop.pAll.set(1)      
            
    def get_disvol( self,  pump=1, Dir=None, ): 
        '''dir: 0 for infusion, 1 for withdraw '''
        if Dir is None:
            Dir = self.get_dir(   pump  ) 
        if Dir ==0:
            if pump==1:
                return self.disI_vol_rb.p1.value
            else:
                return self.disI_vol_rb.p2.value  
        else:
            if pump==1:
                return self.disW_vol_rb.p1.value
            else:
                return self.disW_vol_rb.p2.value   
           
    def clr( self,  pump=1, Dir=None, ): 
        '''dir: 0 for infusion, 1 for withdraw '''
        if Dir is None:
            Dir = self.get_dir(   pump  ) 
        if pump==1:
            return self.Clr.p1.set( Dir )   
        else:
            return self.Clr.p2.set( Dir )   
                          
    
    @property
    def hints(self):
        fields = []
        for name in self.component_names:
            motor = getattr(self, name)
            fields.extend(motor.hints['fields'])
        return {'fields': fields}                   

SP = Syringe_Pump( 'XF:11IDB-ES', name='sp'  )   
 
  


class syringe_pump_old():
    def __init__( self ):
    
        self.vol_units = ['ul', 'ml']
        self.rate_units = ['ul/min', 'ml/min','ul/h', 'ml/h' ]     
        self.direction_units = ['infuse', 'withdraw', 'reverse', 'sticky' ] 
           
        self.pump_name = 'NE_1002X'
        
        self.PV_set_vol = 'XF:11IDB-ES{Pmp:%s}Val:Vol-SP'
        self.PV_get_vol = 'XF:11IDB-ES{Pmp:%s}Val:Vol-RB'
        self.PV_set_rate = 'XF:11IDB-ES{Pmp:%s}Val:Rate-SP'
        self.PV_get_rate = 'XF:11IDB-ES{Pmp:%s}Val:Rate-RB'
        self.PV_vol_unit =     'XF:11IDB-ES{Pmp:%s}Unit:Vol-Sel'
        self.PV_rate_unit =     'XF:11IDB-ES{Pmp:%s}Unit:Rate-Sel'
        self.PV_diameter = 'XF:11IDB-ES{Pmp:%s}Val:Dia-RB'
        self.PV_direction = 'XF:11IDB-ES{Pmp:%s}Val:Dir-Sel'
        self.PV_run = 'XF:11IDB-ES{Pmp:%s}Cmd:Run-Cmd'
        self.PV_purge_ = 'XF:11IDB-ES{Pmp:%s}Cmd:Purge-Cmd'
        self.PV_stop = 'XF:11IDB-ES{Pmp:%s}Cmd:Stop-Cmd'
        self.PV_run_all = 'XF:11IDB-ES{Pmp:All}Cmd:Run-Cmd'
        self.PV_purge_all = 'XF:11IDB-ES{Pmp:All}Cmd:Purge-Cmd'
        self.PV_stop_all = 'XF:11IDB-ES{Pmp:All}Cmd:Stop-Cmd'
        self.PV_dispense_inf_vol = 'XF:11IDB-ES{Pmp:%s}Val:InfDisp-I'  
        self.PV_dispense_inf_vol_unit = 'XF:11IDB-ES{Pmp:%s}Val:InfDisp-I.EGU'  
        self.PV_dispense_wid_vol = 'XF:11IDB-ES{Pmp:%s}Val:WdlDisp-I'  
        self.PV_dispense_wid_vol_unit = 'XF:11IDB-ES{Pmp:%s}Val:WdlDisp-I.EGU'               


    def get_dispense_vol_val(self, pump=1, direct=0):
        if direct==0:
            return caget( self.PV_dispense_inf_vol%pump )
        else:
            return  caget( self.PV_dispense_wid_vol%pump )

    def get_dispense_vol(self,  pump=1):           
        direct = caget( self.PV_direction%pump )
        if direct == 0:
           dis = caget( self.PV_dispense_inf_vol%pump )
           dis_u = caget(  self.PV_dispense_inf_vol_unit%pump ) 
           print('The infusion vol is %s (%s).'%( dis, dis_u)  )  
        else:
           dis = caget( self.PV_dispense_wid_vol%pump )
           dis_u = caget(  self.PV_dispense_wid_vol_unit%pump ) 
           print('The withdraw vol is %s (%s).'%( dis, dis_u)  )           
        return dis  
        
    def purge_all(self):
        caput(  self.PV_purge_all, 1 ) 
    def pause_all(self):
        caput(  self.PV_stop_all, 1 )        
        #caput(  self.PV_stop_all, 1 )          
    def stop_all(self):
        caput(  self.PV_stop_all, 1 )        
        caput(  self.PV_stop_all, 1 )              
    def run_all(self):
        caput(  self.PV_run_all, 1 )   
          
    def purge(self, pump=1):
        caput(  self.PV_purge%pump, 1 ) 
    def stop(self, pump=1):
        caput(  self.PV_stop%pump, 1 )        
        caput(  self.PV_stop%pump, 1 )   
    def pause(self, pump=1):
        caput(  self.PV_stop%pump, 1 )        
        #caput(  self.PV_stop%pump, 1 )                   
    def run(self, pump=1):
        caput(  self.PV_run%pump, 1 )         
               
    def set_direction(self, direct,  pump=1):   
        caput( self.PV_direction%pump, direct )
        print('Set the direction of the pump %s as %s.'%(pump, self.direction_units[direct]) )    
        
    def get_direction(self,  pump=1):   
        direct = caget( self.PV_direction%pump )
        print('The direction of the pump %s is %s .'%(pump, self.direction_units[direct]) )    
        return self.direction_units[direct]        

    def set_diamter(self, dia,  pump=1):   
        caput( self.PV_diameter%pump, dia )
        print('Set the diameter of the pump %s as %s mm.'%(pump, dia) )    
        
    def get_diamter(self,  pump=1):   
        dia = caget( self.PV_diameter%pump )
        print('The diameter of the pump %s is %s mm.'%(pump, dia) )    
        return dia               
        
    def set_vol_unit(self, unit, pump=1):
        '''unit: 0, ul; 
                 1, ml
        '''        
        caput( self.PV_vol_unit%pump, unit)
        print('Set the volume unit of the pump %s as %s.'%(pump, self.vol_units[unit] ) )    
        
    def get_vol_unit(self,  pump=1):
        '''unit: 0, ul; 
                 1, ml
        '''        
        unit = caget( self.PV_vol_unit%pump )        
        #print('The volume unit of the pump  %s is %s.'%(pump, self.vol_units[unit] ) ) 
        return self.vol_units[unit]
        
    def set_rate_unit(self, unit, pump=1):
        '''unit: 'ul/min', 'ml/min','ul/h', 'ml/h'
                 
        '''        
        caput( self.PV_rate_unit%pump, unit)
        print('Set the rate unit of the pump %s as %s.'%(pump, self.rate_units[unit] )    )
        
    def get_rate_unit(self, unit, pump=1):
        '''unit: 'ul/min', 'ml/min','ul/h', 'ml/h'                 
        '''        
        unit = caget( self.PV_rate_unit%pump)
        #print('The rate unit of the pump %s is %s.'%(pump, self.rate_units[unit] )   )            
        return self.rate_units[unit]    
        
    def set_vol(self, vol, pump=1):
        caput( self.PV_set_vol%pump, vol)
        print('Set the liquid volume of the pump %s as %s.'%(pump, vol) ) 
        
    def get_vol(self,  pump=1):
        vol = caget( self.PV_get_vol%pump )
        unit = self.get_vol_unit( pump ) 
        print('The liquid volume of the pump %s is %s (%s).'%(pump, vol, unit )  ) 
        return vol       
        
    def set_rate(self, rate, pump=1):
        caput( self.PV_set_rate%pump, rate)
        print('Set the rate of the pump %s as %s.'%(pump, rate) )
        
    def get_rate(self,  pump=1):
        rate = caget( self.PV_get_rate%pump )
        unit = self.get_rate_unit( pump )         
        print('The rate of the pump %s is %s (%s).'%(pump, rate, unit) )
        return rate    
        
            
    
#syp =     syringe_pump()






















