import re


# Function to clean the file containing the opening lines
def pgn_to_txt(old_location, new_location):
    memory = ""
    with open(old_location, "r", encoding="utf-8") as old_file, open(new_location, 'r+', encoding="utf-8") as new_file:
        for line in old_file:
            if "[Site" not in line.strip():
                # Write the name of the white line
                if "[White" in line.strip():
                    if memory:
                        new_file.write(memory)
                        new_file.write("\n")
                        new_file.write("\n")
                        memory = ""
                    new_file.write("White: " + re.search('"([^"]*)"', line)[1].strip())
                    new_file.write("\n")
                # Write the name of the black line
                elif "[Black" in line.strip():
                    new_file.write("Black: " + re.search('"([^"]*)"', line)[1])
                    new_file.write("\n")
                elif not re.match(r"^(\n).*$", line):
                    if memory:
                        memory = memory+" "+line.strip()
                    else:
                        memory = line.strip()
        if memory:
            new_file.write(memory)
            new_file.write("\n")

# pgn_to_txt("Lines/all_lines.txt", "Lines/clean_lines.txt")


# Returns lists of 2-3 elements: name(s), line separated by commas
def read_lines(location):
    lines = []

    with open(location, "r", encoding="utf-8") as f:
        info = []
        for line in f:
            if line != "\n":
                info.append(line.strip())
            else:
                lines.append(info)
                info = []

    return lines

# print(read_lines("Lines/clean_lines.txt"))

