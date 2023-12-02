### hcat_speed_run.py

Simple tool to quickly calculate time to crack | time to exhaustion based on hashcat's benchmark function.
* Run `hashcat -b` on the rig you want to benchmark.
* Copy-paste the output to a new file called data.txt
* Give it the password length and permutations and it will do the math!

For example, an 8 character password policy with upper, lower, alphanumeric and !@#$% symbols allowed would yield:
- 26 lowercase (a-z)
- 26 uppercase (A-Z)
- 10 digits (0-9)
- 5 symbols !@#$%

- So in the script edit ` password_length = 8 `
  ` total_combos = 67 `

  <img width="1147" alt="Screen Shot 2023-12-01 at 11 03 19 PM" src="https://github.com/kali-mx/hcat_speed_run/assets/76034874/6f10185c-69bb-45ea-9ea2-de034655e736">
