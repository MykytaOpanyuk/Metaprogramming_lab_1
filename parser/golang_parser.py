from .import_parser import ImportsParser
from .package_parser import PackageParser
from .objects_parser import ObjectParser
from .objects_parser import get_type, get_const, get_variable, get_func

class GolangParser:

    def __init__(self, input_file, output_file):

        self.output_file = output_file
        self.input_file = input_file
        self.index = 0
        self.line_counter = 0

        self.content = ''
        self.package = ''
        self.imports = []
        self.const = []
        self.types = []
        self.structs = []
        self.functions = []
        self.variables = []
        self.interfaces = []
        self.comments = []
        self.comments_attached = []
        self.first_comment = ""

    def get_content(self):

        file = open(self.input_file, encoding='utf-8', mode="r")

        self.content = file.read()
        print(self.content)
        self.content = self.content.replace("\t", " ")

        file.close()

    def get_comment(self):

        """Parsing content in the begin of *.go file"""
        chars = self.content[self.index:][:2]
        temporary_content = ""

        if chars == "/*":
            self.index = self.index + len("/*")

            while self.content[self.index:][:2] != "*/":
                while self.content[self.index] != "\n":  # while not end of line
                    temporary_content = temporary_content + self.content[self.index]
                    self.index = self.index + 1
                self.index = self.index + 1
                self.line_counter = self.line_counter + 1
                temporary_content = temporary_content + "<br />"

            self.comments.append(temporary_content)
            self.comments_attached.append(False)
            self.index = self.index + len("*/")

        elif chars == "//":
            self.index = self.index + len("//")

            while self.content[self.index] != "\n" or self.content[self.index + 1:][:2] == "//":  # while not end of comment
                if self.content[self.index] == "\n" and self.content[self.index + 1:][:2] == "//":
                    temporary_content = temporary_content + "<br />"
                    self.index = self.index + 1 + len("//")
                    self.line_counter = self.line_counter + 1
                else:
                    temporary_content = temporary_content + self.content[self.index]
                    self.index = self.index + 1

            self.index = self.index + 1
            self.line_counter = self.line_counter + 1
            temporary_content = temporary_content + "<br />"

            self.comments.append(temporary_content)
            self.comments_attached.append(False)
            return
        return

    def parse_content(self):
        new_import_parser = ImportsParser()
        new_package_parser = PackageParser()

        while self.index < len(self.content):
            self.get_comment()
            new_package_parser.get_package(self)
            new_import_parser.get_imports(self)
            get_variable(self)
            get_const(self)
            get_type(self)
            get_func(self)
            if self.index < len(self.content) and self.content[self.index] == "\n":
                self.index = self.index + 1
                self.line_counter = self.line_counter + 1

        print("Parsing is done!")
        self.first_comment = self.comments[0]