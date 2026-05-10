from __future__ import annotations
from abc import ABC, abstractmethod


class ASTNode(ABC):


    @abstractmethod
    def label(self) -> str:


    def children(self) -> list[ASTNode]:

        return []

    def print(self, indent: str = "", is_last: bool = True) -> None:

        branch = "└── " if is_last else "├── "
        print(indent + branch + self.label())
        child_indent = indent + ("    " if is_last else "│   ")
        kids = self.children()
        for i, child in enumerate(kids):
            child.print(child_indent, i == len(kids) - 1)



# Concrete node types

class Program(ASTNode):


    def __init__(self, statements: list[ASTNode]) -> None:
        self.statements = statements

    def label(self) -> str:
        return "Program"

    def children(self) -> list[ASTNode]:
        return self.statements


class FunctionDef(ASTNode):

    def __init__(self, name: str, params: list[str]) -> None:
        self.name   = name
        self.params = params

    def label(self) -> str:
        return f"FunctionDef: {self.name}({', '.join(self.params)})"




class Assignment(ASTNode):

    def __init__(self, variable: str, value: ASTNode) -> None:
        self.variable = variable
        self.value    = value

    def label(self) -> str:
        return f"Assign: {self.variable}"

    def children(self) -> list[ASTNode]:
        return [self.value]


class FunctionCall(ASTNode):

    def __init__(self, name: str, args: list[ASTNode]) -> None:
        self.name = name
        self.args = args

    def label(self) -> str:
        return f"Call: {self.name}"

    def children(self) -> list[ASTNode]:
        return self.args


class BinaryOp(ASTNode):

    def __init__(self, op: str, left: ASTNode, right: ASTNode) -> None:
        self.op    = op
        self.left  = left
        self.right = right

    def label(self) -> str:
        return f"BinaryOp: {self.op}"

    def children(self) -> list[ASTNode]:
        return [self.left, self.right]


class NumberLiteral(ASTNode):


    def __init__(self, value: str) -> None:
        self.value = value

    def label(self) -> str:
        return f"Number: {self.value}"


class Identifier(ASTNode):


    def __init__(self, name: str) -> None:
        self.name = name

    def label(self) -> str:
        return f"Identifier: {self.name}"