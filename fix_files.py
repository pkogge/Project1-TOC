#!/usr/bin/env python3
def convert_cnf_csv_format(input_path, output_path):
    """
    Convert a CNF-like CSV file so that lines beginning with 'c' or 'p'
    use spaces instead of commas, while leaving all other lines unchanged.
    """

    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        max = 151
        curr = 0

        for line in infile:
            stripped = line.lstrip()

            # If line starts with 'c' or 'p', replace commas with spaces
            if stripped.startswith("c") or stripped.startswith("p"):
                curr += 1
                if curr == max:
                    break

                new_line = line.replace(",", " ")
                outfile.write(new_line)
            else:
                # Otherwise leave the clause lines unchanged
                outfile.write(line)



if __name__ == "__main__":
    input_file = "2SAT.cnf"        # ← your actual file
    output_file = "testSAT.cnf"   # ← output file to write

    convert_cnf_csv_format(input_file, output_file)
    print("Conversion complete.")