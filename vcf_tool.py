from typing import Optional, List

from interfaces import DataPreparationTool
from config import ENV_PATH

class VcfMergeTool(DataPreparationTool):
    def __init__(self):
        super().__init__()

    def process(self, vcf_file_list: List[str]) -> Optional[str]:
        if len(vcf_file_list) < 2:
            return None

        vcf_file_list_str = " ".join(vcf_file_list)
        output_file = self.get_output_file_path("merged.vcf")
        command = f"bcftools merge {vcf_file_list_str} -o {output_file}"
        self.execute_command(command)
        return output_file