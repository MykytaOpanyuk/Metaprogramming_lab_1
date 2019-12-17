from .objects_parser import get_type, get_const, get_variable, get_func, get_import, get_package
import os


class GolangParser:

    def __init__(self, input_file):

        self.input_file = input_file
        self.index = 0
        self.line_counter = 0

        self.content = ''
        self.package = ''
        self.imports = []
        self.const = []
        self.types = []
        self.functions = []
        self.variables = []
        self.comments = []
        self.comments_attached = []
        self.first_comment = ""

        self.get_content()
        self.parse_content()

    def get_content(self):
        self.input_file = os.path.normpath(self.input_file)
        file = open(self.input_file, encoding='utf-8', mode="r")

        self.content = file.read()
        print(self.content)
        self.content = self.content.replace("\t", " &emsp; ")
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

            while self.content[self.index] != "\n" or self.content[self.index + 1:][
                                                      :2] == "//":  # while not end of comment
                if self.content[self.index] == "\n" and self.content[self.index + 1:][:2] == "//":
                    check_is_multiple = True
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
        while self.index < len(self.content):
            if self.line_counter > 5630:
                print("stop")
            self.get_comment()
            get_package(self)
            get_import(self)
            get_type(self)
            get_const(self)
            get_variable(self)
            get_func(self)
            if self.index < len(self.content) and self.content[self.index] == "\n":
                self.index = self.index + 1
                self.line_counter = self.line_counter + 1
            if self.index < len(self.content) and self.content[self.index] == " ":
                self.index = self.index + 1
            if self.index < len(self.content) and self.content[self.index] == "\t":
                self.index = self.index + 1

        print("Parsing is done!")
        if len(self.comments) > 0:
            self.first_comment = self.comments[0]

