from collections import defaultdict

from . import Optional, List, os
from .interfaces import DataPreparationTool

class VcfEncodingTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def extract_sequence(self, data: str) -> Optional[str]:
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
    
    def one_hot_encode(self, input_str: str) -> List[int]:
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

        sample_name = os.path.basename(vcf_file).split('.')[0]
        res = sample_name  # 第一列设置为样本名
        with open(vcf_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            else:
                temp_res = line.split()[9]
                temp_res = self.extract_sequence(temp_res)
                temp_res = self.one_hot_encode(temp_res)
                res += "," + ",".join(map(str, temp_res))  # 添加编码结果，逗号分隔

        return res
    
    def process(self, vcf_files_dir: str) -> Optional[str]:
        '''
        :param vcf_files_dir: 存放 VCF 文件的目录
        :return: 处理结果
        '''
        results = []  # 存放每个文件的处理结果
        for filename in os.listdir(vcf_files_dir):
            vcf_file_path = os.path.join(vcf_files_dir, filename)
            result = self.single_process(vcf_file_path)
            results.append(result)
        
        # 在这里将结果合并，你可以根据需要进行处理
        combined_result = "\n".join(results)

        # 存为文件
        output_file = os.path.join(self.current_dir, "vcf_encoding_result.txt")
        with open(output_file, 'w') as f:
            f.write(combined_result)

        return output_file
