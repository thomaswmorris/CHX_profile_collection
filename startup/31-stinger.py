import asyncio
import time
from ophyd import EpicsMotor
from epics import caput
from epics import caget
from math import radians
from IPython.core.magic import Magics, magics_class, line_magic
from bluesky import RunEngine
from bluesky.utils import ProgressBarManager
from bluesky.plan_stubs import rd
from matplotlib import cm

  
def set_stinger_temperature(Tsetpoint,heat_ramp=3,cool_ramp=0,log_entry='on',check_vac=True):    
    """
    heating with Stinger sample chamber, using both heaters
    macro maintains 40deg difference between both heaters to have a temperature gradient for stabilization
    Tsetpoint: temperature setpoint in deg Celsius!
    heat_ramp: ramping speed [deg.C/min] on heating. Currently a ramp with max 3deg.C/min will be enforced!
    cool_ramp: ramping speed [deg.C/min] on cooling. '0' -> ramp off!
    log_entry: 'on' / 'off'  -> make olog entry when changing temperature ('try', ignored, if Olog is down...)
    check_vac: True/False -> checks for vacuum level on hard-coded PV for temperatures > 50C or <10C
    """
    vac_check_PV='XF:11IDB-VA{Samp:1-TCG:1}P-I'
    if check_vac:
        vac=caget(vac_check_PV)
        if vac > .1:
            raise ValueError('vacuum in sample chamber needs to be better than .1 for T>50C or T<10C!')
        else:
            print('vacuum in sample chamber: %s Torr -> passed vacuum check!'%vac)
    
    if heat_ramp > 7.:
        heat_ramp=7.
    else: pass
    if cool_ramp==0:
        cool_ramp_on=0
    else:  cool_ramp_on=1
    
    start_T=caget('XF:11IDB-ES{Env:01-Chan:C}T:C-I')
    start_T2=caget('XF:11IDB-ES{Env:01-Chan:B}T:C-I')
    if start_T >= Tsetpoint:        # cooling requested 
        caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',0)  # ramp off
        caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',0)                          
        caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+start_T)    # start from current temperature
        caput('XF:11IDB-ES{Env:01-Out:2}T-SP',273.15+start_T2)
        if cool_ramp==0:                                                                                # print message and make Olog entry, if requested
            print('cooling Channel C to '+str(Tsetpoint)+'deg, no ramp')
            RE(sleep(5))  # need time to update setpoint....
            if log_entry == 'on':
                try:
                    olog_client.log( 'Changed temperature to T='+ str(Tsetpoint)[:5]+'C, ramp: off')
                except:
                    pass
            else: pass
        elif cool_ramp >0:
            print('cooling Channel C to '+str(Tsetpoint)+'deg @ '+str(cool_ramp)+'deg./min')    
            if log_entry == 'on':
                try:
                    olog_client.log( 'Changed temperature to T='+ str(Tsetpoint)[:5]+'C, ramp: '+str(cool_ramp)+'deg./min')
                except:
                    pass
            else: pass
        #caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',cool_ramp_on)        #switch ramp on/off as requested
        #caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',cool_ramp_on)
        caput('XF:11IDB-ES{Env:01-Out:1}Val:Ramp-SP',cool_ramp,wait=True)   # set ramp to requested value
        caput('XF:11IDB-ES{Env:01-Out:2}Val:Ramp-SP',cool_ramp,wait=True)
        RE(sleep(5))
        caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',cool_ramp_on,wait=True)        #switch ramp on/off as requested
        caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',cool_ramp_on,wait=True)
        caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+Tsetpoint)    # setting channel C to Tsetpoint
        caput('XF:11IDB-ES{Env:01-Out:2}T-SP',233.15+Tsetpoint) # setting channel B to Tsetpoint-40C
    elif start_T<Tsetpoint:        #heating requested, ramp on
        print('heating Channel C to '+str(Tsetpoint)+'deg @ '+str(heat_ramp)+'deg./min')
        RE(sleep(5))    
        if log_entry == 'on':
            try:
                olog_client.log( 'Changed temperature to T='+ str(Tsetpoint)[:5]+'C, ramp: '+str(heat_ramp)+'deg./min')
            except:
                pass
        else: pass
        caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',0,wait=True)  # ramp off
        caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',0,wait=True)
        caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+start_T)    # start from current temperature
        caput('XF:11IDB-ES{Env:01-Out:2}T-SP',273.15+start_T2)
        caput('XF:11IDB-ES{Env:01-Out:1}Val:Ramp-SP',heat_ramp,wait=True)   # set ramp to selected value or allowed maximum
        caput('XF:11IDB-ES{Env:01-Out:2}Val:Ramp-SP',heat_ramp,wait=True)
        #print('flashed yet??')
        #RE(sleep(5))
        caput('XF:11IDB-ES{Env:01-Out:1}Out:MaxI-SP',1.0) # force max current to 1.0 Amp
        caput('XF:11IDB-ES{Env:01-Out:2}Out:MaxI-SP',.7)
        caput('XF:11IDB-ES{Env:01-Out:1}Val:Range-Sel',3) # force heater range 3 -> should be able to follow 2deg/min ramp
        caput('XF:11IDB-ES{Env:01-Out:2}Val:Range-Sel',3)
        RE(sleep(5))
        caput('XF:11IDB-ES{Env:01-Out:1}Enbl:Ramp-Sel',1,wait=True)  # ramp on
        caput('XF:11IDB-ES{Env:01-Out:2}Enbl:Ramp-Sel',1,wait=True)
        caput('XF:11IDB-ES{Env:01-Out:1}T-SP',273.15+Tsetpoint)    # setting channel C to Tsetpoint
        caput('XF:11IDB-ES{Env:01-Out:2}T-SP',233.15+Tsetpoint) # setting channel B to Tsetpoint-40C
