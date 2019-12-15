# Metaprogramming_lab_1
Design and development of software documentation generators
Program language: Golang (Go)

USAGE: python goland_doc.py [argument] [value]
    List of arguments:
       	--version (-v): Path to directory for parsing.
       	--directory (-d) <path-to-directory> : Path to directory for parsing.
		Not recursive parsing.
       	--project (-p) <path-to-project> : Path to project for parsing.
		Recursive parsing (find *.go files using os.walk()).
       	--file (-f) <path-to-file> : Path to file for parsing.

Example:
	python goland_doc.py -p /home/mykyta/Studying/golang/example/ -o /home/mykyta/Studying/html_doc/ 
