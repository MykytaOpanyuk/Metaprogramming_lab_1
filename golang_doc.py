import argparse

class GolangDocGen:
    VERSION = "pre0.1"


parser = argparse.ArgumentParser(description='Getting arguments for parsing Golang files/projects.')

parser.add_argument("--version",  "-v", action='version', version=GolangDocGen.VERSION)
parser.add_argument("--directory", "-d", help="Path to directory for parsing.")
parser.add_argument("--project", "-p", help="Path to project for parsing.")
parser.add_argument("--file", "-f",  help="Path to file for parsing.")

args = parser.parse_args()

if args.project is not None:
    print(args.project)

elif args.directory is not None:
    print(args.directory)

elif args.file is not None:
    print(args.file)
