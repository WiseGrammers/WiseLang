# WiseLang

WiseLang is an esoteric, compiler-based programming language inspired by Python, designed for unique computational experiments and exploration of novel programming paradigms.

## Overview

WiseLang was developed to provide an innovative approach to programming language design, combining familiar Python-like syntax with experimental features. It includes a custom compiler and core language functionalities to support such exploration.

## Features

- Python-inspired, easy-to-read syntax.
- Compiler-based implementation for efficient execution.
- Support for fundamental programming constructs with unique syntax.
- Designed for learning, experimentation, and language theory research.


## Requirements

WiseLang uses the `sly` library for lexical analysis and parsing. Install necessary dependencies with:

```
pip install -r requirements.txt
```


## Basic Syntax Examples

### Hello, World

```
// Comment lines start with //

eww "Hello, World!";  // Prints Hello, World!
```


### Variables

```
WTF a = 10;
WTF b = "variable";
```

*Note: Variable names are case-sensitive (e.g., `A` ≠ `a`).*

### Conditional Statements

```
WTF a = 10;
agar a == 10 {
    eww "a is 10";
}
nahi toh {
    eww "a is not 10";
}
```


### Control Statements

```
// Comments
c***iya; // acts as a pass or no-op statement
hatt;    // break or exit from a block
```


## Operators

### Comparison Operators

| Operator | Description | Example |
| :-- | :-- | :-- |
| == | Equal to | x == y; |
| != | Not equal to | x != y; |
| > | Greater than | x > y; |
| >= | Greater than or equal to | x >= y; |
| < | Less than | x < y; |
| <= | Less than or equal to | x <= y; |

### Arithmetic Operators

| Operator | Description | Example |
| :-- | :-- | :-- |
| + | Addition | x + y; |
| - | Subtraction | x - y; |
| * | Multiplication | x * y; |
| / | Division | x / y; |
| % | Modulus (remainder) | x % y; |

## Running the Interpreter

Run the WiseLang interpreter in standard mode:

```
python src [file]
```


### Debug Mode

Activate debug mode (for development or troubleshooting) with the `-d` flag:

```
python src -d [file]
```

If no file is provided, the interpreter starts in interactive mode.

## Additional Information

Comprehensive documentation is maintained in the project Wiki for reference on language features and usage.
