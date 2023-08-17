# 在 interfaces.py 中
from abc import ABC, abstractmethod
import os

class DataPreparationTool(ABC):
    def __init__(self):
        self.current_dir = os.getwd()
        self.cmd_list = []
        self.is_success = False

    @abstractmethod
    def process(self, input_data):
        pass

    def run_cmd_list(self, arr: List[str]) -> Union[bool, None]:
        isSuccess = False
        for cmd in arr:
            proc = subprocess.run(cmd, shell=True)
            if proc.returncode != 0:
                isSuccess = False
                print("命令执行失败。")
                break
            else:
                isSuccess = True
                print("命令执行成功。")
        return isSuccess

class DataFilterTool(ABC):
    @abstractmethod
    def filter(self, data, filter_criteria):
        pass

# 定义其他接口和抽象类...
