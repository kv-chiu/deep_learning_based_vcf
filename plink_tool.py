from collections import defaultdict

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

    def process(self, filter_assoc_file: str, vcf_file_list: List[str]) -> Optional[str]:
        '''
        :param filter_assoc_file: plink.assoc.filter文件
        :param vcf_file_list: vcf文件列表
        :return: plink.assoc.match文件
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

        # step2: 基于snp_list创建哈希表，key为snp，value默认为""
        snp_dict = defaultdict(str)
        for vcf_file in vcf_file_list:
            with open(vcf_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                else:
                    snp = line.split()[2]
                    if snp in snp_list:
                        snp_dict[snp] = line

        # step3: 读取snp_dict，将value写入新文件
        output_file = self.current_dir + '/plink.assoc.match'
        with open(output_file, 'w') as f:
            for snp in snp_list:
                f.write(snp_dict[snp])
        return output_file
