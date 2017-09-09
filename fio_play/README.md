## Generator or values based on provide distribution.

Intended for generating latencies faking EBS drives
Based on ideas/code from iproute2/netem

To run:
*  Collect FIO samples for the desired distribution, with FIO '--output=json+'. This will show how the actual device works
* run `convert.sh fio_file`. This will generate **.dist** and **.stats** files with distribution information
* build (`gcc -o le le.c`) and run **le* tool , e.g. `le <dist_table> <stats> <number_of_samples>` , redirect output \<somewhere\>.
 
 this "somewhere" will have the set of samples martching the distribution. To validation, run `stats <somewhere>` and make sure the
 mean/std. deviation for generated samples matching the one in \<stats\> file.

---
 readme created: 9/9/2017
