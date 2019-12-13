from .comment_helper import attached_comment


class ImportsParser:
    def __init__(self):
        self.import_body = ""
        self.import_comment = ""
        self.start_line = 0

    def get_imports(self, parser):
        """Parsing imports of another packages"""
        chars = parser.content[parser.index:][:7]

        if chars == "import ":
            self.import_body = self.import_body + chars
            self.start_line = parser.line_counter
            parser.index = parser.index + len(chars)

            while parser.content[parser.index] != "\n":
                if parser.content[parser.index] == "(":
                    while parser.content[parser.index] != ")":
                        if parser.content[parser.index] == "\n":
                            parser.line_counter = parser.line_counter + 1
                            parser.index = parser.index + 1
                            self.import_body = self.import_body + "<br />"
                        else:
                            self.import_body = self.import_body + parser.content[parser.index]
                            parser.index = parser.index + 1

                self.import_body = self.import_body + parser.content[parser.index]
                parser.index = parser.index + 1

            parser.index = parser.index + 1
            parser.line_counter = parser.line_counter + 1
            self.import_body = self.import_body + "<br />"

            self.get_imports_comment(parser)

    def get_imports_comment(self, parser):
        self.import_comment = attached_comment(parser, self.start_line)
        parser.imports.append(self)

        self.import_body = ""
        self.import_comment = ""

