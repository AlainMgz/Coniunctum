kill $(ps -x | grep python3\ miner.py | awk 'NR==1{print $1}') 
kill $(ps -x | grep python3\ miner.py | awk 'NR==2{print $1}') 