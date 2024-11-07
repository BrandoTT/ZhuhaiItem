"""
Tinder python interface
"""
from __future__ import annotations
__all__ = ['Attribute', 'DetectedSituation', 'EquipmentAmmo', 'EquipmentPlatform', 'Geometry', 'LLA', 'PlanInfo', 'SimDevice', 'SimEvent', 'SimForce', 'TEAM_BLUE', 'TEAM_RED', 'Variant', 'accelerate', 'check_connection', 'conduct', 'customize_publish', 'decelerate', 'device_control', 'get_blue_detected_situation', 'get_blue_force_by_id', 'get_blue_forces', 'get_blue_forces_by_type', 'get_current_speed', 'get_current_step', 'get_current_time', 'get_force_plans', 'get_geometries', 'get_geometry', 'get_plan', 'get_red_detected_situation', 'get_red_force_by_id', 'get_red_forces', 'get_red_forces_by_type', 'get_sim_events', 'log_debug', 'log_error', 'log_event', 'log_info', 'log_warning', 'post_event', 'terminate']
class Attribute:
    """
    属性
    """
    def __init__(self) -> None:
        ...
    @property
    def name(self) -> str:
        """
        属性名称
        """
    @name.setter
    def name(self, value: str) -> None:
        ...
    @property
    def value(self) -> str:
        """
        属性值
        """
    @value.setter
    def value(self, value: str) -> None:
        ...
class DetectedSituation:
    """
    探测到的兵力态势数据
    """
    def __init__(self) -> None:
        ...
    @property
    def alt(self) -> float:
        """
        高度
        """
    @alt.setter
    def alt(self, value: float) -> None:
        ...
    @property
    def heading(self) -> float:
        """
        航向角
        """
    @heading.setter
    def heading(self, value: float) -> None:
        ...
    @property
    def id(self) -> int:
        """
        兵力实例id
        """
    @id.setter
    def id(self, value: int) -> None:
        ...
    @property
    def knowledgeLevel(self) -> int:
        """
        识别度
        """
    @knowledgeLevel.setter
    def knowledgeLevel(self, value: int) -> None:
        ...
    @property
    def lat(self) -> float:
        """
        纬度
        """
    @lat.setter
    def lat(self, value: float) -> None:
        ...
    @property
    def lon(self) -> float:
        """
        经度
        """
    @lon.setter
    def lon(self, value: float) -> None:
        ...
    @property
    def pitch(self) -> float:
        """
        俯仰角
        """
    @pitch.setter
    def pitch(self, value: float) -> None:
        ...
    @property
    def speed(self) -> float:
        """
        速度
        """
    @speed.setter
    def speed(self, value: float) -> None:
        ...
class EquipmentAmmo:
    """
    弹药装备
    """
    def __init__(self) -> None:
        ...
    @property
    def equipmentId(self) -> str:
        """
        装备id
        """
    @equipmentId.setter
    def equipmentId(self, value: str) -> None:
        ...
    @property
    def equipmentType(self) -> str:
        """
        装备分类
        """
    @equipmentType.setter
    def equipmentType(self, value: str) -> None:
        ...
    @property
    def launchSystemId(self) -> str:
        """
        武器系统装备id
        """
    @launchSystemId.setter
    def launchSystemId(self, value: str) -> None:
        ...
    @property
    def name(self) -> str:
        """
        名称
        """
    @name.setter
    def name(self, value: str) -> None:
        ...
    @property
    def num(self) -> int:
        """
        数量
        """
    @num.setter
    def num(self, value: int) -> None:
        ...
    @property
    def properties(self) -> list[Attribute]:
        """
        属性列表
        """
    @properties.setter
    def properties(self, value: list[Attribute]) -> None:
        ...
class EquipmentPlatform:
    """
    平台装备
    """
    def __init__(self) -> None:
        ...
    @property
    def ammo(self) -> list[EquipmentAmmo]:
        """
        搭载的弹药列表
        """
    @ammo.setter
    def ammo(self, value: list[EquipmentAmmo]) -> None:
        ...
    @property
    def equipmentId(self) -> str:
        """
        装备id
        """
    @equipmentId.setter
    def equipmentId(self, value: str) -> None:
        ...
    @property
    def equipmentType(self) -> str:
        """
        装备分类
        """
    @equipmentType.setter
    def equipmentType(self, value: str) -> None:
        ...
    @property
    def id(self) -> int:
        """
        指定的实例id，实例化时直接使用此id
        """
    @id.setter
    def id(self, value: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        名称
        """
    @name.setter
    def name(self, value: str) -> None:
        ...
    @property
    def parentId(self) -> int:
        """
        所属父节点兵力实例id
        """
    @parentId.setter
    def parentId(self, value: int) -> None:
        ...
    @property
    def properties(self) -> list[Attribute]:
        """
        属性列表
        """
    @properties.setter
    def properties(self, value: list[Attribute]) -> None:
        ...
class Geometry:
    """
    图形资源
    """
    def __init__(self) -> None:
        ...
    @property
    def additional(self) -> float:
        """
        附加字段，如果是Circle和sphere，这里是半径
        """
    @additional.setter
    def additional(self, value: float) -> None:
        ...
    @property
    def attributes(self) -> list[Attribute]:
        """
        环境属性列表
        """
    @attributes.setter
    def attributes(self, value: list[Attribute]) -> None:
        ...
    @property
    def geometryType(self) -> str:
        """
        点线面类型：point,lineString,circle,polygon,sphere,cylinder,box
        """
    @geometryType.setter
    def geometryType(self, value: str) -> None:
        ...
    @property
    def id(self) -> int:
        """
        图形id
        """
    @id.setter
    def id(self, value: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        名称
        """
    @name.setter
    def name(self, value: str) -> None:
        ...
    @property
    def points(self) -> list[LLA]:
        """
        图形顶点列表
        """
    @points.setter
    def points(self, value: list[LLA]) -> None:
        ...
    @property
    def type(self) -> str:
        """
        空间资源类型：0其他 1航线 2任务区 3禁区 4出发点 5到达点
        """
    @type.setter
    def type(self, value: str) -> None:
        ...
class LLA:
    """
    经纬点
    """
    def __init__(self) -> None:
        ...
    @property
    def alt(self) -> float:
        """
        高度
        """
    @alt.setter
    def alt(self, value: float) -> None:
        ...
    @property
    def lat(self) -> float:
        """
        纬度
        """
    @lat.setter
    def lat(self, value: float) -> None:
        ...
    @property
    def lon(self) -> float:
        """
        经度
        """
    @lon.setter
    def lon(self, value: float) -> None:
        ...
class PlanInfo:
    """
    导调任务信息
    """
    def __init__(self) -> None:
        ...
    @property
    def additional(self) -> float:
        """
        附加字段，如果是Circle和sphere，这里是半径
        """
    @additional.setter
    def additional(self, value: float) -> None:
        ...
    @property
    def area(self) -> list[LLA]:
        """
        区域点列表
        """
    @area.setter
    def area(self, value: list[LLA]) -> None:
        ...
    @property
    def area_id(self) -> int:
        """
        区域资源id
        """
    @area_id.setter
    def area_id(self, value: int) -> None:
        ...
    @property
    def attributes(self) -> list[Attribute]:
        """
        输入扩展属性列表
        """
    @attributes.setter
    def attributes(self, value: list[Attribute]) -> None:
        ...
    @property
    def coverOtherPlan(self) -> bool:
        """
        是否覆盖其他任务
        """
    @coverOtherPlan.setter
    def coverOtherPlan(self, value: bool) -> None:
        ...
    @property
    def duration(self) -> int:
        """
        持续时长
        """
    @duration.setter
    def duration(self, value: int) -> None:
        ...
    @property
    def executors(self) -> list[int]:
        """
        协同兵力id列表
        """
    @executors.setter
    def executors(self, value: list[int]) -> None:
        ...
    @property
    def force_id(self) -> int:
        """
        兵力实例id
        """
    @force_id.setter
    def force_id(self, value: int) -> None:
        ...
    @property
    def id(self) -> int:
        """
        导调任务id
        """
    @id.setter
    def id(self, value: int) -> None:
        ...
    @property
    def name(self) -> str:
        """
        任务名称
        """
    @name.setter
    def name(self, value: str) -> None:
        ...
    @property
    def point_id(self) -> int:
        """
        点资源id
        """
    @point_id.setter
    def point_id(self, value: int) -> None:
        ...
    @property
    def points(self) -> list[LLA]:
        """
        点资源坐标点列表
        """
    @points.setter
    def points(self, value: list[LLA]) -> None:
        ...
    @property
    def realEndTime(self) -> int:
        """
        任务实际结束时间
        """
    @realEndTime.setter
    def realEndTime(self, value: int) -> None:
        ...
    @property
    def realStartTime(self) -> int:
        """
        任务实际起始时间
        """
    @realStartTime.setter
    def realStartTime(self, value: int) -> None:
        ...
    @property
    def status(self) -> int:
        """
        任务执行状态, 0:未开始, 1:正在执行, 2:已完成
        """
    @status.setter
    def status(self, value: int) -> None:
        ...
    @property
    def targetType(self) -> str:
        """
        目标类型
        """
    @targetType.setter
    def targetType(self, value: str) -> None:
        ...
    @property
    def targets(self) -> list[int]:
        """
        目标id列表
        """
    @targets.setter
    def targets(self, value: list[int]) -> None:
        ...
    @property
    def task_type(self) -> str:
        """
        任务类型
        """
    @task_type.setter
    def task_type(self, value: str) -> None:
        ...
class SimDevice:
    """
    设备对象
    """
    def __init__(self) -> None:
        ...
    def get_attributes(self) -> dict[str, Variant]:
        """
        获取属性列表
        """
    def get_id(self) -> int:
        """
        获取设备id
        """
    def get_name(self) -> str:
        """
        获取设备名称
        """
    def get_position(self) -> str:
        """
        获取位置、偏转、俯仰信息
        """
    def get_type(self) -> str:
        """
        获取设备类型
        """
class SimEvent:
    """
    仿真事件
    """
    def __init__(self) -> None:
        ...
    @property
    def content(self) -> str:
        """
        仿真事件内容
        """
    @content.setter
    def content(self, value: str) -> None:
        ...
    @property
    def type(self) -> int:
        """
        仿真事件类型
        """
    @type.setter
    def type(self, value: int) -> None:
        ...
class SimForce:
    """
    兵力对象
    """
    def __init__(self) -> None:
        ...
    def add_equipment_ammo(self, ammo: EquipmentAmmo) -> None:
        """
        新增一个弹药装备
        
        参数列表
        --------
        ammo: EquipmentAmmo
        	弹药信息
        """
    def add_equipment_platform(self, platform: EquipmentPlatform) -> None:
        """
        新增一个平台装备
        
        参数列表
        --------
        platform: EquipmentPlatform
        	平台信息
        """
    def get_alt(self) -> float:
        """
        获取高度
        """
    def get_attributes(self) -> dict[str, Variant]:
        """
        获取属性列表
        """
    def get_device_by_id(self, device_id: int) -> SimDevice:
        """
        根据设备id获取设备对象，当设备不存在时返回 None
        
        参数列表
        --------
        device_id: int
        	设备id
        """
    def get_device_by_name(self, device_name: str) -> SimDevice:
        """
        根据设备名称获取设备对象，当设备不存在时返回 None
        
        参数列表
        --------
        device_name: str
        	设备名称
        """
    def get_devices(self) -> list[SimDevice]:
        """
        获取所有设备对象
        """
    def get_equipment_ammo_by_id(self, ammo_equipment_id: str) -> EquipmentAmmo:
        """
        根据弹药的装备id获取弹药信息，当弹药不存在时返回 None
        
        参数列表
        --------
        ammo_equipment_id: str
        	弹药装备id
        """
    def get_equipment_ammo_by_name(self, ammo_name: str) -> EquipmentAmmo:
        """
        根据弹药名称获取弹药信息，当弹药不存在时返回 None
        
        参数列表
        --------
        ammo_name: str
        	弹药名称
        """
    def get_equipment_ammo_by_type(self, ammo_equipment_type: str) -> list[EquipmentAmmo]:
        """
        根据弹药的装备类型获取弹药列表
        
        参数列表
        --------
        ammo_equipment_type: str
        	弹药装备类型
        """
    def get_equipment_ammos(self) -> list[EquipmentAmmo]:
        """
        获取搭载的所有弹药列表
        """
    def get_equipment_id(self) -> str:
        """
        获取装备id
        """
    def get_equipment_platform_by_id(self, platform_equipment_id: str) -> list[EquipmentPlatform]:
        """
        根据平台的装备id获取平台列表
        
        参数列表
        --------
        platform_equipment_id: str
        	平台装备id
        """
    def get_equipment_platform_by_name(self, platform_name: str) -> EquipmentPlatform:
        """
        根据平台名称获取平台信息，当平台不存在时返回 None
        
        参数列表
        --------
        platform_name: str
        	平台名称
        """
    def get_equipment_platform_by_type(self, platform_equipment_type: str) -> list[EquipmentPlatform]:
        """
        根据平台的装备类型获取平台列表
        
        参数列表
        --------
        platform_equipment_type: str
        	平台装备分类
        """
    def get_equipment_platforms(self) -> list[EquipmentPlatform]:
        """
        获取搭载的所有平台列表
        """
    def get_heading(self) -> float:
        """
        获取航向角
        """
    def get_id(self) -> int:
        """
        获取实例id
        """
    def get_lat(self) -> float:
        """
        获取纬度
        """
    def get_life(self) -> float:
        """
        获取生命值，当生命值为0时自动被销毁
        """
    def get_lon(self) -> float:
        """
        获取经度
        """
    def get_name(self) -> str:
        """
        获取名称
        """
    def get_pitch(self) -> float:
        """
        获取俯仰角
        """
    def get_roll(self) -> float:
        """
        获取滚转角
        """
    def get_speed(self) -> float:
        """
        获取速度，单位：m/s
        """
    def get_team(self) -> str:
        """
        获取阵营，红方返回 TinderPy.TEAM_RED，蓝方返回 TinderPy.TEAM_BLUE
        """
    def get_type(self) -> str:
        """
        获取装备分类
        """
    def initialize_equipment_ammo(self, equipment_id: str, lon: float, lat: float, alt: float, heading: float, pitch: float, roll: float, name: str) -> SimForce:
        """
        实例化弹药，生成一个新的弹药实例对象，生成失败时返回 None
        
        参数列表
        --------
        equipment_id: str
        	需要生成的弹药实例的装备id，即EquipmentAmmo.equipmentId
        lon: float
        	初始经度，一般为平台自身所在经度
        lat: float
        	初始纬度，一般为平台自身所在纬度
        alt: float
        	初始高度，一般为平台自身所在高度
        heading: float
        	初始朝向角
        pitch: float
        	初始俯仰角
        roll: float
        	初始滚转角
        name: str
        	新的弹药实例名称
        """
    def initialize_equipment_platform_by_id(self, platform_id: int, lon: float, lat: float, alt: float, heading: float, pitch: float, roll: float) -> SimForce:
        """
        实例化平台，根据提供的平台id生成一个新的平台实例对象，生成失败时返回 None
        
        参数列表
        --------
        platform_id: int
        	需要生成的平台的实例id
        lon: float
        	初始经度，一般为平台自身所在经度
        lat: float
        	初始纬度，一般为平台自身所在纬度
        alt: float
        	初始高度，一般为平台自身所在高度
        heading: float
        	初始朝向角
        pitch: float
        	初始偏转角
        roll: float
        	初始滚转角
        """
    def initialize_equipment_platform_by_name(self, platform_name: str, lon: float, lat: float, alt: float, heading: float, pitch: float, roll: float) -> SimForce:
        """
        实例化平台，根据提供的平台名称生成一个新的平台实例对象，生成失败时返回 None
        
        参数列表
        --------
        platform_name: str
        	需要生成的平台的实例名称
        lon: float
        	初始经度，一般为平台自身所在经度
        lat: float
        	初始纬度，一般为平台自身所在纬度
        alt: float
        	初始高度，一般为平台自身所在高度
        heading: float
        	初始朝向角
        pitch: float
        	初始偏转角
        roll: float
        	初始滚转角
        """
class Variant:
    """
    设备对象
    """
    def __init__(self) -> None:
        ...
    def to_bool(self) -> bool:
        """
        转换为bool
        """
    def to_float(self) -> float:
        """
        转换为float
        """
    def to_int(self) -> int:
        """
        转换为int
        """
    def to_str(self) -> str:
        """
        转换为str
        """
def accelerate() -> None:
    """
    仿真加速，调用一次仿真速度*2
    """
def check_connection(src_force_id: int, tar_force_id: int) -> bool:
    """
    查询源兵力到目标兵力之间是否网络连通，单向查询。
    
    参数列表
    --------
    src_force_id: int
    	源兵力id
    tar_force_id: int
    	目标兵力id
    """
def conduct(plan: PlanInfo) -> bool:
    """
    任务导调，当指定兵力id对应的兵力不存在时返回 False，否则返回 True
    
    参数列表
    --------
    plan: PlanInfo
    	任务计划信息
    """
def customize_publish(msg_id: int, msg: str) -> None:
    """
    发送自定义消息至前端，仅用于跟前端通信
    
    参数列表
    --------
    msg_id: int
    	消息类型
    msg: int
    	消息内容
    """
def decelerate() -> None:
    """
    仿真减速，调用一次仿真速度/2
    """
def device_control(target_id: int, device_type: int, cmd_msg: str) -> bool:
    """
    设备控制，当目标兵力id对应的兵力不存在时返回 False，否则返回 True
    
    参数列表
    --------
    target_id: int
    	目标兵力id
    device_type: int
    	设备类型
    cmd_msg: str
    	设备控制指令，json字符串
    """
def get_blue_detected_situation() -> list[DetectedSituation]:
    """
    获取蓝方探测到的兵力态势
    """
def get_blue_force_by_id(force_id: int) -> SimForce:
    """
    根据兵力id获取某个蓝方兵力对象，当兵力不存在时返回 None
    
    参数列表
    --------
    force_id: int
    	兵力id
    """
def get_blue_forces() -> list[SimForce]:
    """
    获取蓝方所有兵力对象
    """
def get_blue_forces_by_type(force_type: str) -> list[SimForce]:
    """
    根据兵力类型获取某类型的所有蓝方兵力对象
    
    参数列表
    --------
    force_type: int
    	兵力类型
    """
def get_current_speed() -> float:
    """
    获取当前仿真倍速
    """
def get_current_step() -> int:
    """
    获取当前仿真步长，单位: ms
    """
def get_current_time() -> int:
    """
    获取当前仿真时间，单位: ms
    """
def get_force_plans(force_id: int) -> list[PlanInfo]:
    """
    获取兵力下的所有任务信息
    
    参数列表
    --------
    force_id: int中
    	兵力id
    """
def get_geometries() -> list[Geometry]:
    """
    获取场景内的所有图形资源
    """
def get_geometry(geo_id: int) -> Geometry:
    """
    根据图形id获取图形资源，当图形不存在时返回 None
    
    参数列表
    --------
    geo_id: int
    	图形id
    """
def get_plan(plan_id: int) -> PlanInfo:
    """
    获取任务信息，当任务不存在时返回 None
    
    参数列表
    --------
    plan_id: int
    	任务计划id
    """
def get_red_detected_situation() -> list[DetectedSituation]:
    """
    获取红方探测到的兵力态势
    """
def get_red_force_by_id(force_id: int) -> SimForce:
    """
    根据兵力id获取某个红方兵力对象，当兵力不存在时返回 None
    
    参数列表
    --------
    force_id: int
    	兵力id
    """
def get_red_forces() -> list[SimForce]:
    """
    获取红方所有兵力对象
    """
def get_red_forces_by_type(force_type: str) -> list[SimForce]:
    """
    根据兵力类型获取某类型的所有红方兵力对象
    
    参数列表
    --------
    force_type: int
    	兵力类型
    """
def get_sim_events() -> list[SimEvent]:
    """
    获取仿真事件列表，每步长更新
    """
def log_debug(log: str) -> None:
    """
    打印debug等级日志
    
    参数列表
    --------
    log: str
    	日志内容
    """
def log_error(log: str) -> None:
    """
    打印error等级日志
    
    参数列表
    --------
    log: str
    	日志内容
    """
def log_event(log: str) -> None:
    """
    打印event日志
    
    参数列表
    --------
    log: str
    	日志内容
    """
def log_info(log: str) -> None:
    """
    打印info等级日志
    
    参数列表
    --------
    log: str
    	日志内容
    """
def log_warning(log: str) -> None:
    """
    打印warning等级日志
    
    参数列表
    --------
    log: str
    	日志内容
    """
def post_event(e: SimEvent) -> None:
    """
    发布仿真事件
    
    参数列表
    --------
    e: SimEvent
    	仿真事件信息
    """
def terminate() -> None:
    """
    终止仿真
    """
TEAM_BLUE: str = 'BLUE'
TEAM_RED: str = 'RED'
__version__: str = '0.38.14'
