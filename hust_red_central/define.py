from enum import Enum

class RescEnum(Enum):
    nul = 0
    switch = 1
    extend = 2
    label = 3
    pathway =4
    posture =5
    track =6
    search =7
    launch = 8
    jammer = 9
    decoy = 10
    command =11
    informing = 12
    
    
class DeviceControlEnum(Enum):
	Control_Dynamics_Switch = 1	    # 动力系统开关
	Control_Dynamics_Pathway = 2	# 轨迹控制
	Control_Dynamics_Posture = 3	# 姿态控制
                                    #
	Control_Radar_Switch = 4		# 雷达开关
	Control_Radar_Extend = 5		# 雷达延展
	Control_Radar_Track = 6		    # 雷达跟踪
	Control_Radar_Search = 7		# 雷达搜索
                                    #
	Control_Sonar_Switch = 8		# 声纳开关
	Control_Sonar_Extend = 9		# 声纳延展
	Control_Sonar_Track = 10		# 声纳跟踪
	Control_Sonar_Search = 11		# 声纳搜索
                                    #
	Control_Optic_Switch = 12		# 光学开关
	Control_Optic_Extend = 13		# 光学延展
	Control_Optic_Track = 14		# 光学跟踪
	Control_Optic_Search = 15		# 光学搜索
                                    #
	Control_Elint_Switch = 16		# 电侦开关
	Control_Elint_Extend = 17		# 电侦延展
	Control_Elint_Track = 18		# 电侦跟踪
	Control_Elint_Search = 19		# 电侦搜索
                                    #
	Control_Launcher_Switch = 20	# 武器开关
	Control_Launcher_Extend = 21	# 武器延展
	Control_Launcher_Strike = 22	# 武器开火
                                    #
	Control_Jammer_Interfere = 23	# 干扰实施
	Control_Baiter_Release = 24	    # 诱饵释放
	Control_Network_Switch = 25	    # 信息开关
	Control_Network_Inform = 26	    # 信息传递
    
    
#   (兵力所属)基枚举
class EntityDomainEnum(Enum):
	EDE_NULL = 0		#	无效
	EDE_LAND = 301		#	陆基 
	EDE_NAVY = 302		#	海基
	EDE_AENO = 303		#	天基
	EDE_UNDER = 3022	#	水下
	EDE_OUTER = 304 	#	空基

#   模糊匹配枚举
class AmbiguousMatcherEnum(Enum):
	ABME_UNKNOWN = 0
	ABME_ALL = 3						# 所有实体
                                        #
	ABME_ALL_GROUND = 301				# 所有路基
	ABME_VEHICLE = 3011				    # 装甲车辆 (30101,30102,30103,30104)
	ABME_FRONT = 3012					# 固定阵地 (30105,30106,30107)
	ABME_VEHICLE_AUTO = 30108			# 无人车辆
	ABME_INFANTRY = 30109				# 步兵
                                        #
	ABME_ALL_SURFACE = 302				# 海基设备
	ABME_SHIPS = 30201  				# 水面舰船
	ABME_CARRIER = 3020101				# 航母
	ABME_DESTROYER = 3020102			# 驱逐舰
	ABME_FRIGATE = 3020103				# 护卫舰
	ABME_SHIP_SUPPLY = 3020105			# 补给舰
	ABME_MINE_DREDGER = 3020106		    # 猎扫雷舰
	ABME_CRUISER = 3020107				# 巡洋舰
	ABME_BOAT_MISSILE = 3020108		    # 导弹快艇
                                        #
	ABME_BEACHER = 30202				# 两栖登陆装备
                                        #
	ABME_UNDERSEA = 30203				# 水下装备
	ABME_SUBMARINE_GENERAL = 3020301	# 常规潜艇
	ABME_SUBMARINE_NUCLEAR = 3020302	# 核潜艇
	ABME_VEHICLE_UNDERSEA = 3020303	    # 深潜器
                                        #
	ABME_UNMANNED_SEA = 30204			# 无人舰艇
	ABME_USV = 3020402					# 水面无人艇
	ABME_UUV = 3020403					# 无人潜航器
                                        #
	ABME_SURFACE_STATION = 30205		# 水上固定设施
                                        #
	ABME_ALL_AIRFORCE = 303			    # 空基设备
                                        #
	ABME_FIXED_WING = 30301			    # 固定翼飞机
	ABME_AIRCRAFT_WARNING = 3030101	    # 预警机
	ABME_AIRCRAFT_EW = 3030102			# 电子战飞机
	ABME_AIRCRAFT_BOMBER = 3030103		# 轰炸机
	ABME_AIRCRAFT_FIGHTER = 3030104	    # 战斗机
	ABME_AIRCRAFT_ANTISUB = 3030105	    # 反潜机
                                        #
	ABME_ROTOR_WING = 30302		    	# 直升机
	ABME_ROTOR_WARNING = 3030201		# 预警直升机
	ABME_ROTOR_CRAFT = 3030202			# 武装直升机
	ABME_ROTOR_ANTISUB = 3030203		# 反潜直升机
	ABME_ROTOR_TRANSPORT = 3030204		# 运输直升机
                                        #
	ABME_UAV = 30303					# 无人机
	ABME_FLOATER = 30304				# 浮空器
                                        #
	ABME_ALL_OUTER = 304				# 空基设备
                                        #
	ABME_ALL_AMMO = 305			    	# 弹药
                                        #
	ABME_MISSILE = 30501				# 导弹
	ABME_MISSILE_F2F = 3050101  		# 面对面导弹
	ABME_MISSILE_F2A = 3050102			# 防空导弹
	ABME_MISSILE_A2A = 3050103			# 空对空导弹
	ABME_MISSILE_A2F = 3050104			# 空对面导弹
                                        #
	ABME_TORPEDO = 30502				# 鱼雷
	ABME_DEPTH_CHARGE = 30505			# 深水炸弹
	ABME_MINE = 30508					# 水雷
	ABME_BOMB = 30509					# 炸弹

#   (兵力)机动等级
class ManeuverEnum(Enum):
	MANEU_UNKNOWN = 0
	MANEU_STATIC = 1	# 静止 (spd [0,2]) eg:静止目标
	MANEU_WEAK = 2		# 机动能力弱 (spd (2,50]) eg:船
	MANEU_MEDIUM = 3	# 机动能力中 (spd (50,350]) eg:飞机
	MANEU_STRONG = 4	# 机动能力强 (spd (350, ~]) eg:战机，反舰导弹，战略导弹
	MANEU_PEDESIS = 5	# 随机运动 (高速 + 灵活) eg:空空弹
    
#   (兵力)尺寸等级
class SizeEnum(Enum):
	SIE_UNKNOWN = 0
	SIE_MINI = 1		# 三维 (0, 5]     eg: 小型导弹
	SIE_SMALL = 2		# 三维 (5, 15]    eg: 无人装备，中大型导弹
	SIE_MEDI = 3		# 三维 (15, 50]   eg: 飞机
	SIE_BIG = 4	    	# 三维 (50, 150]  eg: 驱逐舰 预警机
	SIE_HUGE = 5		# 三维 (150, ~]   eg: 航母

#   干扰弹类型枚举 
class DisruptorEnum(Enum):
	DISR_NULL = 0		
	DISR_CHAFF = 1		# 电磁干扰(箔条)
	DISR_IFRARED = 2	# 红外干扰
	DISR_PUPPET = 3 	# 假目标
	DISR_SONIC = 4		# 声干扰
    
   

