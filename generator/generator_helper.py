import os
import collections

all_lists_name = {}

class GeneratorHelper:

    def __init__(self):
        return

    @staticmethod
    def generate_breadcrumb(self):
        output_struct = self.input_path[self.input_path.find(self.parser_mode):]
        output_struct = output_struct.split(os.sep)
        i = 0
        depth = 0

        while i < len(output_struct):
            if output_struct[i].endswith('.go'):
                output_struct[i] = output_struct[i][:-3] + ".html"
            i = i + 1

        if len(output_struct) > 1:
            depth = len(output_struct) - 1
        else:
            depth = len(output_struct)
        breadcrumb = '<ul class="breadcrumb">'

        if self.parser_mode != "file" and self.parser_mode != "module":
            for item in output_struct:
                if depth != 0:
                    breadcrumb = breadcrumb + '<a href="' + \
                                 self.output_path + "/" + depth * "../" + item + '">' + item + '/</a>'
                else:
                    breadcrumb = breadcrumb + '<a href="' + \
                                 self.output_path + "/" + depth * "../" + item + '">' + item + '</a>'
                depth = depth - 1
            breadcrumb = breadcrumb + '</ul>'
            return breadcrumb

    @staticmethod
    def get_names(self):
        list_name = []
        path = self.output_path + "/" + os.path.basename(self.input_path)[:-3] + ".html"

        index = 0
        while index < len(self.parser.const):
            list_name.append(self.parser.const[index].name)
            index += 1

        index = 0
        while index < len(self.parser.types):
            name = self.parser.types[index].name + self.parser.types[index].object_type
            list_name.append(name)
            index += 1

        index = 0
        while index < len(self.parser.variables):
            list_name.append(self.parser.variables[index].name)
            index += 1

        index = 0
        while index < len(self.parser.functions):
            name = self.parser.functions[index].func_name + self.parser.functions[index].inputs \
                   + self.parser.functions[index].returns
            list_name.append(name)
            index += 1

        index = 0
        while index < len(list_name):
            all_lists_name[list_name[index]] = path
            index += 1

    @staticmethod
    def generate_alphabetical_index(output_path):
        global all_lists_name
        all_lists_name = collections.OrderedDict(sorted(all_lists_name.items()))

        if os.path.exists(output_path):
            with open(os.path.join(output_path, "main.html"), "a") as file:
                file.write("""<div class="container">
                        <h2>
                            <span>Alphabetical index list:</span>
                        </h2>
                    """ + ''.join(('<hr style="height:2p"/><h2>{}</h2><br />'.format(
                    key) if value == "" else '<a href="{}">{}</a><br />'.format(value, key)) for (key, value) in
                  all_lists_name.items()) + """</div>""")
