from re import search


class PackageParser:
    start_line: int
    package_comment: str
    package_body: str

    def get_package(self, parser):
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
            self.get_package_comment()
            return
        return

    def get_package_comment(self, parser):
        previous_line = parser.content.split('\n')[self.start_line - 1]

        if search(r"(\*/|/\*|/{2,})", previous_line):
            self.package_comment = parser.comments[-1]
            parser.comments_attached[-1] = True

        parser.package = self
        return
