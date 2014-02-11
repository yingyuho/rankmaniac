cat <(sed "/^#.*$/d" "$1" | grep "[0-9]\+" -o | sort -n -u) <(sed "/^#.*$/d" < "$1") |
sort -k1 -n |
python preprocess.py > "$2"
