#!/usr/bin/python3

#author: Max Ahartz
#created: 12/01/2023

#create the data.txt file by first running hashcat -b on the system you want to benchmark.  
#Then copy and paste the screen output to the new file.

password_length = 7 #CHANGE THIS!
total_combos = 62   #CHANGE THIS!

myfile = 'data.txt'
table_data = []

import os, sys, pyfiglet 
from datetime import datetime
os.system("clear")

banner = pyfiglet.figlet_format("Hcat_speed_run!")
print(banner)
print("python version:", sys.version)
current_date = datetime.now()
print(current_date)
date = datetime.today().strftime("%Y-%m-%d")

def human_readable(total_variations):
    if len(str(total_variations)) == 13:
        number = str(total_variations)
        formatted_number = number[0] + '.' + number[1]
        return formatted_number + " trillion."

    elif len(str(total_variations)) == 14:
        number = str(total_variations)
        formatted_number = number[0:2] + '.' + number[2]
        return formatted_number + " trillion." 

    elif len(str(total_variations)) == 15:
        number = str(total_variations)
        formatted_number = number[0:3] + '.' + number[3]
        return formatted_number + " trillion."
    else:
        return "Bud, it's pointless. You won't be alive to see it with today's current compute power."


total_variations = int(total_combos ** password_length)
print('\n')
print(f"{password_length} character password with {total_combos} permutations:")
print("Total possibilities to run is:",total_variations, 'or about', str(human_readable(total_variations)),'\n')

with open(myfile, 'r') as file:
    for _ in range(20):
        line = file.readline()
        print(line.strip()) 

# Open the file and iterate through lines
with open(myfile, 'r') as file:
  
  # Print table heading
    print("{:<10} {:<45} {:<25} {:<20} {:<20} {:<10}".format("Mode", "Mode Name", "Hash Rate", "Time(sec)", "Hours", "Days"))
    print("-" * 129)

    for line in file:
        # Exclude text from '[Iterations' until the end of the line
        line = line.split('[Iterations')[0].strip()
        # Check for lines containing "Hash-Mode" and extract information
        if "Hash-Mode" in line:
            parts = line.split()
            mode_number = parts[2]
            mode_name = " ".join(parts[3:])
        elif "Speed.#1" in line:
            parts = line.split()
            hash_rate = " ".join(parts[1:3])
            hash_int = float(parts[1])
            

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

            time_to_crack = round(time_to_crack)
            hr_to_crack = round(time_to_crack/3600)
            days_to_crack = round(hr_to_crack/24)
           
            #print("{:<10} {:<45} {:<25} {:<20} {:<20} {:<20}".format(mode_number, mode_name, hash_rate, time_to_crack, hr_to_crack, days_to_crack))
            
             # Store data in a dictionary
            row_data = {
                "Mode": mode_number,
                "Mode Name": mode_name,
                "Hash Rate": hash_rate,
                "Time(sec)": time_to_crack,
                "Hours": hr_to_crack,
                "Days": days_to_crack
            }

            # Append the dictionary to the list
            table_data.append(row_data)

    # Sort the table data by the "Time(sec)" key (fastest times first)
    sorted_table_data = sorted(table_data, key=lambda x: x["Time(sec)"])

    # Print the sorted table
    for row in sorted_table_data:
        print("{:<10} {:<45} {:<25} {:<20} {:<20} {:<10}".format(
            row["Mode"], row["Mode Name"], row["Hash Rate"],
            row["Time(sec)"], row["Hours"], row["Days"]
        ))
   
