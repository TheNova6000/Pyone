# Pyone  
### A Minimal English-Based DSL Interpreter

---

## 🚀 What is Pyone?

Pyone is a custom-built **Domain Specific Language (DSL) interpreter** written in Python.

It allows you to write executable programs in simple, English-like syntax — and runs them through a fully manual interpreter engine.

No `eval()`.
No shortcuts.
No cheating.

This project demonstrates how programming languages work internally:

* Parsing
* Expression evaluation
* Control flow execution
* State management
* Runtime error handling

---

## ✨ Example

```text
let x is 10
let y is 5

if x is greater than y
    print "x is bigger"
otherwise x is equals to y
    print "equal"
else
    print "y is bigger"
end
```

Run it:

```bash
python pyone.py example.pyo
```

Output:

```
x is bigger
{'x': 10, 'y': 5}
```

---

## 🧠 Core Concepts Implemented

Pyone implements fundamental interpreter architecture concepts:

### 1️⃣ Lexical Handling

* Line tokenization
* Keyword detection
* Variable name validation

### 2️⃣ Expression Preprocessing

* Converts English comparisons into operators

  * `is greater than` → `>`
  * `is equals to` → `==`
* String literal placeholder system
* Safe evaluation without Python's `eval()`

### 3️⃣ Stack-Based Expression Evaluation

* Custom operand stack
* Type-safe arithmetic
* Controlled comparison handling
* Error detection for invalid expressions

### 4️⃣ Control Flow Parsing

* `if`
* `otherwise` (elif)
* `else`
* `end`
* Block boundary resolution
* Marker scanning system

### 5️⃣ Runtime State Management

* Internal variable memory dictionary
* Redeclaration prevention
* Assignment validation

---

## 🏗 Architecture Overview

```
Source File (.pyo)
        ↓
Line Parsing
        ↓
Token Classification
        ↓
Expression Preprocessing
        ↓
Stack Evaluation Engine
        ↓
Control Flow Resolution
        ↓
Runtime Execution
        ↓
Memory State Output
```

Pyone behaves like a miniature interpreter runtime.

---

## 📦 Features

* Variable declaration
* Variable reassignment
* Integer arithmetic (+, -, *, /)
* String concatenation
* Comparison operators
* Conditional branching
* Runtime syntax errors
* Type checking
* No external dependencies

---

## 🔥 Why This Project Matters

Most students use Python.

Very few understand how Python works internally.

Pyone demonstrates:

* How interpreters manage state
* How expressions are evaluated
* How branching logic is resolved
* How runtime environments execute instructions

This is foundational computer science.

Not surface-level scripting.

---

## 📂 Project Structure

```
pyone/
│
├── pyone.py
├── example.pyo
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt
```

---

## 🛠 How to Run

1. Clone repository
2. Ensure Python 3.8+
3. Run:

```bash
python pyone.py example.pyo
```

---

## 📌 Limitations (Current Version)

* Nested `if` not supported
* No loops yet
* Only integers and strings supported
* No boolean operators (`and`, `or`)

---

## 🔮 Future Roadmap

* Nested conditional support
* Loop constructs
* Boolean logic
* Modular parser architecture
* Bytecode compilation stage
* CLI interface with flags
* Packaging as installable module

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Sri Krishna Batkeeri**


Choose your evolution.
