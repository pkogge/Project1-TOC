import subprocess
import os
import sys

MAIN_SCRIPT = "main.py"
TEST_DIR = "input"
TIMEOUT = 5

TEST_CASES = [
    # --- aplus.csv ---
    ("aplus.csv", "a", "accepted", "Single 'a' accepted"),
    ("aplus.csv", "aaa", "accepted", "Multiple 'a's accepted"),
    ("aplus.csv", "", "rejected", "Empty string rejected"),
    ("aplus.csv", "aab", "rejected", "String with 'b' rejected"),

    # --- ntm_n1n.csv (ZeroNOneN) ---
    ("ntm_n1n.csv", "", "accepted", "epsilon accepted"),
    ("ntm_n1n.csv", "01", "stopped", "valid but non-halting"),
    ("ntm_n1n.csv", "0011", "stopped", "valid but non-halting"),
    ("ntm_n1n.csv", "000111", "stopped", "valid but non-halting"),
    ("ntm_n1n.csv", "001", "stopped", "invalid but looping"),
    ("ntm_n1n.csv", "0101", "stopped", "invalid but looping"),
    ("ntm_n1n.csv", "11", "rejected", "immediate reject"),

    # --- equal_01s.csv ---
    ("equal_01s.csv", "01", "accepted", "Simple 01"),
    ("equal_01s.csv", "10", "accepted", "Simple 10"),
    ("equal_01s.csv", "0011", "accepted", "Nested 0011"),
    ("equal_01s.csv", "011", "rejected", "Unequal count (more 1s)"),
    ("equal_01s.csv", "00011", "rejected", "Unequal count (more 0s)"),
]

def run_test(test_num, csv_file, input_str, expected, desc):
    print(f"Test {test_num}: {desc}")

    file_path = os.path.join(TEST_DIR, csv_file)
    if not os.path.exists(file_path):
        print(f"Result: Failure (File not found: {file_path})\n")
        return False

    cmd = [sys.executable, MAIN_SCRIPT, file_path, input_str]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
        output = result.stdout + "\n" + result.stderr

        if "String accepted" in output:
            actual = "accepted"

        elif "String rejected" in output:
            actual = "rejected"

        elif "Execution stopped" in output:
            actual = "stopped"

        else:
            actual = "error"

        if actual == expected:
            print("Result: Success\n")
            return True
        
        else:
            print(f"Result: Failure (Expected {expected}, Got {actual})")
            print("---- Output ----")
            print(output.strip())
            print("---------------\n")
            return False

    except subprocess.TimeoutExpired:
        print("Result: Failure (Timeout)\n")
        return False

def main():
    passed = 0
    for i, test in enumerate(TEST_CASES, 1):
        if run_test(i, *test):
            passed += 1
    print(f"Summary: {passed}/{len(TEST_CASES)} tests passed")

if __name__ == "__main__":
    main()