import TinderPy
from define import RescEnum,EntityDomainEnum,AmbiguousMatcherEnum,ManeuverEnum,SizeEnum,DisruptorEnum
import json
from helper import lla2str,llas2str
from typing import List

# def json_str(resc_type:RescEnum,**info_dict):
    # res={}
    # if resc_type == RescEnum.pathway:
        # res["pathway"]={}
        # for key,val in info_dict.items():
            # res["pathway"][key] = val
        # return json.dumps(res)
    

def pathway_json(desireX : float = 0.0,
                desireY  : float = 0.0,
                desireZ  : float = 0.0,
                timeStep : float = 1.0
                ):
                
    '''
	用于device_control，命令号cmd : 2	    # 动力设备轨迹控制
    
    desireX;		# 本地坐标系(当前点为原点,北东地)，期望目标点的x坐标(北)
	desireY;		# 本地坐标系(当前点为原点,北东地)，期望目标点的y坐标(东)
	desireZ;		# 本地坐标系(当前点为原点,北东地)，期望目标点的z坐标(下)
	timeStep;		# 步长 单位:秒 (默认一秒)
    '''
    
    res ={
        "pathway":{
            "desireX":desireX,
            "desireY":desireY,
            "desireZ":desireZ,
            "timeStep":timeStep
        }
    }
    return json.dumps(res)
    
def posture_json(adjustAx : float = 0.0,
                adjustAy  : float = 0.0,
                adjustAz  : float = 0.0,
                adjustSpeed : float = 0.0
                ):
                
    '''
    用于device_control，命令号cmd : 3	    # 动力设备姿态控制
    
    adjustAx;		# 横滚轴调整量
	adjustAy;		# 俯仰轴调整量
	adjustAz;		# 偏航轴调整量
	adjustSpeed;	# 速度调整量
    '''
    res ={
        "posture":{
            "adjustAx":adjustAx,
            "adjustAy":adjustAy,
            "adjustAz":adjustAz,
            "adjustSpeed":adjustSpeed
        }
    }
    return json.dumps(res)

    
def switch_json(equipIndex : int = 0,
                isOn : bool = True
                ):
    '''
    用于device_control，命令号 cmd : 1，4，8，12，16，20，25	    # 动力，雷达，声纳，光学，电侦，武器，信息开关
    
	equipIndex;	# 指定设备编号,为负数时对应全体设备 (指定设备后使用switchMode赋值)
	isOn;		# 开机与否		
    '''

    res ={
        "switch":{
            "equipIndex":equipIndex,
            "switchMode":1 if isOn == True else -1,
            "isOn":isOn
        }
    }
    return json.dumps(res)
    
    
def extend_json(equipIndex : int = 0,
                x : float = 0.0,
                y : float = 0.0,
                z : float = 0.0
                ):
                
    '''
    用于device_control，命令号cmd : 5，9，13，17，21	    # 雷达，声纳，光学，电侦，武器延展
    
    equipIndex;	# 指定设备编号,为负数时对应全体设备(自动选择)
	x		# 向前延展至某一相对位置(相对于本体坐标系)
    y       # 向右延展至某一相对位置(相对于本体坐标系)
    z       # 向下延展至某一相对位置(相对于本体坐标系)
    '''
    res ={
        "extend":{
            "equipIndex":equipIndex,
            "toPosBody":f"{x},{y},{z}"
        }
    }
    return json.dumps(res)
     
     
def track_json( ID : int = 0, 
                aimLon : float = 0.0,
                aimLat : float = 0.0,
                aimAlt : float = 0.0,
                aimFreq : float = 0.0 ,
                appointing : int = 0
                ):     
    '''
    用于device_control，命令号cmd : 5，10，14，18	    # 雷达，声纳，光学，电侦跟踪
    
	ID;			        # 需求追踪目标ID
	aimLon;				# 建议瞄向经度
	aimLat;				# 建议瞄向纬度
	aimAlt;				# 建议瞄向高度
	aimFreq;			# 建议工作频率 单位: MHz, 等于零时候自动选择
	appointing;         # 指定设备, 为负数时自动选择
    '''
    res ={
        "track":{
            "id":ID,
            "aimLon":aimLon,
            "aimLat":aimLat,
            "aimAlt":aimAlt,
            "aimFreq":aimFreq,
            "appointing":appointing
        }
    }
    return json.dumps(res)
    
def search_json(aimLon : float = 0.0,
                aimLat : float = 0.0,
                aimAlt : float = 0.0,
                vextex : List[TinderPy.LLA] = [],
                appointing : int =0
                ):
                
    '''
    用于device_control，命令号cmd : 7，11，15，19	    # 雷达，声纳，光学，电侦搜索

    
    aimLon;				# 建议瞄向经度
	aimLat;				# 建议瞄向纬度
	aimAlt;				# 建议瞄向高度
	vextex;	            # 需求搜索区域, 非必要参数
	appointing;	        # 指定设备, 为负数时自动选择
    '''
    res ={
        "search":{
            "aimLon":aimLon,
            "aimLat":aimLat,
            "aimAlt":aimAlt,
            "vextex":llas2str(vextex),
            "appointing":appointing
        }
    }
    return json.dumps(res)
    
def strike_json(aimLocation : TinderPy.LLA,
                aimDomain   : EntityDomainEnum = EntityDomainEnum.EDE_NULL,
                matchIndex  : int = 0,
                matchType   : AmbiguousMatcherEnum = AmbiguousMatcherEnum.ABME_UNKNOWN,
                matchManeuv : ManeuverEnum = ManeuverEnum.MANEU_UNKNOWN,
                matchSize   : SizeEnum = SizeEnum.SIE_UNKNOWN,
                trajactory  : List[TinderPy.LLA] = [],
                ammoToFire  : int = 1,
                appointing  : int = 0,
                ammoToUse   : str = ""
                ):
    '''
    用于device_control，命令号cmd : 22	    # 武器系统开火
    
    # 对象信息(必要信息)
	aimLocation;    # 目标位置
	aimDomain;      # 目标基类 (如:水基,天基)

	# 匹配信息(无目标时不填写,有目标时候至少填写一项)
	matchIndex;		# 唯一标识匹配
	matchType;      # 模糊目标匹配
	matchManeuv;	# 机动性匹配
	matchSize;		# 尺寸匹配

	# 路径信息(选填,无默认值)
	trajactory;	    # 弹道规划

	# 发射信息(选填,有默认值)
	ammoToFire;		# 发射数量, 默认为1
	appointing;		# 指定设备, 默认自动选择
	ammoToUse;		# 指定弹药, 默认自动选择
    '''
    res ={
        "strike":{
            "aimLocation":lla2str(aimLocation),
            "aimDomain":aimDomain.value,
            "matchIndex":matchIndex,
            "matchType":matchType.value,
            "matchManeuv":matchManeuv.value,
            "matchSize":matchSize.value,
            "trajactory":llas2str(trajactory),
            "ammoToFire":ammoToFire,
            "appointing":appointing,
            "ammoToUse":ammoToUse
        }
    }
    return json.dumps(res)
    
def jaming_json(sid : int = 0,
                frequency : float = -999,
                mainDeflect : float = -999,
                mainElevate : float = -999,
                estiDistance : float = -999,
                appointing : int = 0
                ):
    '''
    用于device_control，命令号cmd : 23	    # 干扰控制
    
    sid;		    # 辐射源唯一标识
	frequency;		# 估算功率 单位:MHz
	mainDeflect;	# 建议偏角	单位:度 (北东地坐标系)
	mainElevate;	# 建议仰角 单位:度 (北东地坐标系)
	estiDistance;	# 估计距离(<=零代表无法无法估计) 单位:米 
	appointing;		# 指定设备, 为负数时自动选择
    '''
    res ={
        "jaming":{
            "sid":sid,
            "frequency":frequency,
            "mainDeflect":mainDeflect,
            "mainElevate":mainElevate,
            "estiDistance":estiDistance,
            "appointing":appointing
        }
    }
    return json.dumps(res)
    
def decoy_json( valid : bool = False,
                toUse : DisruptorEnum = DisruptorEnum.DISR_NULL,
                deflection : float = -999,
                appointing : int = 0
                ):
    '''
       用于device_control，命令号cmd : 24	    # 诱饵弹
    
	valid;			# 是否有效(防止误操作)
	toUse;	        # 使用哪种诱饵手段
	eflection;		# 主发射方向, 默认(-999)自由选择, 单位:度
	appointing;		# 指定设备, 为负数时自动选择
    '''
    res ={
        "decoy":{
            "valid":valid,
            "toUse":toUse.value,
            "deflection":deflection,
            "appointing":appointing
        }
    }
    return json.dumps(res)    
    
def inform_json(content : str = "",
                target : int = 0,
                ):
    '''
    用于device_control，命令号cmd : 26	    # 诱饵弹
    
    content;	# 内容
	target;	    # 对象 (0:广播)
    '''
    res ={
        "inform":{
            "content":content,
            "target":target
        }
    }
    return json.dumps(res)    
    
