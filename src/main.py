import argparse
import sys
import os 
from lexer import lex
from parser import parse
from interpreter import interpret

def run_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    tokens = lex(code) 
    ast = parse(tokens) 
    interpret(ast)      

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to the .ev file")
    args = parser.parse_args()
    run_file(args.file)
