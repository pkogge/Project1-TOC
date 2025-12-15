# Turing Machine Test Files (1-Tape)

This directory contains **1-tape Turing machine definitions** written in CSV format, compatible with the provided `turing_machine.py` loader and `NTM_Tracer`.

---

## File: `an_bn_cn.csv`

### Language

L = { a^n b^n c^n | n >= 1 }


### Description

This machine decides whether the input string consists of:

* a block of `a`s
* followed by an equal-length block of `b`s
* followed by an equal-length block of `c`s

The machine uses a **three-phase marking strategy**:

* Marks one `a` as `X`
* Finds and marks a corresponding `b` as `Y`
* Finds and marks a corresponding `c` as `Z`
* Returns to the start of the tape and repeats

Once no unmarked `a` remains, the machine performs a final scan to ensure that no unmarked `b` or `c` symbols remain.

### Tape Alphabet

```
{ a, b, c, X, Y, Z, _ }
```

### Accepts

```
abc
aabbcc
aaabbbccc
```

### Rejects

```
ε
aabbc
abcc
aabbbccc
```

### Example Run

```bash
python main.py src/input/an_bn_cn.csv aabbcc --max_depth 1000
```

---

## File: `equal_0_1.csv`

### Language

L = { w in {0,1}* | #0(w) = #1(w) }


### Description

This machine decides whether a binary string contains an **equal number of `0`s and `1`s**, regardless of order.

The machine repeatedly:

* Finds an unmarked `0` and marks it as `X`
* Searches for an unmarked `1` and marks it as `Y`
* Returns to the start of the tape

If a `0` cannot find a matching `1`, or vice versa, the machine rejects.
When no unmarked symbols remain, the machine accepts.

### Tape Alphabet

```
{ 0, 1, X, Y, _ }
```

### Accepts

```
ε
01
10
0011
0101
```

### Rejects

```
0
1
00011
111
```

### Example Run

```bash
python main.py src/input/equal_0_1.csv 0101 --max_depth 300
```

---
