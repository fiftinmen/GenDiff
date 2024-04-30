
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

[View Demo](https://asciinema.org/a/fjDh58WngjdI4LxG26kBqA0Of)

-  **YAML Files**:

[View Demo](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6)

-  **Mixed JSON and YAML**:

[View Demo](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6)

-  **Nested JSONs**:

[View Demo](https://asciinema.org/a/SLyry8tqav7eSo6scsCWHHhVm)

-  **Plain Formatter**:

[View Demo](https://asciinema.org/a/rCZhbkuvZFfxOUaJUVmSQ7XFB)

-  **JSON Formatter**:

[View Demo](https://asciinema.org/a/BQ6iP4bDgIQyGWaBI2qffUOvi)

  

### Inner Data Format

The tool represents differences in dictionaries accumulated in a list. Here's an example:

```json
[
	{
		"key": "key1",
		"values": "value1",
		"status": " "
	},
	{
		"key": "key2",
		"values": {
			"old": "old_value",
			"new": "new_value"
		},
	"status": "-+"
	},
	{
		"key": "key3",
		"children": [
				{
					"key": "follow",
					"values": false,
					"status": " "
				}
			],
		"status": " "
	}
]
```
Here:
+ the *key* is a name of an object originating from source files,
+  *values* are its contents
+ and *status* is indicating it's status: whether that object was added ("+"), removed ("-"), changed ("-+") or not changed(" ").
+ In nested objects key *values* are replaced with *children* which a list of dictionaries.
+  *values* and *children* contain old and new values or/and new children, if they was changed (meaning their parent have *status* "-+").
