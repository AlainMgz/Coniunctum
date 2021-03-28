kill $(ps -x | grep python3\ web_app/web_client.py | awk 'NR==1{print $1, $10}')
kill $(ps -x | grep python3\ coniunctum.py | awk 'NR==1{print $1, $10}')
kill $(ps -x | grep python3\ server.py | awk 'NR==1{print $1, $10}')