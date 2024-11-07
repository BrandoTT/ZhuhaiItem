import random
import os
import sys

sys.path.append(os.path.join("./"))

import TinderPy

from define import *
from device_control_json import *

from py.policy_central import RedPolicy
# from py.policy_central_copy2 import RedPolicy
# from py.policy_central_before import RedPolicy
redpolicy = RedPolicy()

import redis
r = redis.Redis(host='192.168.3.170', port=6379, password='juntai', db=5)
import requests

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
    # print(f'Step: {time//step}, red')
    global patrol_flag
    global move2point_flag
    global tail_flag
    global strike_flag
    # print(f'Time: {time}, Step: {step}')
    order = r.lpop("situation:ai-order") # 临时指令
    if order != None:
        TinderPy.log_info(f'Recived AI-ORDER {order}' )
    redpolicy.act(time//step, order)
    # result = "http://192.168.3.170:5555/free/tinder/v3/ai/message/receive/123456?message=" + "Success"
    # response = requests.get(result)

def __finished__():
    print("__finished__")
