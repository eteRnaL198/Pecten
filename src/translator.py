import sys
from typing import List

from base.lang_processor.c_parser import CParser
from customizer.lang_processor.aspect_parser import AspectParser
from customizer.src import Src
from src.customizer.aspect.pure_aspect import PureAspect
from util.file_util import backup_file, generate_full_path


class Translator:
    def __init__(self):
        if len(sys.argv) > 1:
            self.aspect_file = [sys.argv[1]]  # TODO 複数ファイルに対応
            self.base_file = [sys.argv[2]]
            # for arg in sys.argv[1:]:
            #     print(self.aspect_file.endswith(".acc"))
            #     print(self.base_file.endswith(".c"))
        else:
            self.aspect_file = "acc/aspect.acc"
            self.base_file = "acc/base.c"

    def parse_aspect(self):
        return (AspectParser(self.aspect_file)).parse()

    def parse_base(self):
        return CParser(self.base_file).parse()

    def translate(self, aspects: List[PureAspect], c_asts):
        backup_file(self.base_file)  # TODO 複数ファイルに対応
        target_path = generate_full_path(self.base_file)
        with open(target_path, mode="r") as f:
            target_src = Src(f.readlines())
        for asp in aspects:
            asp.weave(target_src, c_asts)
            for line in target_src.get():
                print(line, end="")
        with open(target_path, mode="w") as f:
            f.writelines(target_src.get())


if __name__ == "__main__":
    translator = Translator()
    aspects = translator.parse_aspect()
    c_asts = translator.parse_base()
    translator.translate(aspects, c_asts)
