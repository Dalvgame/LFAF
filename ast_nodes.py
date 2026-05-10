"""
Abstract Syntax Tree node definitions.

Every node extends ASTNode and implements:
  - label()    – a human-readable description (used when printing the tree)
  - children() – ordered list of child nodes (default: empty)

The print() method on the base class draws the whole subtree with
Unicode box-drawing characters so the hierarchy is easy to read.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Base class for every node in the AST."""

    @abstractmethod
    def label(self) -> str:
        """Short, readable description of this node."""

    def children(self) -> list[ASTNode]:
        """Ordered child nodes. Override in compound nodes."""
        return []

    def print(self, indent: str = "", is_last: bool = True) -> None:
        """Recursively pretty-print the subtree rooted at this node."""
        branch = "└── " if is_last else "├── "
        print(indent + branch + self.label())
        child_indent = indent + ("    " if is_last else "│   ")
        kids = self.children()
        for i, child in enumerate(kids):
            child.print(child_indent, i == len(kids) - 1)


# ---------------------------------------------------------------------------
# Concrete node types
# ---------------------------------------------------------------------------

class Program(ASTNode):
    """Root node – holds a list of top-level statements."""

    def __init__(self, statements: list[ASTNode]) -> None:
        self.statements = statements

    def label(self) -> str:
        return "Program"

    def children(self) -> list[ASTNode]:
        return self.statements


class FunctionDef(ASTNode):
    """
    A function *signature* (no body in this toy language).
    Example: ``def add(x, y)``
    """

    def __init__(self, name: str, params: list[str]) -> None:
        self.name   = name
        self.params = params

    def label(self) -> str:
        return f"FunctionDef: {self.name}({', '.join(self.params)})"

    # No child nodes – params are stored as plain strings on the label


class Assignment(ASTNode):
    """
    Variable assignment.
    Example: ``result = 10.5 - 1.1 / 2``
    """

    def __init__(self, variable: str, value: ASTNode) -> None:
        self.variable = variable
        self.value    = value

    def label(self) -> str:
        return f"Assign: {self.variable}"

    def children(self) -> list[ASTNode]:
        return [self.value]


class FunctionCall(ASTNode):
    """
    A function call with zero or more argument expressions.
    Example: ``sin(3.14)``
    """

    def __init__(self, name: str, args: list[ASTNode]) -> None:
        self.name = name
        self.args = args

    def label(self) -> str:
        return f"Call: {self.name}"

    def children(self) -> list[ASTNode]:
        return self.args


class BinaryOp(ASTNode):
    """
    A binary infix operation.
    Example: ``x + y * 2``
    """

    def __init__(self, op: str, left: ASTNode, right: ASTNode) -> None:
        self.op    = op
        self.left  = left
        self.right = right

    def label(self) -> str:
        return f"BinaryOp: {self.op}"

    def children(self) -> list[ASTNode]:
        return [self.left, self.right]


class NumberLiteral(ASTNode):
    """A numeric literal – integer or float."""

    def __init__(self, value: str) -> None:
        self.value = value

    def label(self) -> str:
        return f"Number: {self.value}"


class Identifier(ASTNode):
    """A variable reference."""

    def __init__(self, name: str) -> None:
        self.name = name

    def label(self) -> str:
        return f"Identifier: {self.name}"