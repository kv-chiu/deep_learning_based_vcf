from . import ABC, abstractmethod, List, Optional, subprocess, os, Tuple

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

    def run_cmd_list(self, arr: List[str]) -> Optional[bool]:
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
    
    def get_run_cmd_list_res(self, arr: List[str]) -> Optional[List[Tuple[int, str, str]]]:
        '''
        :param arr: 命令列表
        :return: [(returncode, stdout, stderr), ...]
        '''
        
        res = []
        for i, cmd in enumerate(arr):
            if i == 0:
                self.start_cmd(cmd)
            proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            res.append((proc.returncode, proc.stdout.decode('utf-8'), proc.stderr.decode('utf-8')))
            if proc.returncode != 0:
                self.end_cmd(cmd, False)
                return res
            self.end_cmd(cmd, True)
        return res
    
    def get_file_dir(self, file_path: str) -> str:
        return os.path.dirname(file_path)
    
    def get_file_name(self, file_path: str) -> str:
        return file_path.split("/")[-1]
    
    def get_output_dir(self, dir_name: str) -> str:
        return self.current_dir + '/' + dir_name
    
    def compress_with_bgzip(self, input_file):
        output_file = f"{input_file}.gz"
        cmd = f"bgzip -c {input_file} > {output_file}"
        subprocess.run(cmd, shell=True)
        return output_file

def get_content_from_gz_file(gz_file_path: str) -> str:
    cmd = f'gzip -dc {gz_file_path}'
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    if proc.returncode == 0:
        return proc.stdout.decode('utf-8')
    else:
        return ''

# todo: 设计其他接口和抽象类

# class DataFilterTool(ABC):
#     @abstractmethod
#     def filter(self, data, filter_criteria):
#         pass

# class DataMatchTool(ABC):
#     @abstractmethod
#     def match(self, data, match_criteria):
#         pass
