from collections import defaultdict

from . import Optional, List
from .interfaces import DataPreparationTool

class VcfEncodingTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def extract_sequence(data: str) -> Optional[str]:
        '''
        :param data: 输入的字符串
        :return: 提取的序列
        '''

        parts = data.split(",")  # 使用逗号进行分割
        for part in parts:
            sub_parts = part.split(":")  # 使用冒号进行分割
            for sub_part in sub_parts:
                if "|" in sub_part or "/" in sub_part:  # 找到包含 "|" 或 "/" 的部分
                    return sub_part
        return None
    
    def one_hot_encode(input_str: str) -> List[int]:
        '''
        :param input_str: 输入的字符串
        :return: one-hot编码结果
        '''

        encoding_dict = defaultdict(lambda: [0, 0, 0, 1])
        encoding_dict.update({
            '0/0': [1, 0, 0, 0],
            '0/1': [0, 1, 0, 0],
            '0/1/0': [0, 0, 1, 0]
        })

        if '|' in input_str:
            input_str = input_str.replace('|', '/')  # 统一将 '|' 替换为 '/'
        
        return encoding_dict[input_str]

    def single_process(self, vcf_file: str) -> Optional[str]:
        '''
        :param vcf_file: vcf文件
        :return: vcf编码结果（单行序列）
        '''

        sample_name = 
        res = ''
        with open(vcf_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            else:
                temp_res = line.split()[9]
                temp_res = self.extract_sequence(temp_res)
                temp_res = self.one_hot_encode(temp_res)
                res += ""
