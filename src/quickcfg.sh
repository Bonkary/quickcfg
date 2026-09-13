#! /bin/bash

err() {
    printf "\e[31m%s\e[0m\n" "$1"
    exit 1
}

filepath=$1
phrase=$2
value=$3
newLine="$phrase=$value"

noSpace=$(cat "$filepath" | grep "$phrase=")
withSpace=$(cat "$filepath" | grep "$phrase = ")
if [[ $noSpace ]]; then
    oldLine=$noSpace
elif [[ $withSpace ]]; then
    oldLine=$withSpace
else
    err "Unable to find the phrase: $phrase"
    exit 1
fi

echo "Current line: $oldLine"
echo "    New line: $newLine"
read -r -p "Continue?(Y/n): " -n 1
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Ok"
    exit 0
fi

if [[ $filepath == *"$USER"* ]]; then
    if sed -i "/$oldLine/c\\$newLine" "$filepath"; then
        exit 1
    fi
else
    if sudo sed -i "/$oldLine/c\\$newLine" "$filepath"; then
        exit 1
    fi
fi



