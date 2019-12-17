from re import match


class ObjectParser:
    def __init__(self):
        self.start_line = 0
        self.object_comment = ""
        self.object_body = ""
        self.object_type = ""

    def get_object(self, parser, chars):
        brace_stack_1 = 0
        brace_stack_2 = 0
        apostrophe_found_3 = False

        self.start_line = parser.line_counter

        self.object_body = self.object_body + chars
        parser.index = parser.index + len(chars)

        while parser.content[parser.index] != "\n":

            if parser.content[parser.index] == "{":
                brace_stack_1 = brace_stack_1 + 1
            if parser.content[parser.index] == "(":
                brace_stack_2 = brace_stack_2 + 1
            if parser.content[parser.index] == "}":
                brace_stack_1 = brace_stack_1 - 1
            if parser.content[parser.index] == ")":
                brace_stack_2 = brace_stack_2 - 1

            if parser.content[parser.index] == "`" and apostrophe_found_3:
                apostrophe_found_3 = False

            if parser.content[parser.index] == "`" and not apostrophe_found_3:
                apostrophe_found_3 = True

            self.object_body = self.object_body + parser.content[parser.index]
            parser.index = parser.index + 1

        while parser.index < len(parser.content) and brace_stack_2 > 0 or brace_stack_1 > 0 or apostrophe_found_3:
            while parser.index < len(parser.content) and parser.content[parser.index] != "\n":
                if parser.content[parser.index] == "(":
                    brace_stack_2 = brace_stack_2 + 1

                if parser.content[parser.index] == "{":
                    brace_stack_1 = brace_stack_1 + 1

                if parser.content[parser.index] == "`" and not apostrophe_found_3:
                    apostrophe_found_3 = True

                if parser.content[parser.index] == ")":
                    brace_stack_2 = brace_stack_2 - 1

                if parser.content[parser.index] == "}":
                    brace_stack_1 = brace_stack_1 - 1

                if parser.content[parser.index] == "`" and apostrophe_found_3:
                    apostrophe_found_3 = False

                self.object_body = self.object_body + parser.content[parser.index]
                parser.index = parser.index + 1

            parser.line_counter = parser.line_counter + 1
            self.object_body = self.object_body + " <br /> "
            parser.index = parser.index + 1

        parser.index = parser.index + 1
        parser.line_counter = parser.line_counter + 1
        self.object_body = self.object_body + " <br /> "
        self.get_comment_for_object(parser)

    def get_comment_for_object(self, parser):
        previous_line = parser.content.split('\n')[self.start_line - 1]

        if previous_line.find('*/') >= 0 or previous_line.find('//') >= 0:
            self.object_comment = parser.comments[-1]
            parser.comments_attached[-1] = True


def get_package(parser):
    chars = parser.content[parser.index:][:8]
    self = ObjectParser()

    if chars == "package ":
        self.get_object(parser, chars)
        self.name = parser.content.split('\n')[self.start_line]
        self.name = self.name.split(' ')[1]
        parser.package = self


def get_import(parser):
    chars = parser.content[parser.index:][:7]
    self = ObjectParser()

    if chars == "import ":
        self.get_object(parser, chars)
        self.name = parser.content.split('\n')[self.start_line]
        parser.imports.append(self)


def get_variable(parser):
    chars = parser.content[parser.index:][:4]
    self = ObjectParser()

    if chars == "var ":
        self.get_object(parser, chars)
        self.name = parser.content.split('\n')[self.start_line]
        parser.variables.append(self)


def get_const(parser):
    chars = parser.content[parser.index:][:6]
    self = ObjectParser()

    if chars == "const ":
        self.get_object(parser, chars)
        self.name = parser.content.split('\n')[self.start_line]
        parser.const.append(self)


def get_type(parser):
    chars = parser.content[parser.index:][:5]
    self = ObjectParser()

    if chars == "type ":
        self.get_object(parser, chars)

        first_str = parser.content.split('\n')[self.start_line]
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
        self.inputs = ""
        self.returns = ""
        self.brace_stack_body = 0

        while index < len(first_str):  # check is function definition
            if first_str[index] == "{":
                self.brace_stack_body = self.brace_stack_body + 1
            index = index + 1

        index = len("func ")

        while index < len(self.object_body) and self.brace_stack_body > 0:
            if brace_stack == 0 and match("[a-zA-Z0-9_]", self.object_body[index]) and not self.func_name:
                while index < len(self.object_body) and self.object_body[index] != "(":
                    buffer = buffer + self.object_body[index]
                    index = index + 1

                self.func_name = buffer
                buffer = ""
            if index < len(self.object_body) and self.object_body[index] == "{":
                self.brace_stack_body = self.brace_stack_body - 1
            if index < len(self.object_body) and self.object_body[index] == "(":
                brace_stack = brace_stack + 1
                if not match("[a-zA-Z0-9_]", self.object_body[index - 1]):
                    index = index + 1
                    while self.object_body[index] != ")":
                        buffer = buffer + self.object_body[index]
                        index = index + 1
                    brace_stack = brace_stack - 1

                    if self.func_name == "":
                        self.inputs = buffer
                    else:
                        self.returns = buffer
                    buffer = ""
                elif match("[a-zA-Z0-9_]", self.object_body[index - 1]):
                    index = index + 1
                    while self.object_body[index] != ")":
                        buffer = buffer + self.object_body[index]
                        index = index + 1

                    brace_stack = brace_stack - 1
                    self.inputs = buffer
                    buffer = ""
            elif index < len(self.object_body) and self.func_name != "" and len(self.inputs) > 0:
                while self.object_body[index] != "{" and index + 1 < len(self.object_body):
                    buffer = buffer + self.object_body[index]
                    index = index + 1

                if len(buffer) > 1:
                    self.returns = buffer[1:-1]
                buffer = ""
            else:
                index = index + 1
        parser.functions.append(self)
