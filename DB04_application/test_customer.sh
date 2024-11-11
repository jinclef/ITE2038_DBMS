#!/bin/bash

python .\customer.py insert 9999 dblab dblab@hanyang.ac.kr password M +82 123-456-7890 -g Action Drama Romance
python .\customer.py info -a 10
python .\customer.py info -g Action
python .\customer.py info -i 9999
python .\customer.py info -n dblab
python .\customer.py update -i 9999 -m dblab@gmail.com
python .\customer.py update -i 9999 -p password dblab
python .\customer.py update -i 9999 -ph +82 010-1234-5678
python .\customer.py delete -i 9999