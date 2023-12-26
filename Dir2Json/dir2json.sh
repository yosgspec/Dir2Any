#! /bin/sh
# chmod 755 ./dir2json.sh
cd $(dirname $0)
python3 dir2json.py $@
