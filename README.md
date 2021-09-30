# Dependency-Checker
A tool to find Dependency Confusions inside a repository or an entire organization on GitHub. Provide it name of organization or repository URL and it will run checks whether the dependencies used exist in public database or not. Dependency Checker checks for valid Python (Pypi), NPM and GoLang Packages. 

`Note: The tool is still in development phase. It might generate some false positives while scanning Packages.`

![alt image](https://github.com/notmarshmllow/Dependency-Checker/blob/main/image.jpg)

<hr>

# Installation:

```
git clone https://github.com/notmarshmllow/Dependency-Checker.git
cd Dependency-Checker
python3 dependency_checker.py -h
```
<hr>

# Configuration


1. Open `cred.py` file and enter your GitHub account's email address and password in respective fields.

```
'login': 'your-github-account@email.here',                      
'password': 'your-github-account-password-here', 
```

<hr>

# Commands

# Scan files in single Repository
```
python3 dependency_checker.py -u https://github.com/notmarshmllow/nonsense
```
Note: `-u` scans only files in repository. If you want to scan files inside folders in a repository, provide URL of the destination where the files exists. 

# Scan an entire Organization

Note: Organization name should match the excat organization name on GitHub
```
python3 dependency_checker.py -org google
```

# Verbose Mode

```
python3 dependency_checker.py -org google -v
```

# Limit Pages to Scan

Limit the amount of pages to scan while scanning an entire organization. (Default: 100 Pages)

```
python3 dependency_checker.py -org google -p 20
```

# Output to a file

```
python3 dependency_checker.py -org google -v -o output.txt
```

<hr>

All developments to the tool are welcomed and highly appreciated. Please feel free to open an issue for bug fixes and new features.

Dependency Checker - Created by [@notmarshmllow](https://github.com/notmarshmllow)


