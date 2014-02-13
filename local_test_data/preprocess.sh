sed "/^#.*$/d" "$1" | grep "[0-9]\+" -o | sort -n -u > tmp 
sed "/^#.*$/d" < "$1" >> tmp
sort -k1 -n < tmp | python preprocess.py > "$2"
rm -f tmp
