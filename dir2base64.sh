#! /bin/sh
# chmod 755 ./dir2base64.sh
cd $(dirname $0)
python3 dir2base64.py $@
