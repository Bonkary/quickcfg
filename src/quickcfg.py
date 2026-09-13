#!/usr/bin/env/ python3

import os
import argparse
import sys


class VariableNotFound(Exception):
    def __init__(self, var):
        super().__init__(f"Unable to find the variable: {var}")
        
class TooManyMatches(Exception):
    pass

parser = argparse.ArgumentParser(
    description="Replace lines in config files without needing to open them."
)

parser.add_argument("filepath", type=str, help="The path to the config file.")
parser.add_argument('variable', type=str, help="The variable to replace.")
parser.add_argument('value', type=str, help="The new value.")
args = parser.parse_args()

def main():
    if os.path.exists(args.filepath):
        matching = []
        with open(args.filepath, 'r+') as cfgFile:
            oldData = cfgFile.readlines()
            for line in oldData:
                if args.variable in line:
                    index = oldData.index(line)
                    oldLine = line
                    matching.append((index, line))

            if len(matching) > 1:
                for line in matching:
                    if '#' in line[1]:
                        matching.pop(line[0])
                if len(matching) > 1:
                    raise TooManyMatches()
                else:
                    oldLine = matching[-1][1]
                    index = matching[-1][0]

            if oldLine:
                if " = " in oldLine:
                    newLine = f"{args.variable} = {args.value}"
                else:
                    newLine = f"{args.variable}={args.value}"
            else:
                print("Failed to find variable")
                sys.exit(1)

        with open(args.filepath, 'w+') as cfgFile:
            newData = oldData.copy()
            newData[index] = newLine
            newData = [line+"\n" for line in newData]

            cfgFile.writelines(newData)

        with open(args.filepath, 'r') as cfgFile:
            newLines = cfgFile.readlines()
            if newLine+"\n" in newLines:
                print("Replaced successfully!")
                sys.exit(0)
                
        print("Failed to write data. Restoring previous...")
        with open(args.filepath, 'w') as cfgFile:
            cfgFile.writelines(oldData)

if __name__ == '__main__':
    main()
        