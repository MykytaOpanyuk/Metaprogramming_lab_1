from re import search
from .comment_helper import attached_comment

class PackageParser:
    def __init__(self):
        self.package_comment = ""
        self.package_body = ""
        self.start_line = ""

    def get_package(self, parser):
        if parser.package != '':
            return

        """Parsing package name in the begin of *.go file"""
        chars = parser.content[parser.index:][:7]
        self.package_body = ""

        if chars == "package":
            self.package_body = self.package_body + chars
            self.start_line = parser.line_counter
            parser.index = parser.index + len(chars)

            while parser.content[parser.index] != "\n":
                self.package_body = self.package_body + parser.content[parser.index]
                parser.index = parser.index + 1

            parser.index = parser.index + 1
            parser.line_counter = parser.line_counter + 1
            self.package_body = self.package_body + "<br />"
            self.get_package_comment(parser)

    def get_package_comment(self, parser):
        self.package_comment = attached_comment(parser, self.start_line)
        parser.package = self

