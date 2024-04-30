### Hexlet tests and linter status:
[![Actions Status](https://github.com/fiftinmen/python-project-50/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/fiftinmen/python-project-50/actions)
[![Python CI](https://github.com/fiftinmen/python-project-50/actions/workflows/Test%20Coverage.yml/badge.svg)](https://github.com/fiftinmen/python-project-50/actions/workflows/Test%20Coverage.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/009d230b83044e6e3f00/maintainability)](https://codeclimate.com/github/fiftinmen/python-project-50/maintainability)

**Package description**

This package contains a command line (CLI) tool which compares two files and print changes made in second file. Tool supports **JSON** or **YAML/YML** formats for input files. Depending on CLI parameters, there are three output formats:

1. ***stylish*** (**default**):
    + prints all contents changed or not;
    + new values of objects or added objects are indicated with sign "+";
    + old values of rewrited objected or removed objects are indicated with sign "-";
    + nested objects arranged with intendation;
2. ***plain***:
    + prints only changes, ignoring unchanged data;
    + nested objects replacement with plain objects and new nested objects instead of plain objects are indicated both as "[complex value]";
    + prints path to changed plain objects inside nested objects as 'nested1.nested2.plain'
3. ***json***:
    + print all differences in JSON raw format.


**Installation**

To build and install the package on Windows, you can follow these instructions:

* Building and Installing and Reinstalling the Package on Windows:

```make setup```

* Building and Installing and Reinstalling the Package on Linux (tested on Ubuntu 22.04.4 LTS):

```make setup-linux```

* If poetry face problems with virtual environment, remove environments of project firstly:

```make remove-envs```

**Note**

Ensure you have **Poetry**, **Python** (from version 3.10) and the necessary dependencies installed on your system before. On Windows you may need install also **Make** to run makefile or any bash emulator like Git bash.


To install Make:

1. Install the [chocolatey](https://chocolatey.org/) package manager for Windows.

2. Run in Windows command line:
   
```choco install make```


**Usage**

1. Default usage example with stylish formatter:

```gendiff file1.json file2.json```

2. Usage with plain formatter:

```gendiff -f plain file1.yaml file2.yaml```

3. Usage with JSON formatter:

```gendiff -f json file1.json file2.yaml```

4. Help can be invoked with -h/--help option:

```gendiff -h```


**Usage demos**

1. You can use it with JSON files.

[![asciicast](https://asciinema.org/a/fjDh58WngjdI4LxG26kBqA0Of.svg)](https://asciinema.org/a/fjDh58WngjdI4LxG26kBqA0Of)

2. Also you cand use it with YAML files.

[![asciicast](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6.svg)](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6)

3. And even with JSON and YAML together.

[![asciicast](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6.svg)](https://asciinema.org/a/NNzfS2hklqB9vUaw9jMQFStj6)

4. Example of usage with nested JSONs.

[![asciicast](https://asciinema.org/a/SLyry8tqav7eSo6scsCWHHhVm.svg)](https://asciinema.org/a/SLyry8tqav7eSo6scsCWHHhVm)

5. Example of usage with plain formatter.

[![asciicast](https://asciinema.org/a/rCZhbkuvZFfxOUaJUVmSQ7XFB.svg)](https://asciinema.org/a/rCZhbkuvZFfxOUaJUVmSQ7XFB)

6. Example of usage with JSON formatter.

[![asciicast](https://asciinema.org/a/BQ6iP4bDgIQyGWaBI2qffUOvi.svg)](https://asciinema.org/a/BQ6iP4bDgIQyGWaBI2qffUOvi)


**Inner data format**

The tool represent differences in a dictionaries accumulated in a list:

```
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
        status: "-+"
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
        status: " "
    }
]
```

Here:

+ the *key* is a name of an object originating from source files,
  
+ *values* are its contents

+ and *status* is indicating it's status: whether that object was added ("+"), removed ("-"), changed ("-+") or not changed(" ").

+ In nested objects key *values* are replaced with *children* which a list of dictionaries.

+ *values* and *children* contain old and new values or/and new children, if they was changed (meaning their parent have *status* "-+").
