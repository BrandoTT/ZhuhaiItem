import TinderPy
from typing import List
def print_force_info(force:TinderPy.SimForce)->None:
    print("name: ",force.get_name()," id: ",force.get_id()," equipment_id:",force.get_equipment_id()," team: ",force.get_team()," type: ",force.get_type())
    print("location: ",force.get_lon(),",",force.get_lat(),",",force.get_alt())
    print("posture: ",force.get_heading(),",",force.get_pitch(),",",force.get_speed(),",",force.get_roll())
    print("valid: ",force.is_valid()," life: ",force.get_life())
    
    
def lla2str(lla : TinderPy.LLA):
    if lla == None :
        return ""
    return str(lla.lon)+','+str(lla.lat)+','+str(lla.alt)
    
def llas2str(llas : List[TinderPy.LLA]):
    if llas == None or len(llas)==0:
        return ""
    res=""
    for i,lla in enumerate(llas):
        if i != 0:
            res +="_"
        res += lla2str(lla) 
    return res