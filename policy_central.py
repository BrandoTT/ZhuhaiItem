"""红蓝方的执行策略--蓝方集中式进攻"""
import TinderPy
import random
import math
# import matplotlib.path as mpath
import traceback
import copy

# POC_LOC = [121.12371295, 38.78725701] # 港口坐标
POC_LOC = [121.11823033, 38.77894595]

class cmdlist:
    low_speed = 10 # 巡航速度
    high_blue_speed = 20 # 蓝方最大速度
    high_red_speed = 25 # 20 # 红方最大速度
    red_patrol_area = [
        77029194,   # !w-1 5号艇 #  3623181337, # 外-1 1号艇 
        3878154559, # !w-2 4号艇 #  2440587693, # 外-2 3号艇
        3623181337, # !w-3 1号艇  #  77029194, # 外-3 5号艇
        2839561766, # !w-4 2号艇 #  3878154559, # 外-4 4号艇
        2440587693, # !w-5 3号艇 #  4240880764, # 外-5 6号艇
        4240880764, # !w-6 6号艇  #  2839561766, # 外-6 2号艇
        3739178117, # 内-1 7号艇
        2655040369, # 内-2 8号艇
    ] # 共8个巡逻去区域
    
    @staticmethod
    def course_maneuver(plan_id: int, 
                        plan_name: str, 
                        task_type: str, 
                        points: list, 
                        speed: str,
                        cover_other_plan: bool = True

    ):
        """生成单个智能体或者一批智能体的航线机动指令

        Args:
            plan_id: 命令id
            plan_name: 任务名称
            task_type: 任务类型
            points: 任务目标点
            speed: 机动速度
        
        Return: 
            plan: 任务
        """
        plan = TinderPy.PlanInfo()
        plan.id = random.randint(0, 2**32 - 1)
        plan.name = plan_name
        plan.force_id = plan_id  # 执行任务的兵力id
        # plan.point_id = 1482267685  # 航线id
        plan.task_type = task_type     # 任务类型
        plan.duration = 0
        plan.cover_other_plan = cover_other_plan

        # 目标点
        points_list = []
        for point in points:
            pt = TinderPy.LLA()
            pt.lon = point[0]
            pt.lat = point[1]
            points_list.append(pt)
        plan.points = points_list

        speed_attr = TinderPy.Attribute()
        speed_attr.name = "cruise_speed"      # 航线机动速度，单位: m/s
        speed_attr.value = speed
        plan.attributes = [speed_attr]
        
        return plan
    

    @staticmethod
    def area_patrol(plan_id: int, 
                    task_type: str,
                    area_id_index: int
    ):
        """生成单个智能体区域巡逻指令
        
        Args:
            plan_id: 命令id
            task_type: 任务类型
            area_id_index: 执行巡逻区域索引: 0代表北矩形区域, 1代表南矩形区域
        
        Return: 
            plan: 任务
        
        """
        plan = TinderPy.PlanInfo()
        try:
            plan.force_id = plan_id
        except Exception as e:
            TinderPy.log_info(e)
            TinderPy.log_info(f'问题: {plan_id}')
            
        plan.id = random.randint(0, 2**32 - 1)
        plan.task_type = task_type
        # TinderPy.log_info(f"Recived index: {area_id_index}")
        plan.area_id = cmdlist.red_patrol_area[area_id_index]

        # ! 1101
        plan.cover_other_plan = True

        return plan

    @staticmethod
    def dd_attack(plan_id: int, 
                plan_name: str, 
                task_type: str, 
                targets: list
    ):
        """红方艇发射导弹攻击范围以内的敌艇"""
        plan = TinderPy.PlanInfo()
        plan.id = random.randint(0, 2**32 - 1)
        plan.name = plan_name
        plan.force_id = plan_id  # 执行任务的兵力id
        plan.task_type = task_type # 0108
        plan.targets = [tar for tar in targets]

        ammo_attr = TinderPy.Attribute()
        ammo_attr.name = "ammo"  # 
        ammo_attr.value = "302050103" # 302050202

        amount_attr = TinderPy.Attribute()
        amount_attr.name = "amount"
        amount_attr.value = "2"
        
        plan.attributes = [ammo_attr, amount_attr]

        return plan

    @staticmethod
    def gun_attack(plan_id: int, 
                plan_name: str, 
                task_type: str, 
                targets: list
    ):
        """红方艇发射导弹攻击范围以内的敌艇"""
        plan = TinderPy.PlanInfo()
        plan.id = random.randint(0, 2**32 - 1)
        plan.name = plan_name
        plan.force_id = plan_id  # 执行任务的兵力id
        plan.task_type = task_type # 0108
        plan.targets = [tar for tar in targets]

        plan.cover_other_plan = True

        ammo_attr = TinderPy.Attribute()
        ammo_attr.name = "ammo"  # 
        ammo_attr.value = "302050202" # 

        amount_attr = TinderPy.Attribute()
        amount_attr.name = "amount"
        amount_attr.value = "1000"
        
        plan.attributes = [ammo_attr, amount_attr]

        return plan


    @staticmethod
    def jp_attack(
        plan_id: int, 
        plan_name: str, 
        task_type: str, 
        targets: list

    ):
        """舰炮打击,2km打击范围,对反舰弹进行补射"""
        plan = TinderPy.PlanInfo()
        plan.id = random.randint(0, 2**32 - 1)
        plan.name = "舰炮打击"
        plan.force_id = plan_id  # 执行任务的兵力id
        plan.task_type = "0108"
        plan.targets = [tar for tar in targets]

        plan.attributes = [
            TinderPy.Attribute(
                name="ammo",
                value="302050s201"
            )
        ]

        return plan

    @staticmethod
    def microwave_attack(
        plan_id: int,
        plan_name: str,
        task_type: str = "0108",
        targets: list = []
    ):
        """微波武器，对敌使用后将敌方逼停，静止不动"""
        plan = TinderPy.PlanInfo()
        plan.id = random.randint(0, 2**32 - 1)
        plan.name = plan_name
        plan.force_id = plan_id  # 执行任务的兵力id
        plan.task_type = task_type # 0108
        plan.targets = targets
        plan.duration = 200000 # 任务持续时间

        ammo_attr = TinderPy.Attribute()
        ammo_attr.name = "weapon_highenergy" # 微波武器
        ammo_attr.value = "true" # 默认：关

        plan.attributes = [ammo_attr]
        
        return plan

    @staticmethod
    def explosive_attack(
                        plan_id: int
    ):
        pass

    @staticmethod
    def compute_distance(p1: list, p2: list):
        """接收两个点的经纬坐标,计算两点的距离(km)."""
        
        lon1, lat1 = p1[0], p1[1]
        lon2, lat2 = p2[0], p2[1]
        R = 6371.0  # 地球半径，单位为公里

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))

        distance = R * c

        return distance

    @staticmethod
    def iseast(coord1, coord2):
        """判断1号坐标点是否在2号坐标点的东侧"""
        # if coord1 == None or coord2 == None:
        #     return False
        return coord1[0] > coord2[0]

    @staticmethod
    def tracking_confirmation(plan_id: int,
                            targets_id: list,
                            trace_distance: int,
                            cover_other_plan: bool = True
        ):
        """全程跟踪目标"""
        plan = TinderPy.PlanInfo()
        plan.id = random.randint(0, 2**32 - 1)
        plan.name = "跟踪目标"
        plan.task_type = "0102"
        plan.force_id = plan_id  # 执行任务的兵力id
        plan.targets = targets_id # [xxx, xxx, xxx]
        plan.cover_other_plan = cover_other_plan
        plan.attributes = [
            TinderPy.Attribute(
                name="trace_distance", # 跟踪距离
                value=str(trace_distance) # "5" 
            )
        ]
        return plan
    
    
    @staticmethod
    def if_can_microwave(a_longitude, a_latitude, a_orientation, b_longitude, b_latitude):
        """是否能够使用微波武器攻击
        
        Args:
            a_longitude: a艇的lon坐标
            a_latitude: a艇的lat坐标
            a_orientation: a艇的朝向
            b_longitude: b艇的lon
            b_latitude: b艇的lat
        
        Return:
            relative_angle: 
        """
        # 计算A艇和B艇之间的角度
        delta_long = b_longitude - a_longitude
        delta_lat = b_latitude - a_latitude
        
        # 计算B艇相对于A艇的角度
        angle = math.degrees(math.atan2(delta_lat, delta_long))
        
        # 将角度转换到0°到360°范围
        angle = (angle + 360) % 360
        
        # 计算相对于A艇的朝向
        relative_angle = (angle - a_orientation + 360) % 360
        
        # 判断角度是否在指定范围内
        if (0 <= relative_angle <= 90) or (270 <= relative_angle <= 359):
            return relative_angle, True
        else:
            return relative_angle, False
    
    @staticmethod
    def calculate_bearing(lat_a, lon_a, lat_b, lon_b, heading_b):
        """计算A艇相对于B艇的方位角，考虑B艇当前的朝向"""
        # 将经纬度转换为弧度
        lat_a_rad = math.radians(lat_a)
        lon_a_rad = math.radians(lon_a)
        lat_b_rad = math.radians(lat_b)
        lon_b_rad = math.radians(lon_b)

        # 计算A艇相对于B艇的方位角
        delta_lon = lon_a_rad - lon_b_rad
        x = math.sin(delta_lon) * math.cos(lat_a_rad)
        y = (math.cos(lat_b_rad) * math.sin(lat_a_rad) -
            math.sin(lat_b_rad) * math.cos(lat_a_rad) * math.cos(delta_lon))
        
        angle = math.degrees(math.atan2(x, y))
        
        # 计算相对于B艇航向的方位角
        relative_angle = (angle - heading_b + 360) % 360

        return relative_angle

    @staticmethod
    def calculate_angle_difference(angle1, angle2):
        """
        计算两个朝向角之间的夹角，返回0到180度之间的最小夹角。

        参数:
            angle1, angle2: 两个朝向角（0°到360°之间）

        返回:
            两个朝向角的夹角（0°到180°之间）
        """
        # 计算角度差
        angle_diff = abs(angle1 - angle2)
        
        # 夹角最大为180度
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
        
        return angle_diff
    
    @staticmethod
    def calculate_escape_angle(bearing, cur_lat, cur_lon, escape_distance, cur_heading, enemy_lat, enemy_lon, enemy_heading, recent_enetity_heading):
        """计算蓝方探测范围内有红艇时，随机选择的逃逸角度
        
        lon, lat, escape_distance, cur_heading 用于计算基于当前朝向,使用生成的新lon, lat是否在禁航区内, 如果是的话, 则换一个角度
        # *recent_enetity_heading 是最近队友的朝向, 用来生成避让的时候，要跟这个呈不同角度
        """
        try:
            if 90 <= bearing <= 270:
                return None  # 敌方艇在后方或后侧方，不需要躲避
            
            # todo 测试 1105 通过判断红方朝向来预测红方是否冲自己来,如果不是的话,也不用躲避
            if not cmdlist.is_enemy_heading_towards_you(cur_lat, cur_lon, enemy_lat, enemy_lon, enemy_heading): # ! 在这里, cur_heading是自己艇的heading
                TinderPy.log_info(f"当前预判不是冲自己来的,因此无需逃避!")
                # 说明cur并不在敌方的角度范围内，预测不是冲自己来的
                return None
            
            # 计算四个逃逸角度
            escape_angles = [
                (bearing + 60) % 360,
                (bearing + 120) % 360,
                (bearing - 60) % 360,
                (bearing - 120) % 360
            ]
            i = 0
            # todo 测试
            while True:
                i+=1
                # 从这四个角度中随机选择一个逃逸角度
                escape_angle = random.choice(escape_angles)
                new_lon, new_lat = cmdlist.calculate_new_coordinates(cur_lat, cur_lon,escape_angle, escape_distance, cur_heading)
                # todo 跟最近队友的朝向角度

                inside_flag = cmdlist.is_point_in_square([new_lat, new_lon], 
                                            [[38.414308, 120.781102],
                                            [38.414308,120.938375],
                                            [38.272312,120.781102],
                                            [38.272312,120.938375]] # ! 西南岛屿
                                            ) or \
                                            cmdlist.is_point_in_square([new_lat, new_lon], 
                                                [ # ! 交易岛
                                                    [38.96704919, 121.27544107],
                                                    [38.95200281, 121.16755007],
                                                    [38.94653060, 121.10158410],
                                                    [38.89771809, 121.08751136],
                                                    [38.83145988, 121.11527063],
                                                    [38.78080525, 121.09502641],
                                                    [38.72926539, 121.15367071],
                                                    [38.72713760, 121.20820322],
                                                    [38.79145642, 121.29068622]
                                                ]
                                            )
                TinderPy.log_info(f"蓝方和队友的角度 {cur_heading} and {recent_enetity_heading}， 产生避让角度: {escape_angle}")
                angle_difference = cmdlist.calculate_angle_difference((cur_heading+escape_angle) % 360, recent_enetity_heading[0])
                TinderPy.log_info(f"蓝方和队友的角度 {(cur_heading+escape_angle) % 360} and {recent_enetity_heading}, angle: {angle_difference}, inside: {inside_flag}, {(inside_flag or angle_difference < 30)}")
                if (inside_flag or angle_difference < 30) and i<10: # ? 返回True则代表在里边
                    # TinderPy.log_info(f"遇到禁航区,禁止向此方向避让!")
                    # todo 蓝方避让角度的时候，要判断距离自己最近的队友的朝向，然后朝向不同的角度
                    continue
                else:
                    break

            return escape_angle

        except Exception as e:
            error_message = traceback.format_exc()  # 获取完整的错误信息和行号
            TinderPy.log_info(f"计算逃逸角度出现问题: {error_message}")


    @staticmethod
    def is_point_in_square(point, square_coords):
        """
        判断给定的坐标点是否在正方形区域内。

        参数:
        point: list[float] - 要判断的坐标点 [纬度, 经度]
        square_coords: list[list[float]] - 正方形区域的四个角点 [[lat1, lon1], [lat2, lon2], [lat3, lon3], [lat4, lon4]]

        返回:
        bool - 如果点在正方形区域内返回 True，否则返回 False
        """
        def is_point_in_polygon(point, polygon_coords):
            """
            判断给定的坐标点是否在多边形区域内。

            参数:
            point: list[float] - 要判断的坐标点 [纬度, 经度]
            polygon_coords: list[list[float]] - 多边形的所有角点 [[lat1, lon1], [lat2, lon2], ...]

            返回:
            bool - 如果点在多边形区域内返回 True，否则返回 False
            """
            lat, lon = point
            num_points = len(polygon_coords)
            inside = False

            p1_lat, p1_lon = polygon_coords[0]
            for i in range(num_points + 1):
                p2_lat, p2_lon = polygon_coords[i % num_points]
                if lat > min(p1_lat, p2_lat):
                    if lat <= max(p1_lat, p2_lat):
                        if lon <= max(p1_lon, p2_lon):
                            if p1_lat != p2_lat:
                                xinters = (lat - p1_lat) * (p2_lon - p1_lon) / (p2_lat - p1_lat) + p1_lon
                            if p1_lon == p2_lon or lon <= xinters:
                                inside = not inside
                p1_lat, p1_lon = p2_lat, p2_lon

            return inside

        if len(square_coords) > 4:
            # 多边形额外处理
            return is_point_in_polygon(point, square_coords)
        
        # 提取正方形区域的纬度和经度
        latitudes = [coord[0] for coord in square_coords]
        longitudes = [coord[1] for coord in square_coords]

        # 计算正方形的边界
        min_lat = min(latitudes)
        max_lat = max(latitudes)
        min_lon = min(longitudes)
        max_lon = max(longitudes)

        # 判断点是否在边界内
        return min_lat <= point[0] <= max_lat and min_lon <= point[1] <= max_lon

    @staticmethod
    def calculate_new_coordinates(lat, lon, bearing, distance_km, heading):
        """蓝方艇沿某个角度行驶distance_km后的新坐标"""
        # # 地球的平均半径
        # R = 6371.0  # 单位：公里
        
        # # 将距离转换为弧度
        # distance_rad = distance_km / R
        
        # # 将角度转换为弧度
        # bearing_rad = math.radians(bearing)
        
        # # 计算新的纬度和经度
        # new_lat = math.asin(math.sin(math.radians(lat)) * math.cos(distance_rad) +
        #                     math.cos(math.radians(lat)) * math.sin(distance_rad) * math.cos(bearing_rad))
        
        # new_lon = math.radians(lon) + math.atan2(math.sin(bearing_rad) * math.sin(distance_rad) * math.cos(math.radians(lat)),
        #                                         math.cos(distance_rad) - math.sin(math.radians(lat)) * math.sin(new_lat))
        
        # return math.degrees(new_lon), math.degrees(new_lat)
        """蓝方艇沿某个角度（bearing）行驶distance_km后的新坐标，
        其中heading为艇的当前航向（以艇的正前方为0°）
        """
        # 地球的平均半径
        R = 6371.0  # 单位：公里

        # 将距离转换为弧度
        distance_rad = distance_km / R

        # 将角度转换为弧度
        heading_rad = math.radians(heading)
        bearing_rad = math.radians(bearing)

        # 计算实际航向
        actual_bearing_rad = heading_rad + bearing_rad

        # 计算新的纬度和经度
        new_lat = math.asin(math.sin(math.radians(lat)) * math.cos(distance_rad) +
                            math.cos(math.radians(lat)) * math.sin(distance_rad) * math.cos(actual_bearing_rad))

        new_lon = math.radians(lon) + math.atan2(math.sin(actual_bearing_rad) * math.sin(distance_rad) * math.cos(math.radians(lat)),
                                                math.cos(distance_rad) - math.sin(math.radians(lat)) * math.sin(new_lat))

        return math.degrees(new_lon), math.degrees(new_lat)

    
    @staticmethod
    def interpolate_bearing(lat_b, lon_b, heading_b, target_lat, target_lon, num_points=10):
        """生成从B艇到目标点的弯曲路径点
        """
        # 计算目标点与B艇之间的距离和方位角
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371.0  # 地球平均半径（公里）
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)

            dlat = lat2_rad - lat1_rad
            dlon = lon2_rad - lon1_rad

            a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            return R * c  # 返回距离（公里）

        # 生成弯曲路径点
        path_points = []
        for i in range(num_points):
            # 计算插值因子
            t = i / (num_points - 1)  # 从0到1的插值因子
            
            # 计算插值经纬度
            new_lat = lat_b + (target_lat - lat_b) * t
            new_lon = lon_b + (target_lon - lon_b) * t
            
            # 在路径上添加一定的弯曲效果
            curve_offset = 0.01 * math.sin(t * math.pi)  # 产生弯曲效果
            new_lat += curve_offset * math.cos(math.radians(heading_b + 90))  # 朝向的垂直偏移
            new_lon += curve_offset * math.sin(math.radians(heading_b + 90))

            path_points.append((new_lat, new_lon))

        return path_points
    

    @staticmethod
    def predict_position(position, speed, heading, n_frames: int = 40): #  500):
        """根据艇的经纬，速度，朝向求n_frames后的新位置"""
        
        lon = position[0]
        lat = position[1]

        #  每帧的时间间隔（秒）
        time_per_frame = 0.2  # 200 ms
        # 总时间
        total_time = n_frames * time_per_frame

        # 计算行驶的距离
        distance_m = speed * total_time  # 以米为单位

        # 将航向角转换为弧度，并调整角度使其符合数学坐标系
        heading_rad = math.radians(heading)

        # 计算新的经纬度增量
        delta_lat = (distance_m * math.cos(heading_rad)) / 6371000.0 * (180 / math.pi)
        delta_lon = (distance_m * math.sin(heading_rad)) / (6371000.0 * math.cos(math.radians(lat))) * (180 / math.pi)

        new_lat = lat + delta_lat
        new_lon = lon + delta_lon

        return [new_lon, new_lat]


    @staticmethod
    def get_partol_points(goal_points: list, radius_km=5) -> list:
        """给一个坐标点，得到以他为中心的，半径为1km的正方形边角坐标"""
        import math
        lon, lat = goal_points[0], goal_points[1]
        
        R = 6371.0

        # 计算边长的一半
        half_distance = radius_km / 2

        # 将距离转换为经纬度差
        lat_delta = half_distance / R * (180 / math.pi)
        lon_delta = half_distance / (R * math.cos(math.pi * lat / 180)) * (180 / math.pi)

        # 计算四个角点
        corners = [
            [lon - lon_delta, lat + lat_delta],  # 左上角
            [lon + lon_delta, lat + lat_delta],  # 右上角
            [lon + lon_delta, lat - lat_delta],  # 右下角
            [lon - lon_delta, lat - lat_delta]  # 左下角
        ]

        return corners


    @staticmethod
    def is_enemy_heading_towards_you(B_lat, B_lon, E_lat, E_lon, E_heading, tolerance=30):
        """
        判断敌方艇是否冲向B艇
        
        参数:
            B_lat, B_lon: B艇的纬度和经度（你的位置）
            E_lat, E_lon: 敌方艇的纬度和经度
            E_heading: 敌方艇的航向角（0°为正北，顺时针增加）
            tolerance: 判断敌方艇是否朝向B艇的容差范围，默认30度（可以调整）

        返回:
            True: 敌方艇正在冲向B艇
            False: 敌方艇不冲向B艇
        """
        def calculate_bearing(lat1, lon1, lat2, lon2):
            """
            计算从点 (lat1, lon1) 到点 (lat2, lon2) 的方位角（航向角），
            返回的角度范围是 [0, 360]，以正北为0度，顺时针增加。
            """
            # 转换经纬度为弧度
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            
            # 计算方位角
            dlon = lon2 - lon1
            x = math.sin(dlon) * math.cos(lat2)
            y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
            
            initial_bearing = math.atan2(x, y)
            
            # 转换为度数，并确保角度在 [0, 360] 范围内
            initial_bearing = math.degrees(initial_bearing)
            compass_bearing = (initial_bearing + 360) % 360
            
            return compass_bearing

        # 计算从敌方艇到B艇的方位角
        bearing_to_B = calculate_bearing(E_lat, E_lon, B_lat, B_lon)
        
        # 计算敌方艇朝向与从敌方艇到B艇的方位角的夹角
        angle_diff = (bearing_to_B - E_heading + 360) % 360
        
        # 判断敌方艇的朝向是否接近B艇
        if abs(angle_diff) <= tolerance or abs(angle_diff - 360) <= tolerance:
            return True
        else:
            return False

        pass
    
    @staticmethod
    def generate_random_point_nearby(points: list, radius: int = 200):
        """
        生成一个随机点，位于给定经纬度(lat, lon)周围的指定范围内（单位：米）。

        参数:
        lat (float): 中心点的纬度
        lon (float): 中心点的经度
        radius (float): 随机点生成的半径，单位：米，默认为100米

        返回:
        tuple: 返回生成的随机点 (lat, lon)
        """
        lat = points[1]
        lon = points[0]

        # 地球半径，单位：米
        EARTH_RADIUS = 6371000

        # 将米转换为度
        def distance_to_deg(distance):
            return distance / (EARTH_RADIUS * math.pi / 180)

        # 随机生成角度
        angle = random.uniform(0, 2 * math.pi)

        # 计算偏移量
        delta_lat = distance_to_deg(radius) * math.cos(angle)
        delta_lon = distance_to_deg(radius) * math.sin(angle) / math.cos(math.radians(lat))

        # 计算新的经纬度
        lat_new = lat + delta_lat
        lon_new = lon + delta_lon

        return [lon_new, lat_new]

    # @staticmethod
    # def if_red_avoid(points_1: list = None, points_2: list = None):
    #     """红方避让效果判断两个点的连线是否经过岛屿, 模拟避让效果(即需要更换理想目标).

    #     # todo 如果与理想目标之间的连线穿过岛屿, 则重新规划一个路径.

    #     "trade1": [121.27380169, 38.96845602],
    #     "trade2": [121.16724190, 38.95374014],
    #     "trade3": [121.08751414, 38.89781016],
    #     "trade4": [121.11248287, 38.83181382],
    #     "trade5": [121.15265619, 38.72466319],
    #     "trade6": [121.29071637, 38.78868264],

    #     """
    #     import shapely.geometry as geom
    #     polygon_points = [(38.96845602, 121.27380169), (38.95374014, 121.16724190), (38.89781016, 121.08751414), \
    #                       (38.83181382, 121.11248287), (38.72466319, 121.15265619), (38.78868264, 121.29071637)]
    #     polygon = geom.Polygon(polygon_points)
    #     pass
    #     pass


    # @staticmethod
    # # 判断A艇是否在追B艇
    # def is_pursuing(latA, lonA, headingA, latB, lonB, headingB):
        
    #     # 计算A艇相对于B艇的方位角
    #     bearing_AB = calculate_bearing(latB, lonB, latA, lonA)

    #     # 计算B艇的航向角
    #     headingB = headingB % 360
        
    #     # 计算A艇相对于B艇的方位角与B艇航向的偏差
    #     relative_bearing = (bearing_AB - headingB + 360) % 360
        
    #     # 如果相对方位角在0到45度之间，或者在315到360度之间，表示A艇在追B艇
    #     if 0 <= relative_bearing <= 45 or 315 <= relative_bearing <= 360:
    #         return True  # A艇在追B艇
    #     return False  # A艇不在追B艇

class RedPolicy:
    def __init__(self):
        # 记录所有我方实体id
        self.entities = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
        }
        self.entities_class = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
        }
        # 记录所有我方实体位置
        self.loc = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
            # "系留探测飞艇-1": POC_LOC
        }
        # 记录所有我方实体上上帧，上帧的位置
        self.loc_last = {
            "1号艇": [None, None], # 上上帧，上帧
            "2号艇": [None, None],
            "3号艇": [None, None],
            "4号艇": [None, None],
            "5号艇": [None, None],
            "6号艇": [None, None],
            "7号艇": [None, None],
            "8号艇": [None, None],
            "9号艇":  [None, None],
            "10号艇": [None, None],
            "11号艇": [None, None],
            "12号艇": [None, None],
            # "系留探测飞艇-1": [POC_LOC, POC_LOC]
        }
        # 记录我方所有实体的当前朝向
        self.heading = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
        }
        self.enemies_heading = {
            "1号走私艇": None,
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }
        # 记录所有敌方实体当前帧位置
        self.enemies = {
            "1号走私艇": None,
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }
        # 记录所有敌方实体上上帧，上帧的位置
        self.enemies_last = {
            "1号走私艇": [None, None],
            "2号走私艇": [None, None],
            "3号走私艇": [None, None],
            "4号走私艇": [None, None],
            "5号走私艇": [None, None],
            "6号走私艇": [None, None],
            "7号走私艇": [None, None],
            "8号走私艇": [None, None],
            "9号走私艇":  [None, None],
            "10号走私艇": [None, None],

        }
        # 记录所有敌方实体id
        self.enemies_id = {
            "1号走私艇": None,
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }
        # ! 增加红方艇状态记录, 记载红方正在追踪或者正在巡逻(无目标跟踪)
        # ! [0, "n号艇正在巡逻中或正在前往巡逻途中"] 代表正在巡逻(预定区域), 无目标跟踪;
        # ! [1, "n号艇正在跟踪n号走私艇"] 代表正在跟踪"n号走私艇"
        # ! [2, "n号艇正前往目标点"] 代表正在执行前往某点（巡逻中）,到达目标点后,开始执行巡逻任务,即转为0
        # // [3, "n号艇正在巡逻中或正在前往巡逻途中"] 代表正在执行区域的巡逻任务
        self.red_records = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
        }
        # ! 记录状态 上帧的记录,如果状态一样的话,就无需发送
        self.last_red_records = copy.deepcopy(self.red_records) 
        # ! 记录蓝方的状态
        self.blue_records = {
            "1号走私艇": [], # 记载被哪些艇跟踪 ["2号艇", "3号艇"]
            "2号走私艇": [],
            "3号走私艇": [],
            "4号走私艇": [],
            "5号走私艇": [],
            "6号走私艇": [],
            "7号走私艇": [],
            "8号走私艇": [],
            "9号走私艇":  [],
            "10号走私艇": [],
        }
        self.last_blue_records = copy.deepcopy(self.blue_records) 

        # ? 设置一个ID: Name的字典
        self.ID_NAME = {}
        
        self.swb_interval = 500 # 500 # 震撼弹间隔
        self.wave_interval = 100 # 持续照射
        
        self.shoot_interval = { # 射击一次，20帧以内不能再重复性射击
            "1号艇": [0, 0, 16], # 模拟震撼弹的数量
            "2号艇": [0, 0, 16],
            "3号艇": [0, 0, 16],
            "4号艇": [0, 0, 16],
            "5号艇": [0, 0, 16],
            "6号艇": [0, 0, 16],
            "7号艇": [0, 0, 16],
            "8号艇": [0, 0, 16],
            "9号艇":  [0, 0, 16],
            "10号艇": [0, 0, 16],
            "11号艇": [0, 0, 16],
            "12号艇": [0, 0, 16],
        }
        self.shoot_interval_gun = {
            "1号艇": True,
            "2号艇": True,
            "3号艇": True,
            "4号艇": True,
            "5号艇": True,
            "6号艇": True,
            "7号艇": True,
            "8号艇": True,
            "9号艇":  True,
            "10号艇": True,
            "11号艇": True,
            "12号艇": True,
        }
        # 存储红方实体有哪些时间段之后是处于空闲的位置，临时指令只有当frame > free_time的时候才会奏效
        self.red_enetity_free_time = {
            "1号艇": 0, # frame
            "2号艇": 0,
            "3号艇": 0,
            "4号艇": 0, #  4868,
            "5号艇": 0,# 4868,
            "6号艇": 0,
            "7号艇": 0,
            "8号艇": 0,
            "9号艇": 0,
            "10号艇": 0,
            "11号艇": 0,
            "12号艇": 0,
        }
        # * 记录红方各个艇是否开始了第一波侦察任务,这个dict是一次性的，用完就不用了
        self.start_check = {
            "1号艇": False,
            "2号艇": False,
            "3号艇": False,
            "4号艇": False, #  4868,
            "5号艇": False,# 4868,
            "6号艇": False,
            "7号艇": False,
            "8号艇": False,
            "9号艇": False,
            "10号艇": False,
            "11号艇": False,
            "12号艇": False,
        }
 
        # 每个艇会有自己的初始默认目标，在推演过程中，这个目标会随意变化
        self.follow_enemy = {
            "1号艇": "10号走私艇", # "Die"
            "2号艇": "1号走私艇",
            "3号艇": "4号走私艇",
            "4号艇": "10号走私艇",
            "5号艇": "9号走私艇",
            "6号艇": "2号走私艇",
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": "6号走私艇",
            "11号艇": "5号走私艇",
            "12号艇": "6号走私艇",
        }
        self.follow_count = {
            "1号走私艇": 0,
            "2号走私艇": 0,
            "3号走私艇": 0,
            "4号走私艇": 0,
            "5号走私艇": 0,
            "6号走私艇": 0,
            "7号走私艇": 0,
            "8号走私艇": 0,
            "9号走私艇":  0,
            "10号走私艇": 0,
        }
        # * 固定任务的标志，跟随多少帧
        self.counter = {
                "1": 0,
                "2": 0,
                "4": 0,
                "5": 0,
                "7": 0, # 7,8号艇沿某个航线巡逻 
                "8": 0,
                "3": 0,
                "6": 0,
                "9": 0,
                "10": 0,
                "11": 0,
                "12": 0
        }
        # ? ---------------------------------------- 临时指令是否开始的标志 ---------------------------------------------------------
        # ! 临时指令拥有最高优先级, 所有的函数运行前都要判断当前艇是否正在执行临时指令机动任务 
        # 临时指令 # todo查证目标 每个艇设置一个查证的目标, 然后在循环过程中,判断是否为空,当不为空时,则将目标设置为敌方, 
        # 每次执行for循环,执行两个判断:1) 执行艇是否空闲(执行艇是否空闲改到make_cmd中去判断); 2)被侦察艇是否存活
        self.check_task = {
            "1号艇": None, # * 现在存储的是敌方ID
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None
        }
        # 临时指令 # todo 航行到某个目标点,开始巡逻
        self.forward_points = {
            "1号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0}, # goal  # ! partol_index 代表的是，巡逻的索引
            "2号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "3号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "4号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "5号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "6号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "7号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "8号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "9号艇":  {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "10号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "11号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0},
            "12号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0}
        }

        # ? ---------------------------------------------------------------------------------------------------------------------------
        # 巡逻区中心点
        self.partol_center = {
            "0": [121.18131194, 39.15385110], # [120.76969571, 38.83097758], # 区域-1
            "1": [120.87651386, 39.08262726], # [121.14575319, 38.54386562], # 区域-2
            "2": [120.77001763, 38.83510117], # [121.17442289, 39.15322178], # 区域-3
            "3": [120.90501538, 38.60919472], # [120.87339587, 39.07907658], # 区域-4
            "4": [121.15515944, 38.54407683], # [121.43682276, 38.62192287], # 区域-5
            "5": [121.43891145, 38.62678623], # [120.90209349, 38.60757628], # 区域-6
        }
        # ! 记录每个巡逻区的巡逻艇的数量, 用来约束每个巡逻区的数量不能超过2
        # self.partol_num = {
        #     "0": 0, # 区域-1
        #     "1": 0, # 区域-2 
        #     "2": 0,
        #     "3": 0,
        #     "4": 0,
        #     "5": 0, 
        # }
        # # 记录交易点
        # self.trading = {
        #     "trade1": [121.27481187, 38.96847375],
        #     "trade2": [121.16631357, 38.95360358],
        #     "trade3": [121.08748786, 38.89710186],
        #     "trade4": [121.11388433, 38.83247226],
        #     "trade5": [121.15210794,38.72702225],
        #     "trade6": [121.28995098,38.78820377],

        # }
        # self.trading = {
        #     "trade1": [121.27518169, 38.96845602],
        #     "trade2": [121.16724190, 38.95374014],
        #     "trade3": [121.08771414, 38.89781016],
        #     "trade4": [121.11448287, 38.83181382],
        #     "trade5": [121.15265619, 38.72716319],
        #     "trade6": [121.29071637, 38.78868264],
        # }
        self.trading = {
            "trade1": [121.27380169, 38.96845602],
            "trade2": [121.16724190, 38.95374014],
            "trade3": [121.08751414, 38.89781016],
            "trade4": [121.11248287, 38.83181382],
            "trade5": [121.15265619, 38.72466319],
            "trade6": [121.29071637, 38.78868264],

        }

        self.patrol_lines_s2n_7 = [
            [121.01429836, 38.94354100],
            [121.10983832, 39.00455319],
            [121.20751086, 39.00090720],
            [121.29110832, 39.03636477],

        ] # 7号艇模型从北往南
        self.patrol_lines_n2s_7 = self.patrol_lines_s2n_7[::-1] # 8号艇默认从南往北
        
        self.partol_7_curr_index = True # 代表到达了最终点
        self.partol_7_direction = 1 # 1代表从南往北 0代表从北往南

        
        self.patrol_lines_n2s_8 = [
            [120.99630143, 38.92666178],
            [120.99203626, 38.86026879],
            [121.04407141,38.80212402],
            [121.06795640,38.72297094],
        ]
        self.patrol_lines_s2n_8 = self.patrol_lines_n2s_8[::-1] # 8号艇默认从北往南
        
        self.partol_8_curr_index = True # 代表到达了最终点
        self.partol_8_direction = 1 # 1代表从北往南 0代表从南往北


        self.patrol_lines_n2s_9 = [
            [121.07861936, 38.70637510],
            [121.16179030, 38.66942058],
            [121.25519767,38.69405905],
            [121.34647244,38.76393283],
        ]
        self.patrol_lines_s2n_9 = self.patrol_lines_n2s_9[::-1] # 8号艇默认从北往南
        
        self.partol_9_curr_index = True 
        self.partol_9_direction = 1 #
        
        # 检查敌方是否存活
        self.enemy_alive = {
            "1号走私艇": None, # float 代表血量多少
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }

    def first_check(self, frame, red_name):
        """所有艇执行第一次侦察任务
        
        Args:
            frame: 当前帧数
            red_name: 红方的名称数字 int = 1 ~ 12

        Return:
            None
        """
        # ! 优先判断当前艇的跟踪艇是否不为None，不为None则说明当前艇还未设置跟踪目标
        if self.follow_enemy[f"{red_name}号艇"] is not None and \
                self.check_task[f"{red_name}号艇"] is None and \
                self.forward_points[f"{red_name}号艇"]["goal"] is None:  # ? 加入当前艇没有在执行临时任务 
            # todo 测试
            # 前驱侦察敌方
            if self.counter[f"{red_name}"] > 0 and frame % 150 == 0:
                self.counter[f"{red_name}"] -= 1
                # ! 先不采用junsheng接口:1)不能紧紧跟随，无法使用微波武器 2）蓝方避让后的效果有点奇怪
                # if cmdlist.compute_distance(self.loc[f"{red_name}号艇"], self.enemies[self.follow_enemy[f"{red_name}号艇"]]) < 5:
                #     # 转而使用junsheng的仿真接口
                #     self.counter[f"{red_name}"] = 0
                #     plan = cmdlist.tracking_confirmation(self.entities[f"{red_name}号艇"], [self.enemies_id[self.follow_enemy[f"{red_name}号艇"]]], 6)
                #     TinderPy.log_info(f"使用junsheng跟踪接口")
                #     TinderPy.conduct(plan)
                # else:
                if self.enemy_alive[self.follow_enemy[f"{red_name}号艇"]] <= 10: # 4号艇跟随的目标已经死掉了 # !是否考虑更换新的目标？配合换目标的模块
                    TinderPy.log_info(f'{self.follow_enemy[f"{red_name}号艇"]} 意外死掉了!')
                    # self.counter[f"{red_name}"] = 0 # 
                    # # todo 测试
                    # self.follow_enemy[f"{red_name}号艇"] = None # 当他掉跟踪的目标死了之后，跟踪目标为None
                    # # ! 这个地方应该及时更换目标, 换到下方更换目标模块
                else:
                    # todo 预判模块，新的目标点是蓝方的后5帧点
                    try:
                        plan = cmdlist.course_maneuver(self.entities[f"{red_name}号艇"], 
                                                    f"红方{red_name}号艇前驱侦察", 
                                                    "0100", 
                                                    [
                                                        # cmdlist.predict_position(self.enemies[self.follow_enemy[f"{red_name}号艇"]], cmdlist.high_blue_speed, self.enemies_heading[self.follow_enemy[f"{red_name}号艇"]])
                                                        # self.enemies[self.follow_enemy[f"{red_name}号艇"]] 
                                                        cmdlist.generate_random_point_nearby(self.enemies[self.follow_enemy[f"{red_name}号艇"]])
                                                        # cmdlist.predict_position(self.enemies[self.follow_enemy[f"{red_name}号艇"]], cmdlist.high_blue_speed, self.enemies_heading[self.follow_enemy[f"{red_name}号艇"]])
                                                    ], 
                                                    str(cmdlist.high_red_speed))
                        
                        TinderPy.log_info(f'蓝方 {self.follow_enemy[f"{red_name}号艇"]} 的实际位置: {self.enemies[self.follow_enemy[f"{red_name}号艇"]]} 红方艇 {red_name} 对其预判位置: {cmdlist.predict_position(self.enemies[self.follow_enemy[f"{red_name}号艇"]], cmdlist.high_blue_speed, self.enemies_heading[self.follow_enemy[f"{red_name}号艇"]])}')
                        # if self.enemy_alive[self.follow_enemy[f'{red_name}号艇']] < 60: # 生命值
                        #     TinderPy.log_info(f"打印血量--------蓝方 {self.follow_enemy[f'{red_name}号艇']} 的血量是: {self.enemy_alive[self.follow_enemy[f'{red_name}号艇']]}")
                        TinderPy.conduct(plan)
                        # ! 记录状态
                        self.red_records[f"{red_name}号艇"] = [1, self.entities[f"{red_name}号艇"], f"正在跟踪{self.enemies_id[self.follow_enemy[f'{red_name}号艇']]}"]
                    except Exception as e:
                        TinderPy.log_error(f"问题!不能正常跟踪: {e}!!")

    def act(self, frame=None, cmd=None) -> TinderPy.PlanInfo:
        """策略执行函数

        Args:
            frame: 当前运行帧数
            cmd: 临时指令

        Return:
            flag: success(临时指令执行成功), failed(临时指令执行失败), none(当前帧没有临时指令)

        """
        # self.last_red_records = self.red_records # ! 记录状态 ! 记录上一帧的消息
        self.follow_count = {key: int(0) for key in self.follow_count} # 初始化现在的跟踪艇数量
        # ! 清空每个巡逻区的巡逻艇数量, 不应该在这里去掉
        # self.partol_num = {key: int(0) for key in self.partol_num}
        import json
        if cmd is not None:
            # ! 解析cmd(暂时没有使用)
            # 解码为字符串
            decoded_string = cmd.decode('utf-8')
            # 转换为字典
            data_dict = json.loads(decoded_string)
            TinderPy.log_info(f"order is : {data_dict}")
            cmd = data_dict

        # 这个敌方用上帝视角代替
        detects_red = TinderPy.get_blue_forces()
        try:
            # 更新敌方位置
            for n, detect in enumerate(detects_red):
                if detect.get_name() in self.enemy_alive:
                    self.enemy_alive[detect.get_name()] = detect.get_life()
                    # 更新上上帧、上帧的位置信息
                    self.enemies_last[detect.get_name()][0] = self.enemies_last[detect.get_name()][1] 
                    self.enemies_last[detect.get_name()][1] = self.enemies[detect.get_name()]
                    self.enemies[detect.get_name()] = [detect.get_lon(), detect.get_lat()]    
                    self.enemies_heading[detect.get_name()] = detect.get_heading()   

            flag = "none"
            if cmd is None:
                # flag = "none"
                pass
            if cmd is not None:
                TinderPy.log_info(f"Receive cmd: {cmd}")
            
            # 解析当前态势
            red_all_forces = TinderPy.get_red_forces()
            for r_item in red_all_forces:
                if r_item.get_name() in self.loc:
                # if r_item.get_name() != "震撼弹-1":
                    self.loc_last[f"{r_item.get_name()}"][0] = self.loc_last[f"{r_item.get_name()}"][1]
                    self.loc_last[f"{r_item.get_name()}"][1] = self.loc[f"{r_item.get_name()}"]
                    self.loc[f"{r_item.get_name()}"] = [r_item.get_lon(), r_item.get_lat()]
                    self.heading[f"{r_item.get_name()}"]= [r_item.get_heading()]
                    # # 减小射击间隔
                    if r_item.get_name() in self.shoot_interval:
                    # if r_item.get_name() != "系留探测飞艇-1":
                        try:
                            if self.shoot_interval[f"{r_item.get_name()}"][0]  > 0:
                                self.shoot_interval[f"{r_item.get_name()}"][0] -= 1
                            if self.shoot_interval[f"{r_item.get_name()}"][1] > 0:
                                self.shoot_interval[f"{r_item.get_name()}"][1] -= 1
                        except Exception as e:
                            TinderPy.log_error('归一化射击间隔出现问题', e)

            if frame == 200: # 500:
                # TinderPy.log_info(f'开始模拟临时指令: 00, 4号艇前往 某点巡逻')
                # cmd = {
                #     "commandId": "00",
                #     "army": [
                #         "4号艇"
                #     ],
                #     "targets":[] ,  
                #     "area": [[120.77197326,38.94613115]],
                #     "timeLimit": 1,
                #     "startTime": "-1"
                # }
                # cmd = {
                #     "commandId": "01",
                #     "army": [
                #         "9号艇", "10号艇"
                #     ],
                #     "targets":[] ,  
                #     "area": ["巡逻区1"],
                #     "timeLimit": 30,
                #     "startTime": "-1"
                # }
                # cmd = {
                #     "commandId": "02",
                #     "army": [
                #         "7号艇", "8号艇"
                #     ],
                #     "targets":[] ,  
                #     "area": ["港口"],
                #     "timeLimit": 30,
                #     "startTime": "-1"
                # }
                # cmd = {
                #     "commandId": "03",
                #     "army": [
                #         "9号艇", "10号艇", "7号艇", "8号艇"
                #     ],
                #     "timeLimit": 0,
                #     "startTime": "-1",
                #     "equip": [
                #         {
                #             "name": "雷达",
                #             "status": 1
                            
                #         },
                #         {
                #             "name": "光电",
                #             "status": 1
                #         },
                #         {
                #             "name": "红外",
                #             "status": 0
                #         }
                #     ]
                # }
                # cmd = {
                #     "commandId": "22",
                #     "army": [
                #         "4号艇"
                #     ],
                #     "targets": ["9号走私艇"],
                #     "startTime": "-1",
                #     "equip": [
                #         {
                #             "name": "雷达",
                #             "status": 0
                            
                #         },
                #         {
                #             "name": "光电",
                #             "status": 0
                #         },
                #         {
                #             "name": "红外",
                #             "status": 0
                #         }
                #     ]
                # }
                # cmd = {
                #     "commandId": "30",
                #     "army":["2号艇", "3号艇", "1号艇", "4号艇"], #
                #     "armyNum":4,  
                #     "timeLimit": 0, 
                #     "startTime": "-1",
                #     "cordon":[5000,50000]
                # }
                # cmd = {
                #     "commandId": "31",
                #     "army":["1号艇","2号艇", "3号艇","4号艇", "5号艇","6号艇",],
                #     "armyNum":2,
                #     "timeLimit": 0,
                #     "startTime": "-1",
                #     "area":["区域1","区域2"],
                # }
                # cmd = {
                #     "commandId": "42",
                #     "army":[],
                #     "armyNum":0,
                #     "timeLimit": 0,
                #     "startTime": "-1",
                #     "targets":["9号走私艇"]
                # }
                pass
            if frame == 2:
                # cmd = {
                #     "commandId": "41",
                #     "army":[],
                #     "armyNum":0,
                #     "timeLimit": 0,
                #     "startTime": "-1",
                #     "targets":["7号走私艇"]
                # }
                # cmd = {
                #     "commandId": "20",
                #     "army": [
                #         "4号艇", "5号艇"
                #     ],
                #     "targets": ["1号走私艇"],
                #     "equip": [
                #         {
                #             "name": "雷达",
                #             "status": 0
                            
                #         },
                #         {
                #             "name": "光电",
                #             "status": 0
                #         },
                #         {
                #             "name": "红外",
                #             "status": 0
                #         }
                #     ]
                # }
                pass
            if frame == 14118:
                # cmd = {
                #     "commandId": "00",
                #     "army": [
                #         "2号艇"
                #     ],
                #     "targets":[] ,  
                #     "area": ["位置2"],
                #     "timeLimit": 10,
                #     "startTime": "-1"
                # }
                pass
            if frame == 200:
                # cmd = {
                #     "commandId": "20",
                #     "army": [
                #         "4号艇", "2号艇"
                #     ],
                #     "targets": ["10号走私艇"],
                #     "equip": [
                #         {
                #             "name": "雷达",
                #             "status": 0
                            
                #         },
                #         {
                #             "name": "光电",
                #             "status": 0
                #         },
                #         {
                #             "name": "红外",
                #             "status": 0
                #         }
                #     ]
                # }
                # cmd = {
                #     "commandId": "40",
                #     "army":[],
                #     "armyNum":2,
                #     "timeLimit": 30,
                #     "startTime": "-1",
                #     "targets":["1号走私艇"]
                # }
                pass    
            if frame == 5000:
                
                # cmd = {
                #     "commandId": "00",
                #     "army": [
                #         "4号艇"
                #     ],
                #     "targets":[] ,  
                #     "area": [[120.90470310,38.92013395]],
                #     "timeLimit": 1,
                #     "startTime": "-1"
                # }
                # cmd = {
                #     "commandId": "20",
                #     "army": [
                #         "4号艇"
                #     ],
                #     "targets": ["10号走私艇"],
                #     "equip": [
                #         {
                #             "name": "雷达",
                #             "status": 0
                            
                #         },
                #         {
                #             "name": "光电",
                #             "status": 0
                #         },
                #         {
                #             "name": "红外",
                #             "status": 0
                #         }
                #     ]
                # }
                pass

            if cmd is not None:
                TinderPy.log_info(f'此刻有临时指令!!{cmd}')
                try:
                    result = self.make_cmd(cmd=cmd, frame=frame)
                    flag = result # str(result) # "success" if result else "failed" # !这个地方改一下，把为什么不能成功执行的字段也要返回
                except Exception as e:
                    TinderPy.log_info(f'问题make_cmd函数不能成功执行, error: {e}, frame: {frame}')

            # todo 测试 增加蓝方艇被跟踪的数量
            for r_i, loc in self.loc.items():
                if self.follow_enemy[r_i] is not None:
                    self.follow_count[self.follow_enemy[r_i]] += 1
                else:
                    if self.check_task[r_i] is not None:
                        self.follow_count[self.check_task[r_i]] += 1

            # ! 临时指令 --- 查证目标
            for name, value in self.check_task.items(): # 临时查证某个目标任务
                if value is not None and (frame % 150 == 0):
                    # if self.enemies[value] is not None: # !判定死亡的条件要改变
                    if self.enemy_alive[value] > 1:
                        plan = cmdlist.course_maneuver(self.entities[name], 
                                                    f"红方{name}执行临时侦察任务, 侦察{value}.", 
                                                    "0100", 
                                                    [
                                                        # self.enemies[value]
                                                        cmdlist.generate_random_point_nearby(self.enemies[value])
                                                    ], 
                                                    str(cmdlist.high_red_speed))
                        TinderPy.conduct(plan)
                        # ! 记录状态, red name 跟踪 blue value
                        self.red_records[name] = [1, self.entities[name],f"正在跟踪{self.enemies_id[value]}"] # "正在跟踪n号走私艇"
                        TinderPy.log_info(f"此时敌方{value}的位置是: {self.enemies[value]}")
                    else:
                        TinderPy.log_info(f"蓝方{value}已经死亡，不能对齐执行侦察任务!")
                        self.check_task[name] = None # 恢复默认状态
            
            # todo 测试
            ## 临时指令, # * 临时指令执行的时候，所有的执行执行都会失效! ↑ first_check()
            # ! 临时指令 --- 前往目标点，开展巡逻 (只适用于前往某点的情况)
            try:
                for red_item, value in self.forward_points.items(): # * "1号艇": {"goal": None, "patrol_ara": None, "start_partol": None},
                    # goal 是要前往的目标点, # * 平时的时候是空的,下临时指令的时候不为None
                    # partol_ara 是前往到某点之后, 要巡逻的四个点, # * 自动生成，根据lon, lat生成以它为中心，半径1km的正方形区域
                    # start_partol 是是否到达某个点已经开始巡逻了 # * 为True,则已经开始巡逻，否则的话，就没有开始巡逻
                    # TinderPy.log_info(f"4号艇是否安排了侦察巡逻任务？{self.forward_points['4号艇']}")
                    if self.forward_points[red_item]["goal"] is not None: # 当前点不为None，说明下达了前往某点的指令
                        # todo 把前往侦查的指令去掉
                        self.forward_points[red_item]["patrol_ara"] = cmdlist.get_partol_points(self.forward_points[red_item]["goal"])
                        # TinderPy.log_info(f"生成的巡逻区域是: {self.forward_points[red_item]['patrol_ara']}")
                        # self.forward_points[red_item]["patrol_ara"] = [
                        #         [120.86735641,39.03027267], [120.89956524,39.02230281], [120.89288489,38.98985806], [120.84993979,38.99449393]
                        # ]
                        # TinderPy.log_info(f"已经成功对 {red_item} 生成巡逻区域, 以下条件判断 距离：{cmdlist.compute_distance(self.loc[red_item], self.forward_points[red_item]['goal'])}")

                        # 如果判断小于50米的时候，开始巡逻
                        if cmdlist.compute_distance(self.loc[red_item], self.forward_points[red_item]["goal"]) < 1:
                            # TinderPy.log_info(f"{red_item} 执行前往某目标点巡逻的命令,现已到达目标点,开始准备巡逻...") 
                            self.forward_points[red_item]["start_partol"] = True

                        if self.forward_points[red_item]["goal"] is not None and not self.forward_points[red_item]["start_partol"]: # 已经下达了这个指令，并且没有开始巡逻
                            # 前往这个点
                            if frame % 100 == 0:
                                # TinderPy.log_info(f"红方 {red_item} 执行巡逻指令正在前往巡逻点中........")
                                plan = cmdlist.course_maneuver(self.entities[red_item], 
                                                        f"红方{red_item}执行临时指令, 前往某点开展巡逻监控!", 
                                                        "0100", 
                                                        [self.forward_points[red_item]["goal"]], 
                                                        str(cmdlist.high_red_speed))
                                TinderPy.conduct(plan)
                                # ! 记录状态 当前艇正在执行前往目标点巡逻的任务
                                # self.red_records[red_item] = [2, self.entities[red_item],f"正前往目标点{}"] # "n号艇正前往某点巡逻中"
                        
                        elif self.forward_points[red_item]["goal"] is not None and self.forward_points[red_item]["start_partol"]:
                            # TinderPy.log_info(f"红方 {red_item} 到达巡逻点，已经开始巡逻...")
                            # 前往这个点，并且已经开始巡逻
                            # 巡逻取索引
                            try:
                                cur_index = self.forward_points[red_item]["partol_index"]
                                if frame % 100 == 0:
                                    try:
                                        plan = cmdlist.course_maneuver(self.entities[red_item], 
                                                                    f"红方{red_item}执行临时指令, 前往某点开展巡逻监控!", 
                                                                    "0100", 
                                                                    [self.forward_points[red_item]["patrol_ara"][cur_index]], 
                                                                    str(cmdlist.high_red_speed))
                                        TinderPy.conduct(plan)
                                        TinderPy.log_info(f"{red_item} 正在执行前进巡逻的指令!!!")
                                        # ! 记录状态
                                        self.red_records[red_item] = [0, self.entities[red_item], f"正在定点巡逻中"] # ! 目标点巡逻 + 目标点
                                        
                                    except Exception as e:
                                        TinderPy.log_error(f"前往目标点执行巡逻出现问题，不会动!!!!!!")

                                    # TinderPy.log_info(f"红方{red_item}执行临时指令,开始在巡逻区执行巡逻,当前执行的索引是:{cur_index}")
                                
                                    if cmdlist.compute_distance(self.loc[red_item], self.forward_points[red_item]["patrol_ara"][cur_index]) < 1:
                                        before_index = self.forward_points[red_item]["partol_index"]
                                        # 更新新的索引
                                        self.forward_points[red_item]["partol_index"] = (before_index+1) % len(self.forward_points[red_item]["patrol_ara"])
                                        # TinderPy.log_info(f"之前的索引是: {before_index}, 更新的索引是: {self.forward_points[red_item]['partol_index']}")
                            except Exception as e:
                                TinderPy.log_info(f"问题: ?????????????????????????????? {e}")
                    
                    # 循环执行这个指令
            except Exception as e:
                TinderPy.log_error(f"执行临时指令, 前往目标点巡逻出现问题: {e}")

            # 根据当前态势做出动作
            if frame == 0:
                # 只有第一帧更新所有实体ID信息
                for r_item in red_all_forces:
                    self.entities[f'{r_item.get_name()}'] = r_item.get_id()
                    self.entities_class[f'{r_item.get_name()}'] = r_item
                for b_item in TinderPy.get_blue_forces():
                    self.enemies_id[f'{b_item.get_name()}'] = b_item.get_id()
                    self.ID_NAME = {str(value): key for key, value in self.enemies_id.items()}

                # 9,10 从南到北开启巡逻
                plan = cmdlist.course_maneuver(self.entities["7号艇"], 
                                                "红方7号艇开始沿海岸线巡逻", 
                                                "0100", 
                                                self.patrol_lines_s2n_7, 
                                                str(cmdlist.high_red_speed))
                TinderPy.conduct(plan)
                # ! 记录状态
                self.red_records["7号艇"] = [0, self.entities["7号艇"],f"正在沿航线巡逻"] # [0, "n号艇正在巡逻中或正在前往巡逻途中"] 代表正在执行区域的巡逻任务
                plan = cmdlist.course_maneuver(self.entities["8号艇"], 
                                                "红方8号艇开始沿海岸线巡逻", 
                                                "0100", 
                                                self.patrol_lines_s2n_8, 
                                                str(cmdlist.high_red_speed))
                TinderPy.conduct(plan)   
                # ! 记录状态
                self.red_records["8号艇"] = [0, self.entities["8号艇"],f"正在沿航线巡逻"]
                plan = cmdlist.course_maneuver(self.entities["9号艇"], 
                                                "红方9号艇开始沿海岸线巡逻", 
                                                "0100", 
                                                self.patrol_lines_n2s_9, 
                                                str(cmdlist.high_red_speed))
                TinderPy.conduct(plan)
                # ! 记录状态
                self.red_records["9号艇"] = [0, self.entities["9号艇"], f"正在沿航线巡逻"]
                
                # 外围所有的船执行巡逻区任务 0 5 1 3 2 4
                plan1 = cmdlist.area_patrol(self.entities["1号艇"], "0103", 2) #  0)
                plan2 = cmdlist.area_patrol(self.entities["2号艇"], "0103", 3) # 5)
                plan3 = cmdlist.area_patrol(self.entities["3号艇"], "0103", 4) # 1)
                plan4 = cmdlist.area_patrol(self.entities["4号艇"], "0103", 1) # 3)
                plan5 = cmdlist.area_patrol(self.entities["5号艇"], "0103", 0) # 2)
                plan6 = cmdlist.area_patrol(self.entities["6号艇"], "0103", 5) # 4)
                for pl in [plan1, plan2, plan3, plan4, plan5, plan6]:
                    TinderPy.conduct(pl)
                
                # ! 记录状态
                self.red_records["1号艇"] = [0, self.entities["1号艇"], f"正在区域-{3}巡逻中"]
                self.red_records["2号艇"] = [0, self.entities["2号艇"], f"正在区域-{4}巡逻中"]
                self.red_records["3号艇"] = [0, self.entities["3号艇"], f"正在区域-{5}巡逻中"]
                self.red_records["4号艇"] = [0, self.entities["4号艇"], f"正在区域-{2}巡逻中"]
                self.red_records["5号艇"] = [0, self.entities["5号艇"], f"正在区域-{1}巡逻中"]
                self.red_records["6号艇"] = [0, self.entities["6号艇"], f"正在区域-{6}巡逻中"]

                # # ! 更新当前巡逻区艇的数量
                # self.partol_num[str(0)] += 1
                # self.partol_num[str(1)] += 1
                # self.partol_num[str(2)] += 1
                # self.partol_num[str(3)] += 1
                # self.partol_num[str(4)] += 1
                # self.partol_num[str(5)] += 1


            # ! 7,8,9号艇按照航线进行巡逻，当到达这个航线的最后一个点时(判断距离是否小于500米)，然后执行新的航线
            ## 先查看当前索引
            if self.partol_7_direction == 1: # 从南往北
                # 判断是否7号艇距离最后一个点小于200米
                if cmdlist.compute_distance(self.loc["7号艇"], self.patrol_lines_s2n_7[-1]) < 0.2 and self.partol_7_curr_index:
                    # 下一个逆向的指令
                    self.partol_7_direction = -1
                    self.partol_7_curr_index = False
                    plan = cmdlist.course_maneuver(self.entities["7号艇"], 
                                                    "红方7号艇沿海岸线巡逻", 
                                                    "0100", 
                                                    self.patrol_lines_n2s_7, 
                                                    str(cmdlist.high_red_speed))
                    TinderPy.conduct(plan)
            elif self.partol_7_direction == -1: # 代表从北往南
                if cmdlist.compute_distance(self.loc["7号艇"], self.patrol_lines_n2s_7[-1]) < 0.2 and not self.partol_7_curr_index:
                    # 下一个逆向的指令
                    self.partol_7_direction = 1
                    self.partol_7_curr_index = True
                    plan = cmdlist.course_maneuver(self.entities["7号艇"], 
                                                    "红方7号艇沿海岸线巡逻", 
                                                    "0100", 
                                                    self.patrol_lines_s2n_7, 
                                                    str(cmdlist.high_red_speed))
                    TinderPy.conduct(plan)
            if self.partol_8_direction == 1: # 从南往北
                # 判断是否7号艇距离最后一个点小于200米
                if cmdlist.compute_distance(self.loc["8号艇"], self.patrol_lines_s2n_8[-1]) < 0.2 and self.partol_8_curr_index:
                    # 下一个逆向的指令
                    self.partol_8_direction = -1
                    self.partol_8_curr_index = False
                    plan = cmdlist.course_maneuver(self.entities["8号艇"], 
                                                    "红方8号艇沿海岸线巡逻", 
                                                    "0100", 
                                                    self.patrol_lines_n2s_8, 
                                                    str(cmdlist.high_red_speed))
                    TinderPy.conduct(plan)
            elif self.partol_8_direction == -1: # 代表从北往南
                if cmdlist.compute_distance(self.loc["8号艇"], self.patrol_lines_n2s_8[-1]) < 0.2 and not self.partol_8_curr_index:
                    # 下一个逆向的指令
                    self.partol_8_direction = 1
                    self.partol_8_curr_index = True
                    plan = cmdlist.course_maneuver(self.entities["8号艇"], 
                                                    "红方8号艇沿海岸线巡逻", 
                                                    "0100", 
                                                    self.patrol_lines_s2n_8, 
                                                    str(cmdlist.high_red_speed))
                    TinderPy.conduct(plan)
            if self.partol_9_direction == 1: # 从南往北
                # 判断是否7号艇距离最后一个点小于200米
                if cmdlist.compute_distance(self.loc["9号艇"], self.patrol_lines_n2s_9[-1]) < 0.2 and self.partol_9_curr_index:
                    # 下一个逆向的指令
                    self.partol_9_direction = -1
                    self.partol_9_curr_index = False
                    plan = cmdlist.course_maneuver(self.entities["9号艇"], 
                                                    "红方9号艇沿海岸线巡逻", 
                                                    "0100", 
                                                    self.patrol_lines_s2n_9, 
                                                    str(cmdlist.high_red_speed))
                    TinderPy.conduct(plan)
            elif self.partol_9_direction == -1: # 代表从北往南
                if cmdlist.compute_distance(self.loc["9号艇"], self.patrol_lines_s2n_9[-1]) < 0.2 and not self.partol_9_curr_index:
                    # 下一个逆向的指令
                    self.partol_9_direction = 1
                    self.partol_9_curr_index = True
                    plan = cmdlist.course_maneuver(self.entities["9号艇"], 
                                                    "红方9号艇沿海岸线巡逻", 
                                                    "0100", 
                                                    self.patrol_lines_n2s_9, 
                                                    str(cmdlist.high_red_speed))
                    TinderPy.conduct(plan)

            detects_red_true = TinderPy.get_red_detected_situation()

            # ! 所有的动作都是在探测到敌方之后，才能够执行
            if len(detects_red_true) > 0:
                # 当敌方某个蓝方艇进入到探测范围时，安排红方艇前去首次侦察
                for blue_item in detects_red:   
                    cur_enemy_name = blue_item.get_name()
                    # TinderPy.log_info(f"当前的敌方艇是: {cur_enemy_name}")
                    if self.enemy_alive[cur_enemy_name] > 1: # 还活着
                        if cmdlist.compute_distance(POC_LOC, self.enemies[cur_enemy_name]) < 60: # 说明这个敌方已经进入到红方探测气球范围内了
                            for red, blue in self.follow_enemy.items():
                                if not self.start_check[red]: # 说明该红方还没有开始第一波侦察任务 
                                    # red是跟随放, blue是被跟随方
                                    if blue == cur_enemy_name: # 如果red的跟随blue是当前的艇
                                        TinderPy.log_info(f"{int(red.split('号')[0])} 号艇==开始执行侦察任务对=={blue}")
                                        self.counter[str(int(red.split('号')[0]))] = 100000 # 红方可以开始任务跟随了，有个问题就是 // 这个函数会一直循环，然后counter一直是1000
                                        self.start_check[red] = True
                                else:
                                    pass
                
                # 各艇首次侦察
                for red_item, id in self.entities.items():
                    if red_item != "系留探测飞艇-1":
                        try:
                            if self.check_task[red_item] is None and self.forward_points[red_item]["goal"] is None:
                                self.first_check(frame=frame, red_name=f"{int(red_item.split('号')[0])}")
                        
                        except Exception as e:
                            TinderPy.log_info(f"循环执行first_check, 有问题!!! {red_item}, {e}")

                # todo 巡逻艇的收割逻辑，7,8,9最后,当有艇进入他的探测范围时，那么它的follow目标就立刻设置成那个蓝方艇
                            
                ## todo 临时指令级别高于一切指令，所有指令执行的时候，要优先判断当前是否有临时指令，尤其是机动指令
                
                ## 武器攻击（可以对任何艇进行攻击）
                # todo 攻击准则：1）任何艇都可以打击；2) 4km范围内，360可以发送震撼弹打击，通过判断位置：当与敌艇的上一帧的距离要比上上帧和当前帧都要低的时候，或者是2km以内就可以发送；3）发送微波武器
                # todo 只要角度合适就可以
                try:
                    for red_item, location in self.loc.items():
                        if red_item != "系留探测飞艇-1":
                            for blue_item, cur_loc in self.enemies.items():
                                if self.enemy_alive[blue_item] > 1: # !蓝方没有死亡，才能攻击它
                                        # 红方和当前的蓝方的距离
                                        # 上上帧
                                        lastlast_dis = cmdlist.compute_distance(self.enemies_last[blue_item][0], self.loc_last[red_item][0])
                                        # 上帧
                                        last_dis = cmdlist.compute_distance(self.enemies_last[blue_item][1], self.loc_last[red_item][1])
                                        # 当前帧
                                        dis = cmdlist.compute_distance(self.enemies[blue_item], self.loc[red_item])
                                        # todo 计算，如果跟敌方是呈追击状态，那么射击距离就是3km；如果是面对面的，那么就是4km发射。
                                        # * 震撼弹: 最优距离判断 + 射击间隔判断 + 弹药量判断 200 帧间隔
                                        if ((last_dis < lastlast_dis and last_dis < dis and dis < 3.5) or dis < 3.5) and self.shoot_interval[red_item][0] == 0 and \
                                                        self.shoot_interval[red_item][2] >= 2: # # !此时判断弹药量是模拟的
                                            # 射击间隔加 # ! 射击间隔记得每帧清0
                                            self.shoot_interval[red_item][0] = self.swb_interval
                                            # 弹药量-2
                                            self.shoot_interval[red_item][2] -= 2
                                            # 下达震撼弹攻击指令
                                            TinderPy.log_info(f"红方 {red_item} 满足震撼弹使用条件!")
                                            plan = cmdlist.dd_attack(self.entities[red_item], 
                                                                            "DD打击", 
                                                                            "0108", 
                                                                            [self.enemies_id[blue_item]])
                                            Flag = TinderPy.conduct(plan)
                                            TinderPy.log_info(f"红方 {red_item} 发送两颗震撼弹攻击 >>>>>> {blue_item}, 上一帧距离: {last_dis} km, 上上帧距离: {lastlast_dis} km, 当前距离: {dis} km. Result: {Flag}")
                                        
                                        else:
                                            # todo 测试 加入机枪效果
                                            if dis < 2 and self.shoot_interval_gun[red_item]:
                                                self.shoot_interval_gun[red_item] = False
                                                plan = cmdlist.gun_attack(self.entities[red_item], 
                                                                            "DD打击", 
                                                                            "0108", 
                                                                            [self.enemies_id[blue_item]])
                                                
                                                Flag = TinderPy.conduct(plan)
                                                TinderPy.log_info(f"红方 {red_item} 使用机枪攻击 >>> {blue_item}")
                                            
                                        # 微波武器: 角度判断 + 距离判断 + 射击间隔判断 # // 2000 帧间隔
                                        relative_angle, if_can_shoot_flag = cmdlist.if_can_microwave(self.loc[red_item][0], self.loc[red_item][0], 
                                                                                self.heading[red_item][0], self.enemies[blue_item][0], self.enemies[blue_item][1]) 

                                        if dis < 0.35 and if_can_shoot_flag and self.shoot_interval[red_item][1] == 0:
                                            try:
                                                TinderPy.log_info(f"{red_item} 使用微波武器对 {blue_item}具备条件!")
                                                # 射击间隔加
                                                self.shoot_interval[red_item][1] = self.wave_interval
                                                plan = cmdlist.microwave_attack(
                                                        self.entities[red_item],
                                                        "微波武器打击",
                                                        "0108",
                                                        [self.enemies_id[blue_item]]
                                                )
                                                Flag = TinderPy.conduct(plan)
                                                TinderPy.log_info(f"{blue_item} 被使用微波武器后，血量还有: {self.enemy_alive[blue_item]},{Flag}")
                                            except Exception as e:
                                                TinderPy.log_error(f"问题 不能正确使用微波武器！！")
                except Exception as e:
                    TinderPy.log_error(f"当前艇 {red_item} 在面对 {blue_item} 执行武器攻击指令时出现问题!")

                # todo 测试
                ## 更换目标（
                # 必须要等当前的艇死亡了之后，才可以更换目标; 
                # // 还有就是红方追逐超过探测圈之后，也会更换；） 
                # 敌方到达目标点
                try:
                    for red_item, follow_enemy in self.follow_enemy.items():
                        if follow_enemy is not None: #  如果艇的跟随不是空 到达港口 + 生命值 < 1 + 
                            if (self.enemy_alive[follow_enemy] <= 5 or \
                                cmdlist.compute_distance(self.enemies[follow_enemy], self.trading["trade1"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[follow_enemy], self.trading["trade2"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[follow_enemy], self.trading["trade3"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[follow_enemy], self.trading["trade4"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[follow_enemy], self.trading["trade5"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[follow_enemy], self.trading["trade6"]) < 1) and frame % 100 == 0: # 敌方艇距离任意一个港口距离小于50米的时候
                                    
                                    # 去寻找离他最近的蓝方艇
                                    recent_avlive_blue = None
                                    recent_dis = 9999999999
                                    for blue_item, b_loc in self.enemies.items():
                                        if blue_item != follow_enemy:
                                            # todo 加一个模块, 当想要跟踪的这个艇，数量不超过2才可以继续判断 (可以通过self.check_task和self.follow_enemy)
                                            if self.follow_count[blue_item] >= 2:
                                                continue
                                            # 距离最短 + 敌方还活着 + 只拦截圈内的
                                            # ? if cmdlist.compute_distance(location, b_loc) < recent_dis and  \
                                            if cmdlist.compute_distance(self.loc[red_item], b_loc) < recent_dis and cmdlist.compute_distance(self.loc[red_item], b_loc) < 8 and \
                                                self.enemy_alive[blue_item] > 1 and \
                                                    cmdlist.compute_distance(b_loc, POC_LOC) < 60 and \
                                                    (cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade1"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade2"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade3"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade4"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade5"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade6"]) > 5): # ! 这个地方增加了, 不能选到达交易点的船
                                                    
                                                    recent_avlive_blue = blue_item
                                                    # recent_dis = cmdlist.compute_distance(location, b_loc)
                                                    recent_dis = cmdlist.compute_distance(self.loc[red_item], b_loc)
                                    
                                    TinderPy.log_info(f"红方 {red_item} 跟随的目标 {follow_enemy} 已经失效, 重新选择新的目标: {recent_avlive_blue}")

                                    if recent_avlive_blue is None:
                                        # 如果都不符合条件的话，回到巡逻区去巡逻
                                        self.counter[red_item] = 0
                                        self.follow_enemy[red_item] = None
                                        # self.check_task[red_item] = None # 侦察敌方的任务没有必要了
                                        # TinderPy.log_info(f"红方 {red_item} 没有最佳跟随目标，返回继续巡逻! - 2")
                                        # 选择一个巡逻区
                                        recent_partol = None
                                        recent_dis = 99999
                                        for p_id, loc in self.partol_center.items():
                                            # ? if cmdlist.compute_distance(location, loc) < recent_dis:
                                            if cmdlist.compute_distance(self.loc[red_item], loc) < recent_dis: # ! 加判断条件,并且当前巡逻区的数量不超过2,否则，返回港口待命
                                                # if self.partol_num[str(p_id)] < 2:
                                                # ? recent_dis = cmdlist.compute_distance(location, loc)
                                                # todo 红方避让,当判断与目标区域的连线穿过岛屿时，就会产生避让效果
                                                recent_dis = cmdlist.compute_distance(self.loc[red_item], loc)
                                                recent_partol = p_id
                                                # else:
                                                #     pass
                                        
                                        if recent_partol is not None: 
                                            plan = cmdlist.area_patrol(self.entities[red_item], "0103", int(recent_partol))
                                            TinderPy.conduct(plan)
                                            # ! 记录状态
                                            self.red_records[red_item] = [0, self.entities[red_item], f"正在区域-{int(recent_partol)+1}巡逻中"]
                                            TinderPy.log_info(f"红方 {red_item} 没有最佳跟随目标，返回继续巡逻 -- 2 巡逻区是: {int(recent_partol)}!")
                                            # self.partol_num[str(recent_partol)] += 1
                                            # # ! 要更新蓝方的状态
                                            # if self.enemy_alive[follow_enemy] <= 5:
                                            #     # 说明这个蓝方艇已经死亡了
                                            #     self.blue_records[self.enemy_alive[follow_enemy]] = []
                                        else: # ! 说明巡逻区最后都已经满了, 舰艇返回港口待命
                                            # todo 测试 ! 为了防止会产生穿过岛的情况,原地巡逻
                                            self.forward_points[red_item]["goal"] = self.loc[red_item]
                                            self.forward_points[red_item]["start_partol"] = True
                                            self.forward_points[red_item]["patrol_ara"] = cmdlist.get_partol_points(self.forward_points[red_item]["goal"])
                                            pass
                                            

                                    else:
                                        TinderPy.log_info(f"红方 {red_item} 不继续跟踪目标，成功更换目标 → {recent_avlive_blue}")
                                        # 否则，就改变跟踪对象
                                        self.counter[red_item] = 100000
                                        self.follow_enemy[red_item] = recent_avlive_blue
                                        # ! 记录状态
                                        self.red_records[red_item] = [1, self.entities[red_item], f"正在跟踪{self.enemies_id[recent_avlive_blue]}"]
                            else:
                                try:
                                    if frame % 100 == 0:
                                        if self.follow_enemy[red_item] is not None:
                                            goal_distance = cmdlist.compute_distance(self.loc[red_item], self.enemies[self.follow_enemy[red_item]])
                                            cur_goal = self.follow_enemy[red_item]
                                            # ! 加一个，当附近有比目标更近的艇时，也会去更新目标
                                            for blue_item, location in self.enemies.items():
                                                if blue_item != self.follow_enemy[red_item]:
                                                    if self.follow_count[blue_item] >= 2:
                                                        continue
                                                    # ? 条件是不仅要近，还要小于6km才可以, 而且不是同一艘, 而且生命值>1
                                                    if cmdlist.compute_distance(self.loc[red_item], self.enemies[blue_item]) < goal_distance and \
                                                        cmdlist.compute_distance(self.loc[red_item], self.enemies[blue_item]) < 8 and \
                                                            cmdlist.compute_distance(POC_LOC, self.enemies[blue_item]) < 60 and \
                                                            self.enemy_alive[blue_item]>1:
                                                        goal_distance = cmdlist.compute_distance(self.loc[red_item], self.enemies[blue_item])
                                                        cur_goal = blue_item
                                            # ! 改 1108_22:09
                                            if self.follow_enemy[red_item] != cur_goal:
                                                TinderPy.log_info(f"红方 {red_item} 在追逐蓝方 {follow_enemy} 的过程中,发现更近的目标 → {cur_goal}, 遂更换目标, 当前的目标是: {self.follow_enemy[red_item]}")
                                                self.follow_enemy[red_item] = cur_goal # ? 更换目标
                                                self.counter[red_item] = 100000
                                                # ! 记录状态
                                                self.red_records[red_item] = [1, self.entities[red_item], f"正在跟踪{self.enemies_id[cur_goal]}"]

                                            # todo 判断当前听是否在执行临时巡逻的指令，如果是，则清空巡逻指令，更换目标追击
                                            if self.forward_points[red_item]["goal"] is not None:
                                                self.forward_points[red_item]["goal"] = None
                                                self.forward_points[red_item]["patrol_ara"] = None 
                                                self.forward_points[red_item]["start_partol"] = False
                                                self.forward_points[red_item]["partol_index"] = 0
                                            # if cur_goal != self.follow_enemy[red_item]:
                                                
                                except Exception as e:
                                    TinderPy.log_error(f"红方 {red_item} 更换目标出现问题! error: {e}")
                        
                        else: # 当跟随目标是None时，会分配目标，20km以内并且距离所有的trade都在5km以上并且是活的
                            try:
                                if frame % 100 == 0: 
                                    # 当跟随的follow_enemy是空时,要及时更换目标,并且要寻找最近的敌人
                                    new_follow_item = None
                                    new_follow_distance = 9999999999999
                                    check_distance = 20 if red_item == '7号艇' or red_item == '8号艇' or red_item == '9号艇' else 12
                                    for blue_item, location in self.enemies.items():
                                        if self.follow_count[blue_item] >= 2:
                                                continue
                                        if cmdlist.compute_distance(self.loc[red_item], self.enemies[blue_item]) < new_follow_distance and \
                                            cmdlist.compute_distance(self.loc[red_item], self.enemies[blue_item]) < check_distance and \
                                            self.enemy_alive[blue_item] > 1 and \
                                            cmdlist.compute_distance(POC_LOC, self.enemies[blue_item]) < 60 and \
                                            (cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade1"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade2"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade3"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade4"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade5"]) > 5 and \
                                                    cmdlist.compute_distance(self.enemies[blue_item], self.trading["trade6"]) > 5): # 并且要小于10km，并且敌方没有完成任务
                                            new_follow_distance = cmdlist.compute_distance(self.loc[red_item], self.enemies[blue_item])
                                            new_follow_item = blue_item
                                    
                                    if new_follow_item is not None:
                                        TinderPy.log_info(f"查看 {red_item} 没有跟随艇, 给他加目标 {new_follow_item}")
                                        self.counter[red_item] = 100000
                                        self.follow_enemy[red_item] = new_follow_item
                                        # ! 记录状态
                                        self.red_records[red_item] = [1, self.entities[red_item], f"正在跟踪{self.enemies_id[new_follow_item]}"]

                            except Exception as e:
                                TinderPy.log_info(f"没有目标的艇重新选择目标失败!出现问题!")
                                
                except Exception as e:
                    TinderPy.log_error(f"红方艇 {red_item} 替换目标失败, 出现问题: {e}")

                try:
                    # todo 测试
                    ## 红方追逐超过了探测圈，则优先先追逐自己离自己最近的目标，如果所有目标都死掉了，则回去巡逻
                    for red_item, location in self.loc.items():
                        # 判断红方是否超出了探测范围，如果超出了，那么就从新分配目标
                        if cmdlist.compute_distance(self.loc[red_item], POC_LOC) >= 60 and frame % 100 == 0 and \
                            self.check_task[f"{red_item}"] is None and \
                                self.forward_points[f"{red_item}"]["goal"] is None: # 红方超出了探测范围, # !但是当临时指令时，则不需要考虑
                            TinderPy.log_info(f"红方 {red_item} 追逐 {self.follow_enemy[red_item]} 过程中已经超出了气球探测范围: 61KM, 正在更换目标或者回去巡逻!")
                            try:
                                # 去寻找离他最近的蓝方艇
                                recent_avlive_blue = None
                                recent_dis = 9999999999
                                for blue_item, b_loc in self.enemies.items():
                                    # 距离最短 + 敌方还活着 + 只拦截圈内的
                                    if cmdlist.compute_distance(self.loc[red_item], b_loc) < recent_dis and  \
                                        self.enemy_alive[blue_item] > 1 and \
                                            cmdlist.compute_distance(b_loc, POC_LOC) < 60:
                                            recent_avlive_blue = blue_item
                                            recent_dis = cmdlist.compute_distance(location, b_loc)
                                
                                if recent_avlive_blue is None:
                                    # 如果都不符合条件的话，回到巡逻区去巡逻
                                    self.counter[red_item] = 0
                                    self.follow_enemy[red_item] = None
                                    
                                    # 选择一个巡逻区
                                    recent_partol = None
                                    recent_dis = 99999
                                    for p_id, loc in self.partol_center.items():
                                        if cmdlist.compute_distance(self.loc[red_item], loc) < recent_dis:
                                            recent_dis = cmdlist.compute_distance(self.loc[red_item], loc)
                                            recent_partol = p_id
                                    plan = cmdlist.area_patrol(self.entities[red_item], "0103", int(recent_partol))
                                    TinderPy.log_info(f"红方 {red_item} 超出探测圈, 没有最佳跟随目标，返回继续巡逻, 巡逻区是: {int(recent_partol)}!")
                                    TinderPy.conduct(plan)
                                    # todo 描述待修改→正在巡逻或正在前往巡逻途中
                                    # ! 记录状态
                                    self.red_records[red_item] = [0, self.entities[red_item], f"正在区域-{int(recent_partol)+1}巡逻中"]

                                else:
                                    TinderPy.log_info(f"红方 {red_item} 不继续跟踪目标，成功更换目标 → {recent_avlive_blue}")
                                    # 否则，就改变跟踪对象
                                    self.counter[red_item] = 100000
                                    self.follow_enemy[red_item] = recent_avlive_blue
                                    # ! 记录状态
                                    self.red_records[red_item] = [1, self.entities[red_item], f"正在跟踪{self.enemies_id[recent_avlive_blue]}"]
                            
                            except Exception as e:
                                TinderPy.log_error(f"红方艇 {red_item} 追逐超过红色探测圈, 重新规划任务失败,出现问题, 错误是: {e}")
                
                except Exception as e:
                    TinderPy.log_info(f"判断是否出探测圈是出现问题: {e}")
                    
                    pass
                pass
        
        except Exception as e:
            error_message = traceback.format_exc()  # 获取完整的错误信息和行号
            TinderPy.log_info(f"Policy act总函数有问题: {error_message}")

        # # ! 整理蓝方态势，看每个艇被谁跟踪
        # for r_i, loc in self.loc.items():
        #     if self.follow_enemy[r_i] is not None:
        #         self.follow_count[self.follow_enemy[r_i]] += 1
        #     else:
        #         if self.check_task[r_i] is not None:
        #             self.follow_count[self.check_task[r_i]] += 1
        
        for bitem, status in self.blue_records.items():
            newstatus = [] # ! 清空上一帧的记录
            # 在这个地方加入到达交易点或者是死亡
            if self.enemy_alive[bitem] <= 5:
                # 该蓝方艇已经死亡
                newstatus.append(int(0))
            elif (cmdlist.compute_distance(self.enemies[bitem], self.trading["trade1"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[bitem], self.trading["trade2"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[bitem], self.trading["trade3"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[bitem], self.trading["trade4"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[bitem], self.trading["trade5"]) < 1 or \
                                cmdlist.compute_distance(self.enemies[bitem], self.trading["trade6"]) < 1):
                # 该蓝方艇已经到达目标交易点
                newstatus.append(int(1))
            
            # 需要更新一个蓝被跟踪状态改变的情况

            else: 
                for r_i, loc in self.loc.items():
                    if self.follow_enemy[r_i] is not None and self.follow_enemy[r_i] == bitem:
                        newstatus.append(r_i)
                    else:
                        if self.check_task[r_i] is not None and self.check_task[r_i] == bitem:
                            newstatus.append(r_i)
            
            # 最后添加上蓝方的forceid
            newstatus.append(self.enemies_id[bitem])
            # TinderPy.log_info(f"*********已经添加: {newstatus}, {bitem}的id是{self.enemies_id[bitem]}")
            self.blue_records[bitem] = newstatus

        RETURN_TOTAL = {
            "flag": None, "red_records": None, "blue_records": None
        }

        RETURN_TOTAL["flag"] = flag

        if self.red_records != self.last_red_records:
            # TinderPy.log_info(f"当前帧 {frame} 执行任务发生变化!===== last records: {self.last_red_records['7号艇']} records: {self.red_records['7号艇']}")
            # return_data = [flag, self.red_records]
            RETURN_TOTAL["red_records"] = self.red_records
        else:
            # TinderPy.log_info(f"当前帧 {frame} 执行任务未发生变化!+++++ last records: {self.last_red_records['7号艇']} records: {self.red_records['7号艇']}")
            # return_data =  [flag]
            RETURN_TOTAL["red_records"] = None
        
        if self.last_blue_records != self.blue_records:
            RETURN_TOTAL["blue_records"] = self.blue_records
        else:
            pass

        self.last_red_records = copy.deepcopy(self.red_records)
        self.last_blue_records = copy.deepcopy(self.blue_records)

        return RETURN_TOTAL


    def make_cmd(self, cmd=None, frame=None):
        """接收临时指令, 判断是否能执行
        
        航行指令: 
            到指令位置 00 # /// 02 
            # // 到指定区域 01
            待机 03 (没有航行操作, 只有雷达操作)
            目标查证跟踪、监视 20 / 21 # // ? 要时刻跟进吗？怎么样发送紧跟的指令 接口询问？
            # //任务取消 23 接口询问？
            # //构建巡逻警戒线 30 (需要多个艇同时满足条件)
            # //构建巡逻区域 31 
            协同查证、跟踪监视 (并不指定具体是哪个兵力去执行操作) 40 / 41

        打击指令：
            打击摧毁 22 
            协同打击摧毁 42
            # //协同打击确认 43
        
        Return: 
            [flag, str()] # ? 返回是否正确执行,如果不能正确执行,则返回为什么不能正确执行。

        """
        try:
            flag = None # 设置初始字符串
            TinderPy.log_info(f'cmd函数接收到的指令是: {cmd}, {cmd["commandId"]}')
            if cmd is None:
                return flag
            else:
                cmd_id = cmd["commandId"]
                # ? 40 41 42
                if cmd_id == "40" or cmd_id == "41" or cmd_id == "42" or cmd_id == "43":
                    """协同控制
                    """
                    target = cmd["targets"][0] # x号自杀艇 target 是ID，改成name
                    target = self.ID_NAME[str(target)]
                    if self.enemies[target] is None:
                        # 如果该艇死亡，那么任务取消
                        TinderPy.log_error("如果该艇死亡，那么任务取消")
                        return False # error: 该艇已经死亡，无法对齐执行任务!
                    target_id = self.enemies_id[target] # 目标id
                    target_loc = self.enemies[target] # 目标位置
                    choose_entity = None
                    recent_dis = 9999999999
                    # 先寻找最近的兵力
                    for eneties in [
                        "1号艇", "2号艇", "3号艇", "4号艇", "5号艇", "6号艇",
                        "9号艇", "10号艇", "11号艇", "12号艇" # 7,8号艇始终执行巡逻任务，除特殊情况不能离开巡逻区域
                    ]:
                        if frame > self.red_enetity_free_time[eneties]:
                            if cmdlist.compute_distance(self.loc[eneties], target_loc) < recent_dis:
                                choose_entity = eneties
                                recent_dis = cmdlist.compute_distance(self.loc[choose_entity], target_loc)
                        else:
                            continue
                    TinderPy.log_info(f"最后选择执行任务的艇是：{choose_entity}")
                    
                    if choose_entity == None:
                        TinderPy.log_info("当前没有空闲的实体执行对目标的协同任务!")
                        return False # error: 当前时刻红方实体均有任务, 因此无法执行协同任务
                    
                    if cmd_id == "40":
                        """寻找最近的兵力去查证"""
                        TinderPy.log_info(f'{choose_entity}开始执行临时指令--前往侦察走私艇{cmd_id}')
                        target = cmd["targets"][0] # 传进来的是一个list，因此读取第0个
                        self.check_task[choose_entity] = target
                        self.forward_points[army_name]["goal"] = None
                        self.forward_points[army_name]["patrol_ara"] = None 
                        self.forward_points[army_name]["start_partol"] = False
                        self.forward_points[army_name]["partol_index"] = 0
                        pass

                    elif cmd_id == "41":
                        """寻找最近的兵力去跟踪"""
                        TinderPy.log_info(f'{choose_entity}开始执行临时指令--前往跟踪目标{cmd_id}')
                        target = cmd["targets"][0] # 传进来的是一个list，因此读取第0个
                        self.check_task[choose_entity] = target
                        self.forward_points[army_name]["goal"] = None
                        self.forward_points[army_name]["patrol_ara"] = None 
                        self.forward_points[army_name]["start_partol"] = False
                        self.forward_points[army_name]["partol_index"] = 0

                    elif cmd_id == "42":
                        """寻找最近的兵力去打击"""
                        if recent_dis < 4:
                            TinderPy.log_info(f"{choose_entity}成功执行42指令，摧毁敌方 {target}")
                            plan = cmdlist.dd_attack(self.entities[choose_entity], "DD打击", "0108", [target_id])
                            TinderPy.conduct(plan)
                        else:
                            TinderPy.log_info("我方所有兵力都不能打击到该敌方，最短距离是：{recent_dis}")
                            return False # error: 该敌方此刻在我方所有实体的打击范围外，因此不能执行临时打击命令!
                    elif cmd_id == "43":
                        """确认打击"""
                        pass
                # ? 00 03 20 21 22
                else:
                    """单实体控制指令
                    """
                    free_armies = []
                    armies = cmd["army"] # 拿到敌方
                    TinderPy.log_info(f"下达指令的实体是:{armies}")
                    for army in armies:
                        # 优先过滤掉不能只能执行任务
                        if self.red_enetity_free_time[army] > frame:
                            continue
                        else:
                            free_armies.append(army)
                    
                    TinderPy.log_info(f"接收临时指令的实体是:{free_armies}")
                    
                    if len(free_armies) == 0:
                        TinderPy.log_info(f"当前没有实体有空闲时间执行!")
                        flag = [False, "下指令的红方艇现均有任务，建议执行其他任务!"] 
                        return flag # ? 应该不会有这种情况, 当前所有的艇都优先服从临时指令
                    else:
                        for army_name in free_armies:
                            if cmd_id == "00":
                                TinderPy.log_info(f'{army_name}开始执行临时指令--航行至某点进行巡逻任务{cmd_id}')
                                time = cmd["timeLimit"] * 60 # 单位：s
                                # area = cmd["area"][0]
                                # point = self.point[area]
                                # point = cmd["area"][0]
                                point = [cmd["areaPoints"][0][0], cmd["areaPoints"][0][1]]
                                # v = cmdlist.compute_distance(self.loc[army_name], point) * 1000 / time # 单位: m/s
                                v = cmdlist.high_red_speed # min(v, cmdlist.high_red_speed) # v不能超过最大速度
                                TinderPy.log_info(f'行进速度是:{v}')
                                plan = cmdlist.course_maneuver(self.entities[army_name], 
                                                            f"红方{army_name}号艇执行临时指令-00, 航行至坐标点: {point}", 
                                                            "0100", 
                                                            [point], 
                                                            str(v))
                                TinderPy.conduct(plan)
                                # ! 定义字典
                                self.forward_points[army_name]["goal"] = point
                                # ! add 如果又来一条指令让这个艇去别的敌方巡逻，那么要把之前的节点信息清空。 "1号艇": {"goal": None, "patrol_ara": None, "start_partol": False, "partol_index": 0}
                                self.forward_points[army_name]["patrol_ara"] = None 
                                self.forward_points[army_name]["start_partol"] = False
                                self.forward_points[army_name]["partol_index"] = 0
                                # 日常执行航行任务取消
                                self.counter[army_name] = 0
                                self.follow_enemy[army_name] = None
                                TinderPy.log_info(f"Success! 下达指令,让{army_name}前往目标点{point}")
                                self.check_task[army_name] = None # ? 这个地方把侦察目标的指令设空
                                # // self.forward_points[army_name]["patrol_ara"] =  这个地方不需要定义区域，因为主函数中会定义
                                flag = [True,] # "红方艇执行前往目标点巡逻指令成功!"
                                # self.red_records[army_name] = [0, self.entities[army_name], f"正在巡逻中或正在前往巡逻途中"]
                                self.red_records[army_name] = [2, self.entities[army_name],f"正前往{cmd['area'][0]}"] # "n号艇正前往某点巡逻中"

                            elif cmd_id == "01":
                                try:
                                    TinderPy.log_info(f'{army_name}开始执行临时指令--航行至巡逻区')
                                    TinderPy.log_info(f'{cmd["area"][0]}')
                                    # area = int(cmd["area"][0][-1]) - 1 # ? 传进来什么 ? "巡逻区1"
                                    area = int("".join([char for char in cmd["area"][0] if char.isdigit()])) - 1
                                    # TinderPy.log_info(f'area os {area}, {len(cmdlist.red_patrol_area)}, {cmdlist.red_patrol_area[1]}')
                                    # id = cmdlist.red_patrol_area[int(area)]
                                    # add 
                                    # 清空日常航行指令
                                    self.counter[army_name] = 0
                                    self.follow_enemy[army_name] = None
                                    # 前往某点巡逻断掉
                                    self.forward_points[army_name]["patrol_ara"] = None 
                                    self.forward_points[army_name]["start_partol"] = False
                                    self.forward_points[army_name]["partol_index"] = 0
                                    # 侦查敌方断掉
                                    self.check_task[army_name] = None
                                    plan = cmdlist.area_patrol(self.entities[army_name], "0103", area) # cmdlist.area_patrol(self.entities["1号艇"], "0103", 0) cmdlist.area_patrol(self.entities["1号艇"], "0103", 2)
                                    TinderPy.conduct(plan)
                                    TinderPy.log_info(f'{army_name}航行指令下达成功!')
                                    flag = [True,] # "红方艇执行前往巡逻区指令成功!"
                                    self.red_records[army_name] = [0, self.entities[army_name], f"正在区域-{area+1}巡逻中或正在前往区域-{area+1}巡逻途中"]
                                    # 更新巡逻区数量
                                    # self.partol_num[str(area)]+=1

                                except Exception as e:
                                    error = traceback.format_exc()
                                    TinderPy.log_info(f"执行航行至巡逻区的指令出现问题! {error}")

                            elif cmd_id == "03":
                                """雷达控制, 保持待机，保持雷达光电对海侦察"""
                                # todo 测试
                                TinderPy.log_info(f'{army_name}开始执行临时指令--保持雷达、光电开启{cmd_id}')
                                cmd_str = '{"switch":{"power": true, "device": 1}}'
                                TinderPy.device_control(self.entities[army_name], 4, cmd_str) # 雷达相关
                                cmd_str = '{"switch":{"power": true, "device": 1}}'
                                TinderPy.device_control(self.entities[army_name], 12, cmd_str) # 光学
                                cmd_str = '{"switch":{"power": true, "device": 1}}'
                                TinderPy.device_control(self.entities[army_name], 16, cmd_str) # 电帧
                                
                            elif cmd_id == "20":
                                """前往查证目标
                                targets: x号自杀艇
                                """
                                TinderPy.log_info(f'{army_name}开始执行临时指令--前往侦察走私艇{cmd_id}')
                                target = cmd["targets"][0] # 传进来的是一个list，因此读取第0个
                                # todo 测试，如果是跟踪的艇太多，则返回False
                                enemy_name = self.ID_NAME[str(target)] # 敌方的名字
                                if self.follow_count[enemy_name] >= 2:
                                    TinderPy.log_info(f"{army_name}不能执行查证任务, 因为已经有2艘艇在追击蓝方艇: {enemy_name}")
                                    flag = [False, f"{army_name}不能执行前往查证目标任务, 因为已经有2艘红方艇在追击蓝方艇: {enemy_name}, 建议安排其他任务!"]
                                    return flag 
                                self.check_task[army_name] = self.ID_NAME[str(target)]  # ? 现在的target应该是一个ID, 因此这个地方先建立一个ID: name的蓝方艇字典,这里是否为字符串
                                # self.check_task[army_name] = target
                                self.forward_points[army_name]["goal"] = None
                                self.forward_points[army_name]["patrol_ara"] = None 
                                self.forward_points[army_name]["start_partol"] = False
                                self.forward_points[army_name]["partol_index"] = 0
                                # 日常跟踪去掉
                                self.counter[army_name] = 0
                                self.follow_enemy[army_name] = None
                                TinderPy.log_info(f"{army_name}下达前往侦察走私艇临时指令成功!")
                                flag = [True,]
                                pass

                            elif cmd_id == "21":
                                """保持跟踪监视目标"""
                                TinderPy.log_info(f'{army_name}开始执行临时指令--前往跟踪目标{cmd_id}')
                                target = cmd["targets"][0] # 传进来的是一个list，因此读取第0个
                                # todo 测试，如果是跟踪的艇太多，则返回False
                                enemy_name = self.ID_NAME[str(target)] # 敌方的名字
                                if self.follow_count[enemy_name] >= 2:
                                    TinderPy.log_info(f"{army_name}不能执行跟踪任务, 因为已经有2艘艇在追击蓝方艇: {enemy_name}")
                                    flag = [False, f"{army_name}不能执行跟踪任务, 因为已经有2艘红方艇在跟踪蓝方艇: {enemy_name}, 建议安排其他任务!"]
                                    return flag
                                self.check_task[army_name] = self.ID_NAME[str(target)]
                                self.forward_points[army_name]["goal"] = None
                                self.forward_points[army_name]["patrol_ara"] = None 
                                self.forward_points[army_name]["start_partol"] = False
                                self.forward_points[army_name]["partol_index"] = 0
                                # 日常跟踪去掉
                                self.counter[army_name] = 0
                                self.follow_enemy[army_name] = None
                                TinderPy.log_info(f"{army_name}下达前往跟踪目标临时指令成功!")
                                flag = [True,]
                                pass
                                
                            elif cmd_id == "22":
                                # todo 临时指令攻击模块要加一个攻击特有的标识字典
                                # ! 现在的打击摧毁最大的问题是 不仅仅是一种武器攻击: 震撼弹 + 微波武器
                                targets_id = cmd["targets"][0] # 拿到ID
                                targets = self.ID_NAME[str(targets_id)] # ID转换为NAME
                                assert targets in ["1号走私艇", "2号走私艇", "3号走私艇", "4号走私艇", "5号走私艇", "6号走私艇", "7号走私艇", "8号走私艇", "9号走私艇", "10号走私艇"]
                                # if self.enemies[target] is None:
                                if self.enemy_alive[targets]<= 5:  
                                    return [False, f"蓝方 {targets} 已经死亡,不能对其执行攻击操作."] # error: 该敌方艇已经死亡，不对对其执行打击任务!
                                # todo 测试
                                # ! 震撼弹攻击
                                if cmdlist.compute_distance(self.loc[army_name], self.enemies[targets]) < 4:
                                    plan = cmdlist.dd_attack(self.entities[army_name], "DD打击", "0108", [self.enemies_id[targets]])
                                    # 弹药量-2
                                    self.shoot_interval[army_name][2] -= 2 # ? 弹药量-2, 临时指令不考虑射击间隔
                                    TinderPy.conduct(plan)
                                    TinderPy.log_info(f"{army_name} 执行临时打击指令, 发动震撼弹攻击！")
                                
                                # ! 微波攻击
                                try:
                                    relative_angle, if_can_shoot_flag = cmdlist.if_can_microwave(self.loc[army_name][0], self.loc[army_name][0], 
                                                                                self.heading[army_name][0], self.enemies[targets][0], self.enemies[targets][1]) 

                                    if cmdlist.compute_distance(self.loc[army_name], self.enemies[targets]) < 0.2 and if_can_shoot_flag:
                                        plan = cmdlist.microwave_attack(
                                                self.entities[army_name],
                                                "微波武器打击",
                                                "0108",
                                                [self.enemies_id[targets]]
                                        )
                                        TinderPy.log_info(f"{army_name} 使用微波武器对 {targets}")
                                        TinderPy.conduct(plan)
                                        TinderPy.log_info(f"{army_name} 被使用微波武器后，血量还有: {self.enemy_alive[targets]}")
                                    else:
                                        TinderPy.log_info("执行临时指令微波武器不能正常使用")
                                        return False # error: 该敌方艇已经超过了我方艇的打击范围，不能执行打击任务!
                                    
                                except Exception as e:
                                    TinderPy.log_error(f"出现问题: 临时指令不能正确使用微波武器！！")   

            return flag
        
        except Exception as e:
            error_message = traceback.format_exc()  # 获取完整的错误信息和行号
            TinderPy.log_info(f"执行临时指令总函数有问题: {error_message}")

"""
8,9,10号走私艇从西北方向切入 8到交易1, 9,10到交易2
2,3,4号走私艇从东南方向切入 2,3到交易3, 4到交易4
1,5,7,6号走私艇从西南方向切入 1,5到交易5, 7,6到交易6
"""
class BluePolicy:
    def __init__(self):
        # 定义蓝方实体的id和导弹信息
        self.entities = {
            "1号走私艇": None,
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }
        self.loc = {
            "1号走私艇": None,
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }

        self.enemies = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
        }
        self.heading = {
            "1号走私艇": None,
            "2号走私艇": None,
            "3号走私艇": None,
            "4号走私艇": None,
            "5号走私艇": None,
            "6号走私艇": None,
            "7号走私艇": None,
            "8号走私艇": None,
            "9号走私艇":  None,
            "10号走私艇": None,
        }
        # add
        self.enemies_heading = {
            "1号艇": None,
            "2号艇": None,
            "3号艇": None,
            "4号艇": None,
            "5号艇": None,
            "6号艇": None,
            "7号艇": None,
            "8号艇": None,
            "9号艇":  None,
            "10号艇": None,
            "11号艇": None,
            "12号艇": None,
        }
        self.task_1_changepath = True

        self.change_3 = True
        self.change_2 = True
        self.change_1 = True

        # 蓝方的交易点, 蓝方交易点不断选择
        self.trade_point = {
            "1号走私艇": 4,
            "2号走私艇": 6,
            "3号走私艇": 4,
            "4号走私艇": 5,
            "5号走私艇": 4,
            "6号走私艇": 3,
            "7号走私艇": 3,
            "8号走私艇": 2,
            "9号走私艇": 1,
            "10号走私艇":2,
        }
        self.trading = {
            "trade1": [121.27380169, 38.96845602],
            "trade2": [121.1672419, 38.95374014],
            "trade3": [121.08751414, 38.89781016],
            "trade4": [121.11248287, 38.83181382],
            "trade5": [121.15265619, 38.72466319],
            "trade6": [121.29071637, 38.78868264],

        }
        # 记录当前艇是否正在避让 int 代表还需要避让多少帧
        self.avoiding = {
            "1号走私艇": 0,
            "2号走私艇": 0,
            "3号走私艇": 0,
            "4号走私艇": 0,
            "5号走私艇": 0,
            "6号走私艇": 0,
            "7号走私艇": 0,
            "8号走私艇": 0,
            "9号走私艇":  0,
            "10号走私艇": 0,
        }
        self.is_alive = {
            "1号走私艇": True,
            "2号走私艇": True,
            "3号走私艇": True,
            "4号走私艇": True,
            "5号走私艇": True,
            "6号走私艇": True,
            "7号走私艇": True,
            "8号走私艇": True,
            "9号走私艇":  True,
            "10号走私艇": True,
        }

        self.free_time = {
            "1号走私艇": 23251,
            "2号走私艇": 0, # 4674,
            "3号走私艇": 8000,
            "4号走私艇": 0,  # 4674,
            "5号走私艇": 6943,
            "6号走私艇": 10525,
            "7号走私艇": 11169,
            "8号走私艇": 6943,
            "9号走私艇":  11633,
            "10号走私艇": 5845,
        }
        # 所有的蓝方艇，如果到达指定交易点，那么将不再动
        self.end_task = {
            "1号走私艇": False,
            "2号走私艇": False,
            "3号走私艇": False,
            "4号走私艇": False,
            "5号走私艇": False,
            "6号走私艇": False,
            "7号走私艇": False,
            "8号走私艇": False,
            "9号走私艇":  False,
            "10号走私艇": False,
        }

    def act(self, frame: int) -> None:
        """Make actions according to thinder.
        
        Args:
            thinder: env class
            frame: cur step
        
        return: 
            plan
        """
        try:
            pt_final = [121.12318351, 38.78727998]
            
            # 解析当前态势
            blue_all_forces = TinderPy.get_blue_forces()
            for b_item in blue_all_forces:
                self.entities[f"{b_item.get_name()}"] = b_item.get_id()
                self.is_alive[f"{b_item.get_name()}"] = b_item.get_life() # 健康状态
                self.loc[f"{b_item.get_name()}"] = [b_item.get_lon(), b_item.get_lat()]
                self.heading[f"{b_item.get_name()}"]= [b_item.get_heading()]

            red_all_forces = TinderPy.get_red_forces()
            for r_item in red_all_forces:
                if r_item.get_name() != "系留探测飞艇-1":
                    self.enemies[f"{r_item.get_name()}"] = [r_item.get_lon(), r_item.get_lat()]
                    self.enemies_heading[f"{r_item.get_name()}"] = r_item.get_heading()

            # TinderPy.log_info(f'cur frame: {frame}, 红4在蓝10的哪个角度:{cmdlist.calculate_bearing(self.enemies["4号艇"][1], self.enemies["4号艇"][0],self.loc["10号走私艇"][1], self.loc["10号走私艇"][0],self.heading["10号走私艇"][0])}, 蓝方当前朝向{self.heading["10号走私艇"]}')
            ################## 启动，冲向交易点
            if frame == 1:
                """
                9、8、10号走私艇分别从西北、正北切入，逼近自己的港口
                """
                # # plan
                plan1 = cmdlist.course_maneuver(self.entities["9号走私艇"], "蓝方9号走私艇航线机动冲向交易点1", "0100", 
                                                [
                                                    [120.71316797, 39.33009653],
                                                    [121.15897678,39.23276735],
                                                    self.trading["trade1"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                
                plan2 = cmdlist.course_maneuver(self.entities["8号走私艇"], "蓝方8号走私艇航线机动冲向交易点2", "0100", 
                                                [
                                                    [120.54916467,39.12000782+0.0072],
                                                    [120.83225963, 39.01613883+0.0072],
                                                    [121.06040788,39.05046960+0.0072],
                                                    [self.trading["trade2"][0], self.trading["trade2"][1]]
                                                ], 
                                                str(cmdlist.high_blue_speed))
                
                plan3 = cmdlist.course_maneuver(self.entities["10号走私艇"], "蓝方10号走私艇航线机动冲向交易点2", "0100", 
                                                [
                                                    [120.54916467,39.12000782],
                                                    [120.83225963, 39.01613883],
                                                    [121.06040788,39.05046960],
                                                    self.trading["trade2"]
                                                ], 
                                                str(cmdlist.high_blue_speed))
                
                # for pl in [plan3]:
                #     TinderPy.conduct(pl)

                for pl in [plan1, plan2, plan3]:
                    TinderPy.conduct(pl)

                # 4,2
                plan1 = cmdlist.course_maneuver(self.entities["4号走私艇"], "蓝方4号走私艇航线机动冲向交易点5", "0100", 
                                                [
                                                    [121.18311872,38.23428116],[121.25043164, 38.47688901],
                                                    self.trading["trade5"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                
                plan2 = cmdlist.course_maneuver(self.entities["2号走私艇"], "蓝方2号走私艇航线机动冲向交易点6", "0100", 
                                                [
                                                    [121.18311872,38.23428116],[121.3954315, 38.49816720],
                                                    self.trading["trade6"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                for pl in [plan1, plan2]:
                    TinderPy.conduct(pl)

            if frame == 200:

                # 6,7 
                plan1 = cmdlist.course_maneuver(self.entities["6号走私艇"], "蓝方6号走私艇航线机动冲向交易点3", "0100", 
                                                [
                                                    [120.27912509, 38.85676886],
                                                    [120.66721550, 38.91624206],
                                                    self.trading["trade3"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                plan2 = cmdlist.course_maneuver(self.entities["7号走私艇"], "蓝方7号走私艇航线机动冲向交易点3", "0100", 
                                                [
                                                    [120.27912509, 38.85676886+0.0072],
                                                    [120.66721550, 38.91624206+0.0072],
                                                    self.trading["trade3"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                for pl in [plan1, plan2]:
                    TinderPy.conduct(pl)

                # 1,3,5 
                plan1 = cmdlist.course_maneuver(self.entities["1号走私艇"], "蓝方1号走私艇航线机动冲向交易点4", "0100", 
                                                [
                                                    [120.45134016, 38.58141372],
                                                    [120.94372986, 38.72632033],
                                                    self.trading["trade4"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                plan2 = cmdlist.course_maneuver(self.entities["3号走私艇"], "蓝方3号走私艇航线机动冲向交易点4", "0100", 
                                                [
                                                    [120.45134016, 38.58141372+0.0072],
                                                    [120.94372986, 38.72632033+0.0072],
                                                    self.trading["trade4"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                plan3 = cmdlist.course_maneuver(self.entities["5号走私艇"], "蓝方5号走私艇航线机动冲向交易点4", "0100", 
                                                [
                                                    [120.45134016, 38.58141372-0.0072],
                                                    [120.94372986, 38.72632033-0.0072],
                                                    self.trading["trade4"],

                                                ], 
                                                str(cmdlist.high_blue_speed))
                for pl in [plan1, plan2, plan3]:
                    TinderPy.conduct(pl)
                
                

            ############### 判断是否到达指定点 
            for enti_name, location in self.loc.items():
                if cmdlist.compute_distance(location, self.trading["trade"+str(self.trade_point[enti_name])]) < 0.2:
                    self.end_task[enti_name] = True
                    TinderPy.log_info(f"蓝方艇: {enti_name} 已经到达交易点 {'trade'+str(self.trade_point[enti_name])}, 结束任务!")
            
            
            ################# 灵活机动，产生避让动作，且执行避让动作完之后，会挑选合适的交易点（最近），重新分配航向
            # 0. 检查到红方艇，开始激活避让，制定避让状态
            ## 检查每个蓝方艇的探测范围内有多少红方艇
            try:
                for en_name, is_alive in self.is_alive.items():
                    # TinderPy.log_info(f"当前蓝方艇是：{en_name}")
                    # if en_name == "10号走私艇": # ! 去掉 
                    if is_alive > 1 and not self.end_task[en_name]: #存活并且没有结束任务
                        if frame > self.free_time[en_name]: # * 这个地方是为了让各个艇到达探测圈边缘再采取行动
                            # TinderPy.log_info(f"{en_name}艇还存活")
                            # 证明这个艇还存活着
                            # 满足条件：1. 该艇没有在避让；2. 该艇的探测范围内有红方
                            # 该艇没有在避让
                            if self.avoiding[en_name] == 0: 
                                # TinderPy.log_info(f"{en_name}艇目前没有避让任务!")
                                # 找该艇10km范围内
                                red_enems = [] # 该蓝方艇10km范围内有无红方
                                for red_enemy, red_loc in self.enemies.items():
                                    if cmdlist.compute_distance(self.loc[en_name], red_loc) < 10:
                                        red_enems.append(red_enemy)
                                
                                if len(red_enems) == 0:
                                    if frame % 109 == 0:
                                        # todo 这个地方应该也加入一个避让的机制，避开岛屿
                                        plan = cmdlist.course_maneuver(self.entities[en_name], f"(循环指令1)蓝方{en_name}航线机动冲向交易点{self.trade_point[en_name]}", "0100", 
                                                            [
                                                                self.trading["trade"+str(self.trade_point[en_name])],
                                                            ], 
                                                            str(cmdlist.high_blue_speed))
                                        TinderPy.conduct(plan)
                                        TinderPy.log_info(f"{en_name}艇探测范围内没有探测到红方艇, 重复执行冲向交易点的航行指令.-1 frame: {frame}")
                                    pass

                                elif len(red_enems) > 0:
                                    if frame % 30 == 0:
                                        # 说明它探测范围内有红艇
                                        # 只看对自己威胁最大的那个红方给艇
                                        dangerous_red = None
                                        dangerous_distance = 99999999
                                        for red in red_enems:
                                            dis = cmdlist.compute_distance(self.loc[en_name], self.enemies[red])
                                            if dis < dangerous_distance and red != "震撼弹":
                                                dangerous_distance = dis 
                                                dangerous_red = red
                                        
                                        recent_entity = None
                                        recent_enetity_heading = None
                                        recent_dis = 9999999999

                                        # todo 找到最近的队友,并拿取到角度
                                        for bl, bl_loc in self.loc.items():
                                            if bl != en_name:
                                                if cmdlist.compute_distance(self.loc[bl], self.loc[en_name]) < recent_dis:
                                                    recent_dis = cmdlist.compute_distance(self.loc[bl], self.loc[en_name])
                                                    recent_entity = bl
                                                    recent_enetity_heading = self.heading[recent_entity]
                                        TinderPy.log_info(f"距离我：{en_name}最近的队友是:{recent_entity}, 它的朝向是: {recent_enetity_heading}")
                                        
                                        # 找到这个红方艇在当前艇的方位
                                        TinderPy.log_info(f"check: {self.enemies[dangerous_red][1]}")
                                        TinderPy.log_info(f"check: {self.enemies[dangerous_red][0]}")
                                        TinderPy.log_info(f"check: {self.loc[en_name][1]}")
                                        TinderPy.log_info(f"check: {self.loc[en_name][0]}")
                                        TinderPy.log_info(f"check: {self.heading[en_name][0]}")
                                        en_angle = cmdlist.calculate_bearing(self.enemies[dangerous_red][1], 
                                                                             self.enemies[dangerous_red][0], 
                                                                             self.loc[en_name][1], 
                                                                             self.loc[en_name][0], 
                                                                             self.heading[en_name][0]
                                        )
                                        TinderPy.log_info(f"{en_name}探测到了红艇,并找到了最威胁的艇:{dangerous_red},距离是:{dangerous_distance}, 在 {en_name} 哪个角度: {en_angle}")
                                        # todo 避让原则增加, 加判断 1）跟队友避让不同的角度；2）蓝方到达最近交易点的时间要比红方来追它还要快的话，就没有必要躲避了;
                                        escape_angle = cmdlist.calculate_escape_angle(en_angle, self.loc[en_name][1], self.loc[en_name][0], 13, self.heading[en_name][0], self.enemies[dangerous_red][1], self.enemies[dangerous_red][0], self.enemies_heading[dangerous_red], recent_enetity_heading) # ? 后边的参数是判断当前角度是否合理的
                                        
                                        if escape_angle is not None:
                                            # recent_red = None
                                            # recent_dis = 999999999
                                            # for red_item, red_loc in self.enemies.items():
                                            #     if cmdlist.compute_distance(self.loc[en_name], self.enemies[red_item]) < recent_dis:
                                            #         recent_dis = cmdlist.compute_distance(self.loc[en_name], self.enemies[red_item])
                                            #         recent_red = red_item # 选距离最近的红方
                                            TinderPy.log_info(f"蓝方 {en_name} 探测到了红方, 是否需要躲避, 进行时间危险评估!")
                                            # ? 当escape_angle != None时， 危险评估: 蓝方到达最近交易点的所需要的时间 < 红方到达这个蓝方艇的时间
                                            blue_achieve = cmdlist.compute_distance(self.loc[en_name], self.trading["trade"+str(self.trade_point[en_name])]) * 1000 / cmdlist.high_blue_speed
                                            red_achieve =  cmdlist.compute_distance(self.loc[en_name], self.enemies[dangerous_red]) * 1000 / cmdlist.high_red_speed
                                            if red_achieve > blue_achieve:
                                                TinderPy.log_info(f"虽然红方有危险,但是尽快驶向最近交易点即可, 不必进行躲让!")
                                                escape_angle = None                                    

                                        # escape_angle = None # ! 最后删掉
                                        TinderPy.log_info(f"蓝方艇执行避让,选择角度: {escape_angle}")
                                        if escape_angle is None:
                                            TinderPy.log_info(f"红方艇在蓝方艇后面...")
                                            pass # 在后方，没有必要逃逸
                                        else:
                                            # 在前方，逃逸
                                            new_lon, new_lat = cmdlist.calculate_new_coordinates(self.loc[en_name][1], self.loc[en_name][0], escape_angle, 13, self.heading[en_name][0])
                                            # todo 测试 - 这个地方要加一个禁避区，有四个点的岛屿，当判断这个方向的点是再这个区域内，那么就选择别的角度,重新生成一个角度
                                            TinderPy.log_info(f"蓝方{en_name}探测到红方艇{dangerous_red},开始避让,逃逸角度是:{escape_angle}, 逃逸点是: {new_lon}, {new_lat}")
                                            plan = cmdlist.course_maneuver(self.entities[en_name], f"蓝方{en_name}正在执行避让", "0100", 
                                                                    [[new_lon, new_lat]],
                                                                    str(cmdlist.high_blue_speed))
                                            TinderPy.conduct(plan)
                                            self.avoiding[en_name] = 2500
                                            pass
            except Exception as e:
                error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
                TinderPy.log_error(f"检查蓝方艇是否探测到红方时出现问题: {error_message}")

            try:
                # 1. 挨个检索走私艇的状态，查看它们是否在避让
                for en_name, if_avoid in self.avoiding.items():
                    # if en_name == "10号走私艇": # ! 去掉 
                    # TinderPy.log_info(f"检查是否在避让!, 存活状态: {self.is_alive[en_name]}, 是否结束任务? {self.end_task[en_name]}")
                    # if en_name is alive
                    # TinderPy.log_info(f"当前循环检查到: {en_name}, 存活状态: {self.is_alive[en_name]}")
                    if self.is_alive[en_name] > 1 and not self.end_task[en_name]:
                        # TinderPy.log_info(f"{en_name} 还存活并且，还没有抵达终点--2")
                        if frame > self.free_time[en_name]:
                            # TinderPy.log_info(f"当前循环检查到: {en_name}, 查看避让并且分配相应的任务: {if_avoid}")
                            if if_avoid == 0:
                                # TinderPy.log_info(f"{en_name} 还存活并且没有在避让...")
                                if frame % 65 == 0:
                                        plan = cmdlist.course_maneuver(self.entities[en_name], f"(循环指令2)蓝方{en_name}航线机动冲向交易点{self.trade_point[en_name]}", "0100", 
                                                            [
                                                                self.trading["trade"+str(self.trade_point[en_name])],
                                                            ], 
                                                            str(cmdlist.high_blue_speed))
                                        TinderPy.conduct(plan)
                                        TinderPy.log_info(f"{en_name}艇探测范围内没有探测到红方艇, 重复执行冲向交易点 {self.trade_point[en_name]} 的航行指令.-2 frame: {frame}")
                                pass
                            
                            elif if_avoid == 1:
                                # 说明避让到了最后一帧，那么当前应该是再重新选择一条路径，到达最近的交易点
                                min_dis_trade = 99999 # 当前实体距离交易点的距离
                                best_trade = None
                                for t_name, t_loc in self.trading.items():
                                    cur_dis = cmdlist.compute_distance(self.loc[en_name], t_loc)
                                    if cur_dis < min_dis_trade:
                                        min_dis_trade = cur_dis
                                        best_trade = t_name

                                # 避让状态设成0
                                self.avoiding[en_name] = 0
                                TinderPy.log_info(f"蓝方艇{en_name}避让结束 frame: {frame}, 重新选择交易点 {best_trade}")
                                self.trade_point[en_name] = int(best_trade[5]) # ! best_trade这里是trade3, 但是self.trade_point的value是int
                                # 重新下达冲向交易点的命令
                                plan = cmdlist.course_maneuver(self.entities[en_name], f"蓝方{en_name}航线机动冲向交易点{best_trade}", "0100", 
                                                            [
                                                                self.trading[best_trade],
                                                            ], 
                                                            str(cmdlist.high_blue_speed))
                                TinderPy.conduct(plan)

                            elif if_avoid > 1:
                                # 蓝方还在避让中，不能干扰
                                self.avoiding[en_name]-=1
                                # TinderPy.log_info(self.avoiding)
                                # TinderPy.log_info(f"蓝方艇{en_name}正在避让中...{frame}, 剩余避让: {self.avoiding[en_name]}")
                                # ! 检查避让的时候是否会到达交易点, 如果到达交易点, 那就不用再继续避让了,且已经结束任务
                                if cmdlist.compute_distance(self.loc[en_name], self.trading["trade"+str(self.trade_point[enti_name])]) < 0.5:
                                    # 
                                    self.end_task[en_name] = True

            except Exception as e:
                TinderPy.log_info(f"检查是否在避让!, 存活状态: {self.is_alive[en_name]}, 是否结束任务? {self.end_task[en_name]}")
                TinderPy.log_error(f"检查蓝方艇是否在避让状态时出现问题: {e}")
        
        except Exception as e:
            error_message = traceback.format_exc()  # 获取完整的错误信息和行号
            TinderPy.log_info(f"蓝方执行act: {error_message}")