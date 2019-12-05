def get_comment_for_object(self, start_line):
    prev_line = self.content.split('\n')[start_line - 2]
    return

def get_object(self, chars):
    timetable_content = ""
    brace_type_1 = False
    brace_type_2 = False
    start_line = self.line_counter

    timetable_content = timetable_content + chars
    self.index = self.index + len(chars)

    while self.content[self.index] != "\n":
        self.index = self.index + 1
        timetable_content = timetable_content + self.content[self.index]
        if self.content[self.index] == "{":
            brace_type_1 = True
        if self.content[self.index] == "(":
            brace_type_2 = True

    self.index = self.index + 1
    self.line_counter = self.line_counter + 1
    timetable_content = timetable_content + "<br />"

    if not brace_type_1 and not brace_type_2:
        self.vars.append(timetable_content)
        return

    if brace_type_2:
        while self.content[self.index] != ")":

            if self.content[self.index] == "\n":
                self.line_counter = self.line_counter + 1
                timetable_content = timetable_content + "<br />"

            self.index = self.index + 1
            timetable_content = timetable_content + self.content[self.index]

        if self.content[self.index] == "\n":
            self.index = self.index + 1
            self.line_counter = self.line_counter + 1
            timetable_content = timetable_content + "<br />"

    self.vars.append(timetable_content)
    get_comment_for_object(self, start_line)

    if brace_type_1:
        while self.content[self.index] != "}":

            if self.content[self.index] == "\n":
                self.line_counter = self.line_counter + 1
                timetable_content = timetable_content + "<br />"

            self.index = self.index + 1
            timetable_content = timetable_content + self.content[self.index]

    if self.content[self.index] == "\n":
        self.index = self.index + 1
        self.line_counter = self.line_counter + 1
        timetable_content = timetable_content + "<br />"

    self.vars.append(timetable_content)

    return


def get_variables(self):
    chars = self.content[self.index:][:4]

    if chars == "var":
        get_object(self, chars)


def get_const(self):
    chars = self.content[self.index:][:4]

    if chars == "const":
        get_object(self, chars)
