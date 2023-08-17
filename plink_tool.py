from typing import Optional

from interfaces import DataPreparationTool
from config import ENV_PATH

class PlinkAssocTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_file: str, phe_file: str,
                is_make_bed: str = 'y', is_allow_no_sex: str = 'y',
                is_allow_extra_chr: str = 'y') -> Optional[str]:
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
