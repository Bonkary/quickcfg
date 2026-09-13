#!/usr/bin/env/ python3

import os
import argparse
import sys
import shutil
import subprocess


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
        matching: list[tuple[int,str]] = []
        with open(args.filepath, 'r+') as cfgFile:
            oldData = cfgFile.readlines()
            oldData = [line.replace("\n", '') for line in oldData]
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
                    oldLine = matching[-1][1].strip()
                    index = matching[-1][0]

            if oldLine:
                if " = " in oldLine:
                    newLine = f"{args.variable} = {args.value}"
                else:
                    newLine = f"{args.variable}={args.value}"
            else:
                print("Failed to find variable")
                sys.exit(1)

        if oldLine == newLine:
            print("Thats already the existing value!")
            sys.exit(1)
        
        print(f"Current line: {oldLine}")
        print(f"    New line: {newLine}")
        choice = input("Continue?(Y/n): ")
        if not choice == 'y':
            print("Exiting...")
            sys.exit(0)
        
        print("Creating backup file...")
        shutil.copy(args.filepath, args.filepath+".bak")
        
        print("Updating file...")
        with open(args.filepath, 'w+') as cfgFile:
            newData = oldData.copy()
            newData[index] = newLine
            newData = [line+"\n" for line in newData]

            cfgFile.writelines(newData)

        with open(args.filepath, 'r') as cfgFile:
            newLines = cfgFile.readlines()
            if newLine+"\n" in newLines:
                print("Replaced successfully!")
                keepBak = input("Keep the backup file?(Y/n): ")
                if not keepBak == 'y':
                    os.remove(args.filepath+'.bak')
                else:
                    print(f"Backup will remain: {args.filepath+".bak"}")
                sys.exit(0)
                
        print("Failed to replace line. Restoring previous...")
        shutil.copy(args.filepath+".bak", args.filepath)
        with open(args.filepath, 'r') as cfgFile:
            data = cfgFile.readlines()
            if oldLine in data:
                print("Restored successfully!")
            else:
                print(f"I got some really bad news... Backup seems to have failed.")
                choice = input("Would you like to open the file?(Y/n): ").lower()
                if choice == 'y':
                    subprocess.run(['sudo', 'nano', args.filepath])
                else:
                    print("Exiting...")
                    sys.exit(1)
    else:
        print("Failed to find the file.")
        sys.exit(1)

if __name__ == '__main__':
    main()
        