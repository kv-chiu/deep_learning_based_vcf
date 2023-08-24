import gzip

from . import List, Optional, subprocess, Union, os
from .interfaces import DataPreparationTool
from .config import ENV_PATH

class VcfMergeTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_file_list: List[str]) -> Optional[str]:
        '''
        :param vcf_file_list: vcf文件列表
        :return: merged.vcf文件
        '''
        
        if len(vcf_file_list) < 2:
            return None
        bcftools = ENV_PATH.get('bcftools')
        cmd = [bcftools, 'merge']
        cmd += vcf_file_list
        output_file = self.current_dir + '/merged.vcf'
        cmd += ['-o', output_file]
        cmd = ' '.join(cmd)
        self.cmd_list.append(cmd)
        self.is_success = self.run_cmd_list(self.cmd_list)
        if self.is_success:
            return output_file
        else:
            return None
        
class VcfAnnoTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_file: str) -> Optional[str]:
        '''
        :param vcf_file: vcf文件
        :return: annotated_vcf_file.vcf文件
        '''
        
        bcftools = ENV_PATH.get('bcftools')
        cmd = [bcftools, 'annotate', '--set-id', '+\'%CHROM:%POS\'']
        output_file = self.current_dir + '/annotated.vcf'
        cmd += [vcf_file]
        cmd += ['-o', output_file]
        cmd = ' '.join(cmd)
        self.cmd_list.append(cmd)
        self.is_success = self.run_cmd_list(self.cmd_list)
        if self.is_success:
            return output_file
        else:
            return None
        
class VcfGetSamplesNameTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_file: str) -> Union[Optional[List[str]], str]:
        '''
        :param vcf_file: vcf文件
        :return: 样本名列表, 输出文件
        '''
        
        bcftools = ENV_PATH.get('bcftools')
        cmd = [bcftools, 'query', '-l']
        cmd += [vcf_file]
        output_file = self.current_dir + '/samples_name.txt'
        cmd += ['>', output_file]
        cmd = ' '.join(cmd)
        self.cmd_list.append(cmd)
        self.is_success = self.run_cmd_list(self.cmd_list)
        if self.is_success:
            with open(output_file, 'r') as f:
                samples_name = f.read().strip().split('\n')
            return samples_name, output_file
        else:
            return None

class VcfSplitMergedTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_merged_file: str, samples_name_file: str) -> Union[Optional[List[str]], str]:
        '''
        :param vcf_merged_file: merged.vcf文件
        :param samples_name_file: 样本名文件
        :return: vcf文件列表, 输出文件夹
        '''
        
        output_dir = self.current_dir + '/split_merged_vcf'
        bcftools = ENV_PATH.get('bcftools')
        cmd = [bcftools, '+split', '-S', samples_name_file]
        cmd += ['-Oz', '-o', 'split_merged_vcf']
        cmd += [vcf_merged_file]
        print(cmd)
        cmd = ' '.join(cmd)
        self.cmd_list.append(cmd)
        self.is_success = self.run_cmd_list(self.cmd_list)
        if self.is_success:
            vcf_files_list = []
            for file in os.listdir(output_dir):
                if file.endswith('.vcf.gz'):
                    vcf_files_list.append(output_dir + '/' + file)
            return vcf_files_list, output_dir
        else:
            return None
