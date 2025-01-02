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

def process_command(command):
    if 'mean=' in command or 'median=' in command or 'mode=' in command:
        match = re.match(r"(mean|median|mode)=(\d+(\.\d+)?) for (.+)", command)
        if match:
            strategy = match.group(1)
            custom_value = match.group(2)
            columns = match.group(4).split(',') 
            columns = [col.strip().strip("'").strip('"') for col in columns] 
            data = clean_data(data, strategy=strategy, custom_value=custom_value, columns=columns)
            print(f"Applied {strategy} with custom value {custom_value} for columns {', '.join(columns)}")
        else:
            print("Invalid custom mean/median/mode command format.")
    else:
        pass
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to the .ev file")
    args = parser.parse_args()
    run_file(args.file)
