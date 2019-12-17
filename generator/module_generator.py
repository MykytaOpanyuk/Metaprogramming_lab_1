import os
from .file_generator import FileGenerator
from .generator_helper import GeneratorHelper


class ModuleGenerator:

    def __init__(self, input_path, output_path, mode, input_root_dir):
        self.parser_mode = mode
        self.input_root_dir = os.path.normpath(input_root_dir)
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)

        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.template_path = os.path.join(self.my_path, "../templates/")
        self.golang_files = []

        all_files = []

        for root, dirs, files in os.walk(input_path):
            for file_name in files:
                all_files.append(os.path.join(root, file_name))
            break

        if len(all_files) > 0:
            self.golang_files = list(filter(lambda x: x.endswith('.go'), all_files))

        self.html_helper = GeneratorHelper()

    def generate_modules(self):
        if len(self.golang_files) > 0:
            for file_name in self.golang_files:
                out_path_dir = self.output_path + os.sep
                generator = FileGenerator(file_name, out_path_dir, self.parser_mode, self.input_root_dir)
                generator.generate_file()

            self.generate_main_file(self.html_helper)

    def generate_main_file(self, breadcrumb):
        if os.path.exists(self.output_path):
            result = open(self.output_path + "/index_" +
                        os.path.basename(self.output_path) + "_go.html", encoding='utf-8', mode="w")

            path = self.template_path + "module_template.html"

            template = os.path.normpath(path)
            gen_file = open(template, encoding='utf-8', mode="r")
            content = gen_file.read()

            gen_file.close()

            template_split = content.split("Insert_here_0")

            result.write(template_split[0])
            if self.parser_mode != "file" and self.parser_mode != "module":
                result.write(
                    '''<a href="''' + self.input_root_dir + os.sep + "index_" + self.parser_mode + "_go.html" +
                    '''" class="btn btn-info float-right" role="button">Return to the main page</a><h2>''')

                result.write('''<code class="container-fluid">''' + breadcrumb.generate_breadcrumb(self) + """</code>
                <strong class="text-success"><br />Module:"""
                       + os.path.basename(self.output_path) + """<br /></strong>
            </h2>""")
            for go_file in self.golang_files:
                result.write('''
                <div class="card mb-3">
                    <div class="card-header">
                        <a href="''' + self.output_path + os.sep + os.path.basename(go_file)[:-3] +
                           '''.html">''' + os.path.basename(go_file)[:-3] + '''.html</a>
                    </div>
                </div>''')
            result.write(template_split[1])

            result.close()
