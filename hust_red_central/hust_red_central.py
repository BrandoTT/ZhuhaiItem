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
# SEND_URL = "http://192.168.3.170:3002/receive"

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
    import traceback
    try:
        global patrol_flag
        global move2point_flag
        global tail_flag
        global strike_flag
        # print(f'Time: {time}, Step: {step}')
        order = r.lpop("situation:ai-order") # 临时指令
        if order != None:
            TinderPy.log_info(f'Recived AI-ORDER {order}' )
        result = redpolicy.act(time//step, order) # * result: list = [flag, dict]
        # if result[0] != "none": 
        if result["flag"] != "none": 
            decoded_string = order.decode('utf-8')
            # 转换为字典
            data_dict = json.loads(decoded_string)
            simid = TinderPy.get_sim_id() ## 
            # TinderPy.log_info(type())
            time = data_dict['time']
            success = result["flag"][0]
            if not success:
                info = result["flag"][1]
                RETURN_DATA = f"http://192.168.3.170:5555"+ f"/free/tinder/v3/ai/conduct/finish/{simid}?time={time}&success={success}&info={info}" # time
                response = requests.get(RETURN_DATA)
                TinderPy.log_info(f"执行内容: {RETURN_DATA}")
            else:
                RETURN_DATA = f"http://192.168.3.170:5555"+ f"/free/tinder/v3/ai/conduct/finish/{simid}?time={time}&success={success}&info={None}" # time
                response = requests.get(RETURN_DATA)
                TinderPy.log_info(f"执行内容: {RETURN_DATA}")
            
            TinderPy.log_info(f"语音指令反馈结果成功! 执行结果")

        simid = TinderPy.get_sim_id() ## 

        # if len(result) >= 2:
        if result["red_records"] is not None:
            # 说明有新的任务刷新
            task_records = result["red_records"] # result[1] # dict = {"1号艇": [0, "正在巡逻中"]}
            # if time//step > 5:
            for red_item, task in task_records.items():
                if task is not None:
                    task_index = task[0]
                    force_id = task[1]
                    task_description = task[2]
                    RETURN_TASK = f"http://192.168.3.170:5555/free/tinder/v3/ai/forces-info/receive/{simid}?forcesId={force_id}&message={task_description}"
                    response = requests.get(RETURN_TASK)
                    TinderPy.log_info(f"成功返回红方 {red_item} 的任务执行信息! {RETURN_TASK}")

        if result["blue_records"] is not None:
            task_records = result["blue_records"]
            for blue_item, task in task_records.items():
                # if task is not None: # is a list
                if len(task) > 1 and task[0] is not None and not isinstance(task[0], int):
                    force_id = task[-1]
                    message = f"正在被{'、'.join(task[:-1])}跟踪"
                    RETURN_TASK = f"http://192.168.3.170:5555/free/tinder/v3/ai/forces-info/receive/{simid}?forcesId={force_id}&message={message}"
                    response = requests.get(RETURN_TASK)
                    TinderPy.log_info(f"成功返回蓝方 {blue_item} 被跟踪信息: {RETURN_TASK} -- frame: {time//step}")
                
                elif len(task) > 1 and task[0] is not None and isinstance(task[0], int):
                    # 该判断返回蓝方死亡或者
                    force_id = task[-1]
                    message = "" if task[0] == 0 else ""
                    RETURN_TASK = f"http://192.168.3.170:5555/free/tinder/v3/ai/forces-info/receive/{simid}?forcesId={force_id}&message={message}"
                    response = requests.get(RETURN_TASK)
                    TinderPy.log_info(f"成功返回蓝方 {blue_item} 状态信息: {RETURN_TASK} -- frame: {time//step}")

                elif len(task) == 1:
                    # 说明只有force_id
                    force_id == task[0]
                    message = ""
                    RETURN_TASK = f"http://192.168.3.170:5555/free/tinder/v3/ai/forces-info/receive/{simid}?forcesId={force_id}&message={message}"
                    response = requests.get(RETURN_TASK)
                    TinderPy.log_info(f"成功返回蓝方 {blue_item} 被跟踪信息(存活,但是无红方艇跟踪): {RETURN_TASK} -- frame: {time//step}")



        # if task_mess is not None:
        #     """发送某些任务有变动的"""
        #     pass

    except Exception as e:
        error = traceback.format_exc()
        TinderPy.log_info(f"出现问题 {error}")

def __finished__():
    print("__finished__")
