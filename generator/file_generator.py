from parser.golang_parser import GolangParser
from .generator_helper import GeneratorHelper
import os
import re
import ntpath


class FileGenerator:

    def __init__(self, input_path, output_path, mode):
        self.parser_mode = mode
        self.input_path = os.path.normpath(input_path)
        self.output_path = os.path.normpath(output_path)
        self.html_breadcrumb = GeneratorHelper(input_path, output_path, self.parser_mode)
        self.parser = GolangParser(self.input_path)

        self.my_path = os.path.abspath(os.path.dirname(__file__))
        self.template_path = os.path.join(self.my_path, "../templates/")

        self.generate_file()

    def generate_file(self):
        path = self.template_path + "file_template.html"
        template_content = self.get_template(path)

        template_split = re.split("Insert_here_0|Insert_here_1|Insert_here_2", template_content)

        output_file = self.output_path + "/" + ntpath.basename(self.input_path)[:-3] + ".html"
        result = open(output_file, encoding='utf-8', mode="a+")

        if self.parser_mode == "file":
            result.write(template_split[0])
        else:
            result.write('<div class="container">')

        result.write("""<br />""" + """<div strong class="text-primary">""" +
                     self.parser.first_comment + """</div>""" + template_split[1] +
                     """<code>""" + self.html_breadcrumb.generate_breadcrumb + """</code>
                                <div class="text-primary">File: </div>""" +
                     """ <div class="text-success">""" + self.parser.package.package_body + """</div>
                            <span class="text-muted">""" + self.parser.package.package_comment + """</span>"""
                     + template_split[2] + """        
                            </div>
                        </div>""")
        result.close()

        self.generate_imports()
        self.generate_types()
        self.generate_const()
        self.generate_variables()
        self.generate_functions()

    def generate_imports(self):
        path = self.template_path + "imports_template.html"
        template_content = self.get_template(path)
        template_split = re.split('Insert_here_0|Insert_here_1|Insert_here_2|Insert_here_3', template_content)

        output_file = self.output_path + "/" + ntpath.basename(self.input_path)[:-3] + ".html"
        result = open(output_file, encoding='utf-8', mode="a+")

        result.write(template_split[0])

        for import_ in self.parser.imports:
            result.write(template_split[1] + """
                            <code>
                                 <span class="text-primary">""" + import_.import_body + """</span>
                            </code>
                        """ + template_split[2] +
                         ("<code>{}</code>".format(import_.import_comment) if import_.import_comment else """
                            <div class="text-muted">
                                No comments available
                            </div>""") + template_split[3] +
                         """
                            <div class="card-footer text-muted font-italic">
                                 <small> Located: """ + self.input_path + """ : """ + str(import_.start_line) + """</small>
                            </div> """)

        result.write(template_split[4])

        result.close()

    def generate_variables(self):
        path = self.template_path + "variables_template.html"
        template_content = self.get_template(path)
        template_split = re.split('Insert_here_0|Insert_here_1|Insert_here_2|Insert_here_3', template_content)

        output_file = self.output_path + "/" + ntpath.basename(self.input_path)[:-3] + ".html"
        result = open(output_file, encoding='utf-8', mode="a+")

        result.write(template_split[0])

        for variable in self.parser.variables:
            result.write(template_split[1] + """
                             <code>
                                 <span class="text-primary">""" + variable.object_body + """</span>
                            </code>
                        """ + template_split[2] +
                         ("<code>{}</code>".format(variable.object_comment) if variable.object_comment else """
                            <div class="text-muted">
                                No comments available
                            </div>""") + template_split[3] +
                         """
                             <div class="card-footer text-muted font-italic">
                                 <small> Located: """ + self.input_path + """ : """ + str(variable.start_line) + """</small>
                            </div> """)

        result.write(template_split[4])

        result.close()

    def generate_const(self):
        path = self.template_path + "const_template.html"
        template_content = self.get_template(path)
        template_split = re.split('Insert_here_0|Insert_here_1|Insert_here_2|Insert_here_3', template_content)

        output_file = self.output_path + "/" + ntpath.basename(self.input_path)[:-3] + ".html"
        result = open(output_file, encoding='utf-8', mode="a+")

        result.write(template_split[0])

        for const_ in self.parser.const:
            result.write(template_split[1] + """ <code>
                        <span class="text-primary">""" + const_.object_body + """</span>
                    </code>
                    """ + template_split[2] +
                         ("<code>{}</code>".format(const_.object_comment) if const_.object_comment else """
                        <div class="text-muted">
                            No comments available
                        </div>""") + template_split[3] +
                         """
                        <div class="card-footer text-muted font-italic">
                            <small> Located: """ + self.input_path + """ : """ + str(const_.start_line) + """</small>
                        </div> """)

        result.write(template_split[4])

        result.close()

    def generate_types(self):
        path = self.template_path + "types_template.html"
        template_content = self.get_template(path)
        template_split = re.split('Insert_here_0|Insert_here_1|Insert_here_2|Insert_here_3', template_content)

        output_file = self.output_path + "/" + ntpath.basename(self.input_path)[:-3] + ".html"
        result = open(output_file, encoding='utf-8', mode="a+")

        result.write(template_split[0])

        for type_ in self.parser.types:
            result.write(template_split[1] + """
                    <code>
                        <span class="text-primary">""" + type_.name + """</span>
                        <span class="text-success">""" + ', '.join(type_.object_type) + """</span>
                    </code>
                """ + template_split[2] +
                         ("<code>{}</code>".format(type_.object_comment)
                          if type_.object_comment else """
                    <div class="text-muted">
                        No comments available
                    </div>""") + template_split[3] +
                         """
                    <div class="card-footer text-muted font-italic">
                        <small> Located: """ + self.input_path + """ : """
                         + str(type_.start_line) + """</small>
                    </div> """)

        result.write(template_split[4])

        result.close()

    def generate_functions(self):
        path = self.template_path + "functions_template.html"
        template_content = self.get_template(path)
        template_split = re.split('Insert_here_0|Insert_here_1|Insert_here_2|Insert_here_3', template_content)

        output_file = self.output_path + "/" + ntpath.basename(self.input_path)[:-3] + ".html"
        result = open(output_file, encoding='utf-8', mode="a+")

        result.write(template_split[0])

        for function in self.parser.functions:
            result.write(template_split[1] + """
                        <span class="text-primary">""" + function.func_name + """</span>
                        <span class="text-success">Inputs:""" + ', '.join(function.inputs) + """</span>
                        <span class="text-success">Returns:""" + ', '.join(function.returns) + """</span>
                """ + template_split[2] +
                         ("<code>{}</code>".format(function.object_comment) if function.object_comment else """
                    <div class="text-muted">
                        No comments available
                    </div>""") + template_split[3] +
                         """
                    <div class="card-footer text-muted font-italic">
                        <small> Located: """ + self.input_path + """ : """ + str(function.start_line) + """</small>
                    </div> """)

        result.write(template_split[4])

        result.close()

    @staticmethod
    def get_template(template):
        template = os.path.normpath(template)
        gen_file = open(template, encoding='utf-8', mode="r")
        content = gen_file.read()

        return content
