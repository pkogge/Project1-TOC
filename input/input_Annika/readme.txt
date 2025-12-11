Input File Explanation - Annika Svensson

Added Test Files: 
1n0n1n.csv
•	I added this file because it is a DTM and it is an interesting case as it cannot be recognized by a PDA or a FA
•	I created this test file on my own and plugged it into TMsim to check it
•	I tested '101' which accepted in 8 steps
•	I tested ‘101101’ which rejects in 7 steps
2x1as0s.csv
•	I chose to use this one because it had way more steps then 1n0n1n
•	I used my own work from hw9
•	I tested '$110000' which accepted in 34 steps
•	I tested '$1100001' which rejects in 49 steps
•	I tested many more too
•	I created this test file on my own and plugged it into TMsim to check it
composite_test.csv 
•	I tested this because this is NDA
•	I wanted a NDA to check if my code found all the transitions one can go down at each level and properly printed out the possible configurations.
•	I wanted to test that the number of levels was different that the number of transitions. This worked!
•	I created this test file on my own and plugged it into TMsim to check it 
•	My repo that I forked did not have any composite test
•	I tested this with '111111' which accepted in 27 steps and 102 transitions.
•	I tested this with ‘11111’ which rejected in 24 steps and 64 transitions.
•	I tested many more strings.
DTM_OpowerN.csv
•	I used this one from the TMsim
•	I used this because it was readily available 
•	I tested it with ‘00’ and it accepted in 7 steps
•	I tested it with '000' and it rejected in 4 steps
eqABC.csv
•	I added this file because it is a DTM
•	I used my work from hw9
•	I wanted to create DTMs so it could easily test my code. This simpler to test as the number of levels equals the number of number of transition explored.
•	I tested my code with ‘$aaabcbcbc’ with a max depth of 100, it stopped the execution because it reached 100 levels before reaching a accept or reject state. This was consistent with the TM when I put it into TMsim.
•	I tested it with ‘$bcacba’ and it accepted in 57 steps
•	I tested it with '$bcacbaaaaaa' and it rejected in 69 steps
Class Tests Uses:
aplus
•	I wanted to test another NTM
•	I tried many different strings
•	I tried ‘aaaaaa’ which accepted in 7 steps, 13 transitions
•	I tried ‘aaaaaaaaaaaaannika’ which rejected in 13 step and 26 transitions
Palindrome
•	I wanted another NTM
•	I tried many different strings
•	I tried ‘abba’ which accepted in 2 steps, 5 transitions
•	I tried ‘ab’ which accepted. I believe the is something wrong with the test provided because it also does not work in the TMsim