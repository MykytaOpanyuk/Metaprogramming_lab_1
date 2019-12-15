import argparse
import os
from generator.file_generator import FileGenerator
from generator.module_generator import ModuleGenerator
from generator.project_generator import ProjectGenerator

VERSION = "0.01 Rev A"

parser = argparse.ArgumentParser(description='Getting arguments for parsing Golang files/projects.')

parser.add_argument("--version",  "-v", action='version', version=VERSION)
parser.add_argument("--directory", "-d", help="Path to directory of *.go files")
parser.add_argument("--project", "-p", help="Path to project of *.go files")
parser.add_argument("--file", "-f", help="Path to *.go file")
parser.add_argument("--output", "-o", help="Path to generated HTML docs")

args = parser.parse_args()

if args.project is not None:
    if os.path.isdir(args.project):
        if args.output is not None:
            print(args.project)
            all_files = []
            for d, dirs, files in os.walk(args.project):
                for f in files:
                    all_files.append(f)
            golang_files = list(filter(lambda x: x.endswith('.go'), all_files))
            if len(golang_files) > 0:
                if os.path.isdir(args.output):
                    new_ProjectGenerator = ProjectGenerator(args.project, args.output, \
                                    os.path.basename(os.path.normpath(args.project)))
                    new_ProjectGenerator.generate_main()
                else:
                    print("Failed! Output directory doesn't exists.")
            else:
                print("Failed! Directory doesn't contain *.go files.")
        else:
            print("Failed! Output isn't set.")
    else:
        print("Failed! Argument isn't a path.")

elif args.directory is not None:
    if os.path.isdir(args.directory):
        if args.output is not None:
            print(args.directory)
            files = os.listdir(args.directory)
            golang_files = list(filter(lambda x: x.endswith('.go'), files))
            if len(golang_files) > 0:
                if os.path.isdir(args.output):
                    new_ModuleGenerator = ModuleGenerator(args.directory,
                        args.output, "module")
                    new_ModuleGenerator.generate_modules()
                else:
                    print("Failed! Output directory doesn't exists.")
            else:
                print("Failed! Directory doesn't contain *.go files.")
        else:
            print("Failed! Output isn't set.")
    else:
        print("Failed! Argument isn't a directory.")

elif args.file is not None:
    if os.path.isfile(args.file):
        if args.output is not None:
            if os.path.isdir(args.output):
                new_FileGenerator = FileGenerator(args.file, args.output, "file")
                new_FileGenerator.generate_file()
            else:
                print("Failed! Output directory doesn't exists.")
        else:
            print("Failed! Output isn't set.")
    else:
        print("Failed! Argument isn't a file.")
