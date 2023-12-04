### hcat_speed_run.py

Simple tool to quickly calculate time to crack | time to exhaustion based on hashcat's benchmark function.
* Run `hashcat -b` on the rig you want to benchmark.
* Copy-paste the output to a new file.
* Give it the password length and permutations and it will do the math!
* OR follow user prompts to benchmark your system!
  
For example, an 8 character password policy with upper, lower, alphanumeric and !@#$% symbols allowed would yield:
- 26 lowercase (a-z)
- 26 uppercase (A-Z)
- 10 digits (0-9)
- 5 symbols !@#$%

- So at the prompt enter  ` password length = 8 `
  ` permutations = 67 `

<img width="982" alt="Screen Shot 2023-12-03 at 1 34 46 AM" src="https://github.com/kali-mx/hcat_speed_run/assets/76034874/a7610ec9-78a2-412a-ad72-cb5dd83b773d">
