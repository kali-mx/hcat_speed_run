#!/usr/bin/python3

# author: Max Ahartz
# created: 12/01/2023
# hcat_speed_run.py
# create the data.txt file by first running hashcat -b on the system you want to benchmark.
# Then copy and paste the screen output to the new file.
# OR follow the user prompts to benchmark your system!

import os, sys, pyfiglet, subprocess, time, threading

class ProgressBarLoading(threading.Thread):
    def run(self):
        global stop
        global kill
        sys.stdout.flush()
        i = 0
        while not stop:
            if (i % 4) == 0:
                sys.stdout.write('\b/')
            elif (i % 4) == 1:
                sys.stdout.write('\b-')
            elif (i % 4) == 2:
                sys.stdout.write('\b\\')
            elif (i % 4) == 3:
                sys.stdout.write('\b|')

            sys.stdout.flush()
            time.sleep(0.2)
            i += 1

        if kill:
            print('\b\b\b\b ABORT!')
        else:
            print('\b\b done!')


def run_with_progress_bar():
    global stop, kill
    kill = False
    stop = False
    p = ProgressBarLoading()
    p.start()

    try:
        # Anything you want to run.
        start_time = time.time()
        print("Benchmarking your system now with hashcat -b. This will take about 8 minutes...") 
        os.system("hashcat -b >data2.txt")
        print("elapsed time:", time.time() - start_time)
        time.sleep(1)
        stop = True
    except (KeyboardInterrupt, EOFError):
        kill = True
        stop = True


myfile = 'data2.txt'

table_data = []
answers = ["Y", 'y', "yes", 'Yes']
password_length = int(input("Enter password length: "))
total_combos = int(input("Enter permutations: "))
answer = input("Benchmark now? Y/n: ")
if answer in answers:
    run_with_progress_bar()
else:
    myfile = input("Enter your existing benchmark file: ")

os.system("clear")


print("""
 _               _                               _                      _ 
| |__   ___ __ _| |_     ___ _ __   ___  ___  __| |    _ __ _   _ _ __ | |
| '_ \ / __/ _` | __|   / __| '_ \ / _ \/ _ \/ _` |   | '__| | | | '_ \| |
| | | | (_| (_| | |_    \__ \ |_) |  __/  __/ (_| |   | |  | |_| | | | |_|
|_| |_|\___\__,_|\__|___|___/ .__/ \___|\___|\__,_|___|_|   \__,_|_| |_(_)
                   |_____|  |_|                  |_____|                  

""")

def human_readable(total_variations):
    if len(str(total_variations)) == 13:
        number = str(total_variations)
        formatted_number = number[0] + "." + number[1]
        return formatted_number + " trillion."

    elif len(str(total_variations)) == 14:
        number = str(total_variations)
        formatted_number = number[0:2] + "." + number[2]
        return formatted_number + " trillion."

    elif len(str(total_variations)) == 15:
        number = str(total_variations)
        formatted_number = number[0:3] + "." + number[3]
        return formatted_number + " trillion."
    else:
        return "Bud, it's pointless. Names for numbers this big are meaningless anyway."


def math(hash_rate, hash_int, total_variations):
    if "GH/s" in hash_rate:
        GH_to_H = hash_int * 10**9
        time_to_crack = total_variations / GH_to_H

    elif "MH/s" in hash_rate:
        MH_to_H = hash_int * 10**6
        time_to_crack = total_variations / MH_to_H

    elif "kH/s" in hash_rate:
        kH_to_H = hash_int * 10**3
        time_to_crack = total_variations / kH_to_H

    else:
        Hash_per_sec = hash_int
        time_to_crack = total_variations / Hash_per_sec

    time_to_crack = round(time_to_crack, 1)
    hr_to_crack = round(time_to_crack / 3600, 1)
    days_to_crack = round(hr_to_crack / 24, 1)

    # Store data in a dictionary
    row_data = {
        "Mode": mode_number,
        "Mode Name": mode_name,
        "Hash Rate": hash_rate,
        "Time(sec)": time_to_crack,
        "Hours": hr_to_crack,
        "Days": days_to_crack,
    }

    # Append the dictionary to the list
    table_data.append(row_data)

    return table_data


total_variations = int(total_combos**password_length)
print("\n")
print(f"{password_length} character password with {total_combos} permutations:")
print(
    "Total possibilities to run is:",
    total_variations,
    "or about",
    str(human_readable(total_variations)),
    "\n",
)


with open(myfile, "r") as file:
    for _ in range(20):
        line = file.readline()
        print(line.strip())

# Open the file and iterate through lines
with open(myfile, "r") as file:

    # Print table heading
    print(
        "{:<10} {:<45} {:<25} {:<20} {:<20} {:<10}".format(
            "Mode", "Mode Name", "Hash Rate", "Time(sec)", "Hours", "Days"
        )
    )
    print("-" * 129)

    for line in file:
        # Exclude text from '[Iterations' until the end of the line
        line = line.split("[Iterations")[0].strip()

        # Check for lines containing "Hash-Mode" and extract information
        if "Hash-Mode" in line:
            parts = line.split()
            mode_number = parts[2]
            mode_name = " ".join(parts[3:])

        if "Speed.#1" in line or "Speed.#*" in line:
            parts = line.split()
            hash_rate = " ".join(parts[1:3])
            hash_int = int(float(parts[1]))
            math(hash_rate, hash_int, total_variations)


unique_modes = {}  # Dictionary to store unique 'Mode' entries with minimum 'Time(sec)'

for entry in table_data:
    mode = entry["Mode"]
    time_sec = entry["Time(sec)"]

    # If the 'Mode' is not in the dictionary or the current 'Time(sec)' is smaller, update the entry
    if mode not in unique_modes or time_sec < unique_modes[mode]["Time(sec)"]:
        unique_modes[mode] = entry


# Convert the dictionary values back to a list
table_data = list(unique_modes.values())

# Sort the table data by the "Time(sec)" key (fastest times first)
# list
sorted_table_data = sorted(table_data, key=lambda x: x["Time(sec)"])


# Print the sorted table
for row in sorted_table_data:
    print(
        "{:<10} {:<45} {:<25} {:<20} {:<20} {:<10}".format(
            row["Mode"],
            row["Mode Name"],
            row["Hash Rate"],
            row["Time(sec)"],
            row["Hours"],
            row["Days"],
        )
    )
