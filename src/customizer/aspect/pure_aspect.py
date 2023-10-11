from typing import List

from aspect import Aspect
from pycparser import c_ast


class PureAspect:
    def __init__(self, name, aspects):
        """
        Args:
            name (str): アスペクト名
            aspects list[(Aspect)]: アスペクトのリスト
        """
        self.name: str = name
        self.aspects: List[Aspect] = aspects

    def weave(self, src: List[str], ast: c_ast.FileAST):
        """アスペクトを織り込む
        Args:
            src (List[str]): アスペクトを織り込むソースコード
            ast (c_ast.FileAST): 構文木
        Returns:
            List[str]: アスペクトが織り込まれたソースコード
        """
        for aspect in self.aspects:
            lines = aspect.get_joinpoints(ast)
            body = aspect.advice_body
            accumulated_line = 0
            for l in lines:
                src.insert(l + accumulated_line, *body)
                accumulated_line += len(body)
        return src
