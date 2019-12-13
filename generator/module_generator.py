import os
from .file_generator import FileGenerator
from .generator_helper import GeneratorHelper


class ModuleGenerator:

    def __init__(self, input_path, output_path, mode):
        self.parser_mode = mode
        self.input_path = input_path.normpath()
        self.output_path = output_path.normpath()
        self.mode = mode

        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.template_path = os.path.join(self.my_path, "../templates/")

        all_files = []

        for root, dirs, files in os.walk(input_path):
            for file_name in files:
                all_files.append(file_name)
            break

        self.golang_files = list(filter(lambda x: x.endswith('.go'), all_files))

        self.generate_modules()

    def generate_modules(self):
        for file_name in self.golang_files:
            out_path_dir = self.output_path + os.sep + os.path.basename(file_name)
            generator = FileGenerator(out_path_dir, file_name, self.mode)
            breadcrumb = GeneratorHelper(self.input_path, self.output_path, self.mode)

        self.generate_main_file(breadcrumb)

    def generate_main_file(self, breadcrumb):
        if os.path.exists(self.output_path):
            file = open(self.output_path + "/main.html", encoding='utf-8', mode="w")

            path = self.template_path + "module_template.html"

            template = os.path.normpath(path)
            gen_file = open(template, encoding='utf-8', mode="r")
            content = gen_file.read()

            template_split = content.split("Insert_here_0")

            file.write(template_split[0] + """
            <h2>
                <code>""" + breadcrumb.generate_breadcrumb() + """</code>
                <strong class="text-success">module</strong>
            </h2>

            """ + (''.join('''
                <div class="card mb-3">
                    <div class="card-header">
                        <a href="''' +
                           os.path.join(".", os.path.basename(file), "main.html")
                           + '''">''' +
                           os.path.basename(file) + '''</a>
                </div>
            </div>
            ''' for file in self.golang_files) + """
            </div>""" + template_split[1]))
