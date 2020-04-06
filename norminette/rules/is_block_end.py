from lexer import Token
from rules import PrimaryRule
from context import (
                    Function,
                    UserDefinedType,
                    VariableAssignation,
                    ControlStructure)


class IsBlockEnd(PrimaryRule):
    def __init__(self):
        super().__init__()
        self.priority = 9
        self.scope = [
                        Function,
                        UserDefinedType,
                        VariableAssignation,
                        ControlStructure]

    def check_udef_typedef(self, context, pos):
        i = context.skip_ws(pos)
        if context.check_token(i, "IDENTIFIER") is False:
            return False, 0
        i += 1
        i = context.skip_ws(i)
        if context.check_token(i, "SEMI_COLON") is False:
            return False, 0
        i += 1
        return True, i

    def run(self, context):
        i = context.skip_ws(0)
        if context.check_token(i, "RBRACE") is False:
            return False, 0

        context.sub = context.scope.outer()
        i += 1
        if type(context.scope) is UserDefinedType:
            i = context.skip_ws(i)
            if context.check_token(i, "TYPEDEF") is True:
                i += 1
                ret, i = self.check_udef_typedef(context, i)
                i = context.eol(i)
                return ret, i
            if context.scope.typedef is True:
                ret, i = self.check_udef_typedef(context, i)
                i = context.eol(i)
                return ret, i
            i = context.skip_ws(i)
            if context.check_token(i, "SEMI_COLON"):
                i += 1
                i = context.eol(i)
                return True, i
        if type(context.scope) is VariableAssignation:
            pass
        if type(context.scope) is ControlStructure:
            pass
        i = context.eol(i)
        return True, i