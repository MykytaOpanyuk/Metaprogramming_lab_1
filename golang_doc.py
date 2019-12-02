import argparse
import os
import glob
from typing import List, Union

VERSION = "pre0.1"

parser = argparse.ArgumentParser(description='Getting arguments for parsing Golang files/projects.')

parser.add_argument("--version",  "-v", action='version', version=VERSION)
parser.add_argument("--directory", "-d", help="Path to directory of *.go files")
parser.add_argument("--project", "-p", help="Path to project of *.go files")
parser.add_argument("--file", "-f", help="Path to *.go file")

args = parser.parse_args()

if args.project is not None:
    if os.path.isdir(args.project):
        print(args.project)
        all_files = []
        for d,dirs, files in os.walk(args.project):
            for f in files:
                all_files.append(f)
        golang_files = list(filter(lambda x: x.endswith('.py'), all_files))
        if len(golang_files) > 0:
            print(golang_files)
        else:
            print("Failed! Project doesn't contain *.go files.")
    else:
        print("Failed! Argument isn't a path.")

elif args.directory is not None:
    if os.path.isdir(args.directory):
        print(args.directory)
        files = os.listdir(args.directory)
        golang_files = list(filter(lambda x: x.endswith('.py'), files))
        if len(golang_files) > 0:
            print(golang_files)
        else:
            print("Failed! Directory doesn't contain *.go files.")
    else:
        print("Failed! Argument isn't a directory.")

elif args.file is not None:
    if os.path.isfile(args.file):
        print(args.file)
    else:
        print("Failed! Argument isn't a file.")
