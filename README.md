
### Hexlet Tests and Linter Status
[![Actions Status](https://github.com/fiftinmen/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/fiftinmen/python-project-50/actions) [![Python CI](https://github.com/fiftinmen/python-project-50/actions/workflows/Test%20Coverage.yml/badge.svg)](https://github.com/fiftinmen/python-project-50/actions/workflows/Test%20Coverage.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/009d230b83044e6e3f00/maintainability)](https://codeclimate.com/github/fiftinmen/python-project-50/maintainability)

### Package Description

This package contains a command-line (CLI) tool that compares two files and prints the changes made in the second file. The tool supports JSON or YAML/YML formats for input files and offers three output formats based on CLI parameters.

### Installation

To build and install the package, follow these instructions:

-  **Windows**:

	- Run `make setup` for building, installing, and reinstalling the package.

-  **Linux** (tested on Ubuntu 22.04.4 LTS):

	- Execute `make setup-linux` for the same tasks.

- If Poetry faces issues with the virtual environment, remove the project environments using `make remove-envs`.

  

### Usage

1.  **Default Usage Example with Stylish Formatter**:

`gendiff file1.json file2.json`

2.  **Usage with Plain Formatter**:

`gendiff -f plain file1.yaml file2.yaml`

3.  **Usage with JSON Formatter**:

`gendiff -f json file1.json file2.yaml`

4.  **Help Command**:

`gendiff -h`

### Usage Demos

-  **JSON Files**:

[![asciicast](https://asciinema.org/a/fjDh58WngjdI4LxG26kBqA0Of.svg)](https://asciinema.org/a/fjDh58WngjdI4LxG26kBqA0Of)

-  **YAML Files**:

[![asciicast](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6.svg)](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6)

-  **Mixed JSON and YAML**:

[![asciicast](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6.svg)](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6)

-  **Nested JSONs**:

[![asciicast](https://asciinema.org/a/SLyry8tqav7eSo6scsCWHHhVm.svg)](https://asciinema.org/a/SLyry8tqav7eSo6scsCWHHhVm)


-  **Plain Formatter**:

[![asciicast](https://asciinema.org/a/rCZhbkuvZFfxOUaJUVmSQ7XFB.svg)](https://asciinema.org/a/rCZhbkuvZFfxOUaJUVmSQ7XFB)

-  **JSON Formatter**:

[![asciicast](https://asciinema.org/a/BQ6iP4bDgIQyGWaBI2qffUOvi.svg)](https://asciinema.org/a/BQ6iP4bDgIQyGWaBI2qffUOvi)

  

### Inner Data Format

The tool represents differences in dictionaries accumulated in a list. Here's an example:

```json
[{
    "key": "common",
    "status": "nested",
    "children": [{
        "key": "follow",
        "status": "added",
        "values": false,
        "type": "simple"
    }, {
        "key": "setting1",
        "status": "unchanged",
        "values": "Value 1",
        "type": "simple"
    }, {
        "key": "setting2",
        "status": "removed",
        "values": 200,
        "type": "simple"
    }, {
        "key": "setting3",
        "status": "updated",
        "old_value": true,
        "new_value": {
            "key": "value"
        },
        "old_type": "simple",
        "new_type": "complex"
    }],
    "type: "diff"
}]
```
Here:
+ the *key* is a name of an object originating from source files,
+  *values* are contents of plain objects and *children* are contents of nested objects,
+  unchanged type of updated nested objects indicated with *nested status*,
+  type (old_type or new_type) indicate whether the value is of simple type (string, number, etc.), complex type (dictionary) or diff.
