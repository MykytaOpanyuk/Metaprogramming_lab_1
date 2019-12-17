from .module_generator import ModuleGenerator
from .generator_helper import GeneratorHelper
import os
import glob


class ProjectGenerator:

    def __init__(self, input_path, output_path, mode, input_root_dir):
        self.parser_mode = mode
        self.input_root_dir = input_root_dir
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)
        self.html_helper = GeneratorHelper()
        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.template_path = os.path.join(self.my_path, "../templates/")

        self.module_list = []

        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        for item in os.listdir(os.path.normpath(input_path)):
            joined_path = os.path.join(os.path.normpath(input_path), item)
            if os.path.isdir(joined_path) and os.path.basename(joined_path) != ".git":
                self.module_list.append(joined_path)

        all_files = []

        for root, dirs, files in os.walk(input_path):
            for file_name in files:
                all_files.append(file_name)

        self.golang_files = list(filter(lambda x: x.endswith('.go'), all_files))
        self.golang_files = sorted(self.golang_files)

        self.golang_modules = []
        self.golang_subprojects = []

        self.html_modules = []

    def parse_modules(self):
        if len(self.golang_files) > 0:
            generator = ModuleGenerator(self.input_path, self.output_path, self.parser_mode, self.input_root_dir)
            generator.generate_modules()

        self.golang_modules = list(filter(lambda module:
                                          len(glob.glob(module + "/*.go")) != 0, self.module_list))

        for mod_path in self.golang_modules:
            out_path_dir = self.output_path + os.sep + os.path.basename(mod_path)

            if not os.path.exists(out_path_dir):
                os.makedirs(out_path_dir)

            generator = ModuleGenerator(mod_path, out_path_dir, self.parser_mode, self.input_root_dir)
            generator.generate_modules()

    def parse_subproject(self):
        self.golang_subprojects = list(filter(lambda module:
                                              len([dI for dI in os.listdir(module)
                                                   if os.path.isdir(os.path.join(module, dI))]) != 0,
                                              self.module_list))

        for subproj_path in self.golang_subprojects:
            out_path_dir = self.output_path + os.sep + os.path.basename(subproj_path)

            if not os.path.exists(out_path_dir):
                os.makedirs(out_path_dir)

            generator = ProjectGenerator(subproj_path, out_path_dir, self.parser_mode, self.input_root_dir)
            if len(generator.golang_files) > 0:
                generator.generate_main()

    def generate_main(self):
        self.parse_modules()
        self.parse_subproject()

        path = self.template_path + "project_template.html"

        template = os.path.normpath(path)
        gen_file = open(template, encoding='utf-8', mode="r")
        content = gen_file.read()

        template_split = content.split("Insert_here_0")
        gen_file.close()

        result = open(self.output_path +
                      "/index_" + os.path.basename(self.output_path) + "_go.html", encoding='utf-8', mode="w")

        result.write(template_split[0] +
            '''<a href="''' + self.input_root_dir + "/index_" + self.parser_mode + "_go.html" +
            '''" class="btn btn-info float-right" role="button">Return to the main page</a><h2>
            <code class="container-fluid">''' + self.html_helper.generate_breadcrumb(self) + '''</code>''')
        if os.path.basename(self.input_path) == self.parser_mode:
            result.write("""<strong class="text-success"><br /> Project:"""
                         + os.path.basename(self.output_path) + """ <br /></strong>
            </h2>""")
        else:
            result.write("""<strong class="text-success"><br /> Directory:"""
                         + os.path.basename(self.output_path) + """ <br /></strong>
            </h2>""")

        if self.golang_files:
            result.write('''
            <div class="card mb-3">
                <div class="card-header">
                    <span>
                        <h2>Content:</h2><br />
                    </span>''')

            content = ''

            for root, directories, files in os.walk(self.input_path):
                depth = root.replace(self.output_path, '').count(os.sep)
                shift_dir = " &emsp;" * depth
                files = list(filter(lambda file: file.endswith(".go"), files))
                path = self.output_path + root[root.find(self.input_path) + len(self.input_path):]

                if directories or files:
                    if os.path.exists(path + os.sep + "index_" + \
                                      os.path.basename(path) + "_go.html"):
                        content = content + '<a href="' + \
                                  path + os.sep + "index_" + \
                                  os.path.basename(path) + "_go.html" + '">' + \
                                  shift_dir + os.path.basename(root) + '<br /></a>'
                        shift_file = " &emsp; " * (depth + 1)
                        for file in files:
                            content = content + '<a href="' + path + os.sep + file[:-3] + ".html" \
                                      + '">' + shift_file + file[:-3] + ".html" + '<br /></a>'

            result.write(content)
            result.write('''</div></div>''')

        result.close()

        self.html_helper.generate_alphabetical_index(self.output_path)

        result = open(self.output_path +
                      "/index_" + os.path.basename(self.output_path) + "_go.html", encoding='utf-8', mode="a")

        result.write(template_split[1])
        result.close()
