import random
import os
import sys

import TinderPy

sys.path.append(os.path.join("./"))
from define import *
from device_control_json import *

from py.policy import RedPolicy, BLUE_ENTITY_NAME
redpolicy = RedPolicy()

def __prepared__():
    print("py __prepared__")

# BLUE_ENTITY_NAME = {
#     "2101123173": "1号自杀艇",
#     "426526038": "2号自杀艇",
#     "1752914734": "3号自杀艇",
#     "1286139094": "4号自杀艇",
#     "2088622868": "5号自杀艇",
#     "1444687572": "6号自杀艇",
#     "1501816854": "7号自杀艇",
#     "917419785": "8号自杀艇",
#     "450644145": "9号自杀艇",
#     "1603660208": "10号自杀艇"
# }


class DeviceControl:
    def __init__(self):
        self.force_id = None
        self.device_control_cmd = None
        self.device_control_json = None
        self.cur_lla = None
        self.matchIndex = None

    def set_force_id(self, force_id):
        self.force_id = force_id

    def set_device_control_cmd(self, dc_cmd: DeviceControlEnum):
        self.device_control_cmd = dc_cmd

    def set_device_control_json(self, dc_js):
        self.device_control_json = dc_js

    def generate_device_control_json(self, dc):
        raise NotImplementedError

    def init(self, dc_dict):
        self.set_force_id(dc_dict["force_id"])
        self.set_device_control_cmd(dc_dict["device_control_cmd"])
        self.set_device_control_json(dc_dict["device_control_json"])

    def device_control(self, ifshow=False):
        if ifshow:
            self.show()
        TinderPy.device_control(self.force_id, self.device_control_cmd.value, self.device_control_json)

    def show(self):
        print("===========================================")
        print("force id :", self.force_id)
        print("device control cmd:", self.device_control_cmd.name, self.device_control_cmd.value)
        print("device control info:", json.loads(self.device_control_json))
        print("===========================================")


class StrikeControl(DeviceControl):
    def __init__(self):
        super(StrikeControl, self).__init__()


class TaskExecutor:
    def __init__(self, Task):
        self.task = Task
        self.cur_task = None

    def new_task(self, dc_dict):
        self.cur_task = self.task()
        self.cur_task.init(dc_dict)
        return self.cur_task

    def exec(self, ifshow=False):
        self.cur_task.device_control(ifshow)


patrol_flag = True
move2point_flag = True
tail_flag = True
strike_flag = True


def __next_step__(time, step):
    # print(f'Step: {time//step}, red')
    global patrol_flag
    global move2point_flag
    global tail_flag
    global strike_flag
    # 获取红方兵力态势
    # print(f'======= Red Forces ======')
    # red_all_forces = TinderPy.get_red_forces()
    # for r_item in red_all_forces:
    #     print(f'当前实体ID: {r_item.get_id()}, 当前实体的名称: {r_item.get_name()}, 阵营信息: {r_item.get_team()}')
    #     print(f'{r_item.get_name()} 具有哪些装备: {r_item.get_equipment_id()}')
    #     print(f'当前实体的位置 经度：{r_item.get_lon()}, 纬度：{r_item.get_lat()}, 高度：{r_item.get_alt ()}')

    #  根据蓝方的集中策略做出应对
    ## 1，4，5号艇作为第1编组
        

    ## 2，3，6号艇作为第2编组
        

    # 获取场景中探测列表
    # if time > 10 * 60 * 1000:
    redpolicy.act(time//step)
    # print(f"===Step: {time//step} ====== Red Detected ==========")
    # 以200ms为步长，大约58帧的时候，会探测到蓝方
    # detects_red = TinderPy.get_red_detected_situation()
    # # 说明红方探测到了消息
    # if len(detects_red) > 0:
    #     for n, detect in enumerate(detects_red):
    #         print(f'探测到{BLUE_ENTITY_NAME[str(detect.id)]} 号蓝方无人艇: id: {detect.id}, lon: {detect.lon}, lat: {detect.lat}')
    #     print(f'一共有: {len(detects_red)}条蓝方被探测到.') 
        


def __finished__():
    print("__finished__")
