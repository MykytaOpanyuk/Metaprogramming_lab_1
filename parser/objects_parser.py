from re import search, match

class ObjectParser:
    def __init__(self):
        self.start_line = ""
        self.object_comment = ""
        self.object_body = ""
        self.object_type = ""

    def get_object(self, parser, chars):
        brace_stack_1 = 0
        brace_stack_2 = 0
        is_first_brace = 0  # 1 - brace "{", 2 - brace "("
        self.start_line = parser.line_counter

        self.object_body = self.object_body + chars
        parser.index = parser.index + len(chars)

        while parser.content[parser.index] != "\n":
            self.object_body = self.object_body + parser.content[parser.index]

            if parser.content[parser.index] == "{":
                brace_stack_1 = brace_stack_1 + 1
                if not is_first_brace:
                    is_first_brace = 1
            if parser.content[parser.index] == "(":
                brace_stack_2 = brace_stack_2 + 1
                if not is_first_brace:
                    is_first_brace = 2
            if parser.content[parser.index] == "}":
                brace_stack_1 = brace_stack_1 - 1
            if parser.content[parser.index] == ")":
                brace_stack_2 = brace_stack_2 - 1

            parser.index = parser.index + 1

        if is_first_brace == 1 or chars == "func ":
            while parser.index < len(parser.content) and brace_stack_1 > 0:
                if parser.content[parser.index] == "\n":
                    parser.line_counter = parser.line_counter + 1
                    parser.index = parser.index + 1
                    self.object_body = self.object_body + "<br />"

                if parser.content[parser.index] == "{":
                    brace_stack_1 = brace_stack_1 + 1

                if parser.content[parser.index] == "}":
                    brace_stack_1 = brace_stack_1 - 1

                self.object_body = self.object_body + parser.content[parser.index]
                parser.index = parser.index + 1

        if is_first_brace == 2 and chars != "func ":
            while brace_stack_2 > 0:
                a = parser.content[parser.index]
                if parser.content[parser.index] == "\n":
                    parser.line_counter = parser.line_counter + 1
                    parser.index = parser.index + 1
                    self.object_body = self.object_body + "<br />"

                if parser.content[parser.index] == "(":
                    brace_stack_2 = brace_stack_2 + 1

                if parser.content[parser.index] == ")":
                    brace_stack_2 = brace_stack_2 - 1

                self.object_body = self.object_body + parser.content[parser.index]
                parser.index = parser.index + 1

        parser.index = parser.index + 1
        parser.line_counter = parser.line_counter + 1
        self.object_body = self.object_body + "<br />"
        self.get_comment_for_object(parser)

    def get_comment_for_object(self, parser):
        previous_line = parser.content.split('\n')[self.start_line - 1]

        if previous_line.find('*/') >= 0 or previous_line.find('//') >= 0:
            self.object_comment = parser.comments[-1]
            parser.comments_attached[-1] = True


def get_variable(parser):
    chars = parser.content[parser.index:][:4]
    self = ObjectParser()

    if chars == "var ":
        self.get_object(parser, chars)
        parser.variables.append(self)


def get_const(parser):
    chars = parser.content[parser.index:][:6]
    self = ObjectParser()

    if chars == "const ":
        self.get_object(parser, chars)
        parser.const.append(self)


def get_type(parser):
    chars = parser.content[parser.index:][:5]
    self = ObjectParser()

    if chars == "type ":
        self.get_object(parser, chars)

        first_str = parser.content.split('\n')[self.start_line]
        self.type_name: str
        list_str = first_str.split(' ')

        self.object_type = list_str[2]
        self.name = list_str[1]

        parser.types.append(self)


def get_func(parser):
    chars = parser.content[parser.index:][:5]
    self = ObjectParser()

    if chars == "func ":
        self.get_object(parser, chars)

        first_str = parser.content.split('\n')[self.start_line]
        self.object_type = "func"
        index = len("func ")
        brace_stack = 0
        buffer = ""

        self.func_name = ""
        self.inputs = []
        self.returns = []
        self.check_is_definition = 1

        while index < len(first_str): # check is function definition
            if first_str[index] == "{":
                self.check_is_definition = 0
            index = index + 1

        index = len("func ")

        while index < len(first_str):
            if brace_stack == 0 and match("[a-zA-Z0-9_]", first_str[index]):
                while index < len(first_str) and first_str[index] != "(":
                    buffer = buffer + first_str[index]
                    index = index + 1

                self.func_name = buffer
                buffer = ""
            if index < len(first_str) and first_str[index] == "(":
                brace_stack = brace_stack + 1
                if not match("[a-zA-Z0-9_]", first_str[index - 1]):
                    index = index + 1
                    while first_str[index] != ")":
                        buffer = buffer + first_str[index]
                        index = index + 1
                    brace_stack = brace_stack - 1

                    if self.func_name == "":
                        self.inputs.append(buffer)
                    else:
                        self.returns.append(buffer)
                    buffer = ""
                elif match("[a-zA-Z0-9_]", first_str[index - 1]):
                    index = index + 1
                    while first_str[index] != ")":
                        buffer = buffer + first_str[index]
                        index = index + 1

                    brace_stack = brace_stack - 1
                    self.inputs.append(buffer)
                    buffer = ""
            elif index < len(first_str) and self.func_name != "" and len(self.inputs) > 0:
                while first_str[index] != "{" or index + 1 < len(first_str):
                    buffer = buffer + first_str[index]
                    index = index + 1

                if len(buffer) > 1:
                    self.returns.append(buffer[1:-1])
                buffer = ""
            index = index + 1
        parser.functions.append(self)