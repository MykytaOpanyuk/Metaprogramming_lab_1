import argparse
import os
from parser.golang_parser import GolangParser

VERSION = "pre0.1"

parser = argparse.ArgumentParser(description='Getting arguments for parsing Golang files/projects.')

parser.add_argument("--version",  "-v", action='version', version=VERSION)
parser.add_argument("--directory", "-d", help="Path to directory of *.go files")
parser.add_argument("--project", "-p", help="Path to project of *.go files")
parser.add_argument("--file", "-f", help="Path to *.go file")
parser.add_argument("--output", "-o", help="Path to generated HTML doc file")

args = parser.parse_args()

if args.project is not None:
    if os.path.isdir(args.project):
        if args.output is not None:
            print(args.project)
            all_files = []
            for d,dirs, files in os.walk(args.project):
                for f in files:
                    all_files.append(f)
            golang_files = list(filter(lambda x: x.endswith('.go'), all_files))
            index = len(golang_files)
            while index > 0:
                print(golang_files)
                """Timetable"""
                gen_file = open(args.output, encoding='utf-8', mode="w+")
                gen_file.close()
                new_parser = GolangParser(golang_files[index - 1], args.output)
                print(type(new_parser))
                new_parser.get_content()
                new_parser.parse_content()
                index = index - 1

            else:
                print("Failed! Project doesn't contain *.go files.")
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
                print(golang_files)
                """Timetable"""
                gen_file = open(args.output, encoding='utf-8', mode="w+")
                input_file = golang_files[0]
                check = GolangParser(input_file, gen_file)
                gen_file.close()
            else:
                print("Failed! Directory doesn't contain *.go files.")
        else:
            print("Failed! Output isn't set.")
    else:
        print("Failed! Argument isn't a directory.")

elif args.file is not None:
    if os.path.isfile(args.file):
        if args.output is not None:
            print(args.file)
            """Timetable"""
            gen_file = open(args.output, encoding='utf-8', mode="w+")
            gen_file.close()
        else:
            print("Failed! Output isn't set.")
    else:
        print("Failed! Argument isn't a file.")
