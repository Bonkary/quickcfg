# quickcfg
A package to easily change lines in config files.

Note: It does expect that each variable is on a line-per-line basis, as it reads in every line and parses to do the work.

## Installation:
```
git clone https://github.com/Bonkary/quickcfg.git
cd quickcfg
pipx install .
```

## Usage
### File 1: /path/to/file1.conf
```
# Old file
variable1 = value1
variable2 = value2
variable3 = value3
```
```
quickcfg /path/to/file1.conf variable2 newvalue
```
```
# New file
variable1 = value1
variable2 = newvalue
variable3 = value3
```

### File 2: /path/to/file2.conf
```
# Old file
variable1=value1
variable2=value2
variable3=value3
```

```
quickcfg /path/to/file2.conf variable3 newvalue
```
```
# New file
variable1=value1
variable2=value2
variable3=newvalue
```