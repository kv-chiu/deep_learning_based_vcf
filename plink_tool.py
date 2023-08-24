from collections import defaultdict
import gzip

from . import Optional, List, Union, os
from .interfaces import DataPreparationTool
from .config import ENV_PATH

class PlinkAssocTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_file: str, phe_file: str,
                is_make_bed: str = 'y', is_allow_no_sex: str = 'y',
                is_allow_extra_chr: str = 'y') -> Optional[str]:
        '''
        :param vcf_file: vcf文件
        :param phe_file: phe文件
        :return: plink.assoc文件
        '''

        # todo: 检查phe文件是否符合要求
        
        plink = ENV_PATH.get('plink')
        cmd = [plink, '--vcf', vcf_file, '--pheno', phe_file, '--assoc']
        if is_make_bed == 'y':
            cmd.append('--make-bed')
        if is_allow_no_sex == 'y':
            cmd.append('--allow-no-sex')
        if is_allow_extra_chr == 'y':
            cmd.append('--allow-extra-chr')

        cmd = ' '.join(cmd)
        self.cmd_list.append(cmd)
        self.is_success = self.run_cmd_list(self.cmd_list)
        if self.is_success:
            output_file = self.current_dir + '/plink.assoc'
            return output_file
        else:
            return None

class PlinkFilterTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, assoc_file: str, thresholds: float) -> Optional[str]:
        '''
        :param assoc_file: plink.assoc文件
        :param thresholds: 阈值
        :return: plink.assoc.filter文件
        '''
        
        with open(assoc_file, 'r') as f:
            lines = f.readlines()
        output_file = self.current_dir + '/plink.assoc.filter'
        with open(output_file, 'w') as f:
            for line in lines:
                if line.split()[0] == 'CHR':
                    f.write(line)
                else:
                    if line.split()[8] == 'NA':
                        continue
                    p_value = float(line.split()[8])
                    if p_value < thresholds:
                        f.write(line)
        return output_file

class PlinkMatchTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def get_match_snp_list(self, filter_assoc_file: str) -> List[str]:
        '''
        :param filter_assoc_file: plink.assoc.filter文件
        :return: SNP列表
        '''

        # step1: 读取filter_assoc_file，获取SNP列表
        snp_list = []
        with open(filter_assoc_file, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.split()[0] == 'CHR':
                continue
            else:
                snp_list.append(line.split()[1])
        return snp_list

    def get_match_vcf_file(self, filter_snp_list: List[str], vcf_file: str) -> Optional[str]:
        '''
        :param filter_snp_list: SNP列表
        :param vcf_file: vcf文件
        :return: ~plink.assoc.match文件
        '''

        # step2: 基于snp_list创建哈希表，key为snp，value默认为""
        snp_dict = defaultdict(str)
        if vcf_file.endswith('.gz'):
            with gzip.open(vcf_file, 'rb') as f:
                lines = f.readlines()
        else:
            with open(vcf_file, 'r') as f:
                lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            else:
                snp = line.split()[2]
                if snp in filter_snp_list:
                    snp_dict[snp] = line

        # step3: 读取snp_dict，将value写入新文件
        vcf_file_name = self.get_file_name(vcf_file)
        output_dir = self.current_dir + '/match'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        output_file = output_dir + '/' + vcf_file_name + '.match'
        with open(output_file, 'w') as f:
            for snp in filter_snp_list:
                f.write(snp_dict[snp])
        return output_file
    
    def process(self, filter_assoc_file: str, vcf_file_list: List[str]) -> Union[Optional[List[str]], str]:
        '''
        :param filter_assoc_file: plink.assoc.filter文件
        :param vcf_file_list: vcf文件列表
        :return: plink.assoc.match文件, 输出文件夹
        '''

        # step1: 读取filter_assoc_file，获取SNP列表
        filter_snp_list = self.get_match_snp_list(filter_assoc_file)

        # step2: 基于snp_list创建哈希表，key为snp，value默认为""
        match_file_list = []
        for vcf_file in vcf_file_list:
            match_file = self.get_match_vcf_file(filter_snp_list, vcf_file)
            match_file_list.append(match_file)

        # match_file_list存为文件
        match_files = self.current_dir + '/match_file_list.txt'
        with open(match_files, 'w') as f:
            for match_file in match_file_list:
                f.write(match_file + '\n')
        return match_files, self.current_dir + '/match'