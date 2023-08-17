# 在 interfaces.py 中
from abc import ABC, abstractmethod
from typing import List, Union
import subprocess
import os

class DataPreparationTool(ABC):
    def __init__(self):
        self.current_dir = os.getcwd()
        self.cmd_list = []
        self.is_success = False

    @abstractmethod
    def process(self, input_data):
        pass

    def start_cmd(self, cmd: str) -> None:
        print('-' * 50)
        print(f'执行命令：{cmd}')
        print('-' * 50)

    def end_cmd(self, cmd: str, if_success: bool) -> None:
        print('-' * 50)
        print(f'命令执行完毕：{cmd}')
        if if_success:
            print('命令执行成功。')
        else:
            print('命令执行失败。')
        print('-' * 50)

    def run_cmd_list(self, arr: List[str]) -> Union[bool, None]:
        isSuccess = False
        for cmd in arr:
            self.start_cmd(cmd)
            proc = subprocess.run(cmd, shell=True)
            if proc.returncode != 0:
                isSuccess = False
                self.end_cmd(cmd, isSuccess)
                break
            else:
                isSuccess = True
                self.end_cmd(cmd, isSuccess)
        return isSuccess

class DataFilterTool(ABC):
    @abstractmethod
    def filter(self, data, filter_criteria):
        pass

class DataMatchTool(ABC):
    @abstractmethod
    def match(self, data, match_criteria):
        pass

# 定义其他接口和抽象类...
