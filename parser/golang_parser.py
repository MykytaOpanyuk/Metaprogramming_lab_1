from .import_parser import ImportsParser
from .package_parser import PackageParser


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
        self.comments_attached = []

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
            self.comments_attached.append(False)
            self.index = self.index + len("*/")

        elif chars == "//":
            self.index = self.index + len("//")

            while self.content[self.index] != "\n":  # while not end of comment
                timetable_content = timetable_content + self.content[self.index]
                self.index = self.index + 1

                if self.content[self.index] == "\n" and self.content[self.index + 1:][:2] == "//":
                    self.index = self.index + 1 + len("//")
                    self.line_counter = self.line_counter + 1
                    timetable_content = timetable_content + "<br />"
                    while self.content[self.index] != "\n":
                        timetable_content = timetable_content + self.content[self.index]
                        self.index = self.index + 1

            self.index = self.index + 1
            self.line_counter = self.line_counter + 1
            timetable_content = timetable_content + "<br />"
            self.comments.append(timetable_content)
            self.comments_attached.append(False)
            return
        return

    def parse_content(self):
        new_import_parser = ImportsParser()
        new_package_parser = PackageParser()
        while self.content and self.index < len(self.content):
            self.get_comment()
            new_package_parser.get_package(self)
            new_import_parser.get_imports(self)
            if self.content[self.index] == "\n":
                self.index = self.index + 1
                self.line_counter = self.line_counter + 1
