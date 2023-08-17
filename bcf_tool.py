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