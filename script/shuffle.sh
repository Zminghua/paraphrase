
file=$1
awk 'BEGIN{ 100000*srand();}{ printf "%s %s\n", rand(), $0}'  $file |sort -k1n | awk '{gsub($1FS,""); print $0}'

