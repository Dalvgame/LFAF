from token_type import TokenType
from token_model import Token
from ast_nodes import (
    ASTNode, Program, FunctionDef, Assignment,
    FunctionCall, BinaryOp, NumberLiteral, Identifier,
)


class ParseError(Exception):



class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self._tokens = tokens
        self._pos    = 0


    def _peek(self) -> Token:
        return self._tokens[self._pos]

    def _consume(self) -> Token:
        token = self._tokens[self._pos]
        self._pos += 1
        return token

    def _expect(self, kind: TokenType) -> Token:
        token = self._consume()
        if token.type != kind:
            raise ParseError(
                f"Expected {kind.name} but got {token.type.name} ({token.value!r})"
            )
        return token

    def _check(self, kind: TokenType) -> bool:
        return self._peek().type == kind

    def _lookahead(self, offset: int) -> TokenType:
        idx = self._pos + offset
        if idx >= len(self._tokens):
            return TokenType.EOF
        return self._tokens[idx].type

    def _at_end(self) -> bool:
        return self._check(TokenType.EOF)

    # Entry point

    def parse(self) -> Program:
        statements: list[ASTNode] = []
        while not self._at_end():
            statements.append(self._parse_statement())
        return Program(statements)

    def _parse_statement(self) -> ASTNode:
        # def keyword → function definition
        if self._check(TokenType.DEF):
            return self._parse_function_def()

        # IDENTIFIER immediately followed by '=' → assignment
        # Two-token lookahead lets us decide without consuming anything.
        if self._check(TokenType.IDENTIFIER) and self._lookahead(1) == TokenType.ASSIGN:
            return self._parse_assignment()

        # Everything else is a standalone expression
        return self._parse_expr()


    def _parse_function_def(self) -> FunctionDef:
        self._expect(TokenType.DEF)
        name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.LPAREN)

        params: list[str] = []
        if not self._check(TokenType.RPAREN):
            params.append(self._expect(TokenType.IDENTIFIER).value)
            while self._check(TokenType.COMMA):
                self._consume()                              # eat ','
                params.append(self._expect(TokenType.IDENTIFIER).value)

        self._expect(TokenType.RPAREN)
        return FunctionDef(name, params)

    def _parse_assignment(self) -> Assignment:
        var_name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.ASSIGN)
        value = self._parse_expr()
        return Assignment(var_name, value)


    def _parse_expr(self) -> ASTNode:
        left = self._parse_term()

        while self._check(TokenType.PLUS) or self._check(TokenType.MINUS):
            op    = self._consume().value
            right = self._parse_term()
            left  = BinaryOp(op, left, right)

        return left

    def _parse_term(self) -> ASTNode:
        left = self._parse_factor()

        while self._check(TokenType.MULTIPLY) or self._check(TokenType.DIVIDE):
            op    = self._consume().value
            right = self._parse_factor()
            left  = BinaryOp(op, left, right)

        return left

    def _parse_factor(self) -> ASTNode:
        t = self._peek()

        # Number literal
        if t.type == TokenType.NUMBER:
            self._consume()
            return NumberLiteral(t.value)

        # Parenthesised expression
        if t.type == TokenType.LPAREN:
            self._consume()                                  # eat '('
            inner = self._parse_expr()
            self._expect(TokenType.RPAREN)
            return inner

        # sin / cos / IDENTIFIER – could be a call or a plain variable reference
        if t.type in (TokenType.SIN, TokenType.COS, TokenType.IDENTIFIER):
            # One-token lookahead: if the next token is '(' it is a call
            if self._lookahead(1) == TokenType.LPAREN:
                return self._parse_function_call()
            # Otherwise just a variable reference
            self._consume()
            return Identifier(t.value)

        raise ParseError(
            f"Unexpected token in expression: {t.type.name} ({t.value!r})"
        )

    def _parse_function_call(self) -> FunctionCall:
        name = self._consume().value                         # function name
        self._expect(TokenType.LPAREN)

        args: list[ASTNode] = []
        if not self._check(TokenType.RPAREN):
            args.append(self._parse_expr())
            while self._check(TokenType.COMMA):
                self._consume()                              # eat ','
                args.append(self._parse_expr())

        self._expect(TokenType.RPAREN)
        return FunctionCall(name, args)