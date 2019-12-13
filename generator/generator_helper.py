import os


class GeneratorHelper:

    def __init__(self, input_path, output_path, mode):
        self.input_path = input_path
        self.output_path = output_path
        self.structure_parsing_mode = mode

    @property
    def generate_breadcrumb(self):
        if self.structure_parsing_mode == "":
            breadcrumb = '<ul class="breadcrumb"><li>' + os.path.basename(self.input_path) + '</li></ul>'
            return breadcrumb

        output_struct = self.input_path[self.input_path.find(self.structure_parsing_mode):]
        output_struct = output_struct.split(os.sep)
        depth = len(output_struct)
        breadcrumb = '<ul class="breadcrumb">'
        breadcrumb = breadcrumb + '<li><a href="' + depth * "../" + self.output_path + '">' \
                     + self.structure_parsing_mode + '/</a></li>'
        depth = depth - 1

        for item in output_struct[1:]:
            depth = depth - 1
            if depth != 0:
                breadcrumb = breadcrumb + '<li><a href="' + depth * "../" + item + \
                             self.output_path + '">' + item + '/</a></li>'
            else:
                breadcrumb = breadcrumb + '<li><a href="' + depth * "../" + item + \
                             self.output_path + '">' + item + '</a></li>'

        breadcrumb = breadcrumb + '</li></ul>'
        return breadcrumb
