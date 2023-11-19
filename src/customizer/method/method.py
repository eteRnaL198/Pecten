from customizer.pointcut.func_signature import FuncSignature


class Method:
    """メソッド"""

    def __init__(self, signature: FuncSignature, body):
        """
        Args:
            signature (FuncSignature): メソッドのシグネチャ
            body (list[str]): メソッドの中身
        """
        self.signature: FuncSignature = signature
        self.body: list[str] = body

    def __str__(self) -> str:
        return str(self.signature) + "{\n" + "\n".join(self.body) + "\n}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Method):
            return False
        return self.signature == other.signature

    def replace(self, current, new):
        self.body = [line.replace(current, new) for line in self.body]
