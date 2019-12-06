from re import search


class ObjectParser:
    start_line: int
    object_comment: str
    object_body: str

    def get_object(self, parser, chars):
        brace_stack_1 = 0
        brace_stack_2 = 0
        is_first_brace = 0  # 1 - brace "{", 2 - brace "("
        self.start_line = parser.line_counter

        self.object_body = self.object_body + chars
        parser.index = parser.index + len(chars)

        while parser.content[parser.index] != "\n":
            parser.index = parser.index + 1
            self.object_body = self.object_body + parser.content[parser.index]
            if parser.content[parser.index] == "{":
                brace_stack_1 = brace_stack_1 + 1
                if not is_first_brace:
                    is_first_brace = 1
            if parser.content[parser.index] == "(":
                brace_stack_2 = brace_stack_2 + 1
                if not is_first_brace:
                    is_first_brace = 2

        parser.index = parser.index + 1
        parser.line_counter = parser.line_counter + 1
        self.object_body = self.object_body + "<br />"

        if brace_stack_1 == 0 and brace_stack_2 == 0:
            parser.vars.append(self)
            return

        if is_first_brace == 2:
            while brace_stack_2 > 0:
                if parser.content[parser.index] == "(":
                    brace_stack_2 = brace_stack_2 + 1

                if parser.content[parser.index] == ")":
                    brace_stack_2 = brace_stack_2 - 1

                if parser.content[parser.index] == "\n":
                    parser.line_counter = parser.line_counter + 1
                    self.object_body = self.object_body + "<br />"

                parser.index = parser.index + 1
                self.object_body = self.object_body + parser.content[parser.index]

        if is_first_brace == 1:
            while brace_stack_1 > 0:
                if parser.content[parser.index] == "{":
                    brace_stack_1 = brace_stack_1 + 1

                if parser.content[parser.index] == "}":
                    brace_stack_1 = brace_stack_1 - 1

                if parser.content[parser.index] == "\n":
                    parser.line_counter = parser.line_counter + 1
                    self.object_body = self.object_body + "<br />"

                parser.index = parser.index + 1
                self.object_body = self.object_body + parser.content[parser.index]
        parser.index = parser.index + 1
        parser.line_counter = parser.line_counter + 1
        self.object_body = self.object_body + "<br />"
        self.get_comment_for_object(self, parser)

        if chars == "var":
            parser.variables.append(self)
        else:
            parser.const.append(self)

        return

    def get_comment_for_object(self, parser):
        previous_line = parser.content.split('\n')[self.start_line - 1]

        if search(r"(\*/|/\*|/{2,})", previous_line):
            self.object_comment = parser.comments[-1]
            parser.comments_attached[-1] = True

        return

    def get_variables(self, parser):
        chars = parser.content[parser.index:][:4]

        if chars == "var":
            self.get_object(parser, chars)

    def get_const(self, parser):
        chars = parser.content[parser.index:][:4]

        if chars == "const":
            self.get_object(parser, chars)
