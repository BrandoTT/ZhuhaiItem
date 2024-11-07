import random
import os
import sys

sys.path.append(os.path.join("./"))

import TinderPy

from define import *
from device_control_json import *
from py.policy_central import BluePolicy
# from py.policy_central_copy2 import BluePolicy
bluepolicy = BluePolicy()


print(sys.path)

def __prepared__():
    print("py __prepared__")


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
    # print(f'Step: {time//step}, blue')
    # TinderPy.log_info(f'Step: {time//step}, blue')
    global patrol_flag
    global move2point_flag
    global tail_flag
    global strike_flag
    # 获取蓝方兵力态势
    # print(f'***************** Blue Forces *****************')
    # blue_all_forces = TinderPy.get_blue_forces()
    # for b_item in blue_all_forces:
    #     print(f'当前实体ID: {b_item.get_id()}, 当前实体的名称: {b_item.get_name()}, 阵营信息: {b_item.get_team()}')
    #     print(f'{b_item.get_name()} 具有哪些装备: {b_item.get_equipment_id()}')
    #     print(f'当前实体的位置 经度：{b_item.get_lon()}, 纬度：{b_item.get_lat()}, 高度：{b_item.get_alt ()}')
    # print("**************************************************************")

    # 1，2，3 号自杀艇前进机动
    bluepolicy.act(time//step)
    # 4，5，6 号自杀艇前进机动
    # 获取场景中探测列表
    # if time > 10 *60 * 1000:
    #     print("========= blue Detected ==========")
    #     detects_blue = TinderPy.get_red_detected_situation()
    #     if len(detects_blue) > 0 and patrol_flag:
    #         for detect in detects_blue:
    #             print(detect)
    #         patrol_flag = False
    #         print(len(detects_blue))



def __finished__():
    print("__finished__")
