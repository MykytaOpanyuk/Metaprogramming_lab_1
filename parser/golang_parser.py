class GolangParser:

    def __init__(self, input_file, output_file):

        self.output_file = output_file
        self.input_file = input_file
        self.index = 0
        self.line_counter = 0
        self.content = ""

        self.package = ""
        self.imports = []
        self.const = []
        self.types = []
        self.structs = []
        self.functions = []
        self.methods = []
        self.variables = []
        self.comments = []

    def get_content(self):

        file = open(self.input_file, encoding='utf-8', mode="r")

        self.content = file.read()
        print(self.content)

        file.close()

    def get_comment(self):

        """Parsing content in the begin of *.go file"""
        chars = self.content[self.index:][:2]
        timetable_content = ""

        if chars == "/*":
            self.index = self.index + len("/*")

            while self.content[self.index:][:2] != "*/":
                while self.content[self.index] != "\n":  # while not end of line
                    timetable_content = timetable_content + self.content[self.index]
                    self.index = self.index + 1
                self.line_counter = self.line_counter + 1
                timetable_content = timetable_content + "<br />"

            self.comments.append(timetable_content)
            self.index = self.index + len("*/")

        elif chars == "//":
            self.index = self.index + len("//")

            while self.content[self.index] != "\n":  # while not end of comment
                timetable_content = timetable_content + self.content[self.index]
                self.index = self.index + 1

                if self.content[self.index + 1] == "\n" and self.content[self.index + 2:][:2] == "//":
                    self.index = self.index + 2 + len("//")
                    self.line_counter = self.line_counter + 1
                    timetable_content = timetable_content + "<br />"
                    while self.content[self.index] != "\n":
                        timetable_content = timetable_content + self.content[self.index]
                        self.index = self.index + 1

            self.index = self.index + 1
            self.line_counter = self.line_counter + 1
            timetable_content = timetable_content + "<br />"
            self.comments.append(timetable_content)
            return
        return

    def get_package(self):
        """Parsing package name in the begin of *.go file"""
        chars = self.content[self.index:][:7]
        timetable_content = ""

        if chars == "package":
            timetable_content = timetable_content + chars
            self.index = self.index + len(chars)

            while self.content[self.index] != "\n":
                timetable_content = timetable_content + self.content[self.index]
                self.index = self.index + 1

            self.index = self.index + 1
            self.line_counter = self.line_counter + 1
            timetable_content = timetable_content + "<br />"
            self.package = timetable_content
            return
        return

    def get_imports(self):
        """Parsing imports of another packages"""
        chars = self.content[self.index:][:6]
        timetable_content = ""

        if chars == "import":  # TODO: check parsing multiline import
            timetable_content = timetable_content + chars
            self.index = self.index + len(chars)

            while self.content[self.index] != "\n":
                if self.content[self.index] == "(":
                    while self.content[self.index] != ")":
                        if self.content[self.index] == "\n":
                            self.line_counter = self.line_counter + 1
                            self.index = self.index + 1
                            timetable_content = timetable_content + "<br />"
                        else:
                            timetable_content = timetable_content + self.content[self.index]
                            self.index = self.index + 1

                timetable_content = timetable_content + self.content[self.index]
                self.index = self.index + 1

            self.index = self.index + 1
            self.line_counter = self.line_counter + 1
            timetable_content = timetable_content + "<br />"
            self.imports.append(timetable_content)

    def parse_content(self):
        while self.content and self.index < len(self.content):
            self.get_comment()
            self.get_package()
            self.get_imports()
            if self.content[self.index] == "\n":
                self.index = self.index + 1