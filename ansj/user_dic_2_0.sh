#!/bin/bash
set -x
set -u

date +'%Y.%m.%d %H:%M:%S'
file=$1
python=$2
user_dic=./library/user/title" "./library/user/date" "./library/user/time" "./library/user/other" "./library/user/nword" "./library/user/wordd" "./library/user/nwordd
rm ${user_dic}


########################### 书名电影名
egrep -o '[《]([^《》]+)[》]' $file > temp
cat temp | awk '{print tolower($0)}' > title
sort title > temp
uniq temp > title
cat title | awk 'BEGIN{}{print $0"\ttitle\t100000"}' > ./library/user/title
rm temp title


########################### 时间
egrep -o '[0-9]+:[0-9][0-9]:[0-9][0-9]|[0-9]+:[0-9][0-9]' $file > temp
cat temp | awk '{print tolower($0)}' > time
sort time > temp
uniq temp > time
cat time | awk 'BEGIN{}{print $0"\ttime\t100000"}' > ./library/user/time
rm temp time


########################### 日期
egrep -o '[0-9]{3,4}-[0-9]+-[0-9]+' $file > temp
cat temp | awk '{print tolower($0)}' > date
sort date > temp
uniq temp > date
sed -i '1,4d' date
cat date | awk 'BEGIN{}{print $0"\tdate\t100000"}' > ./library/user/date
rm temp date


########################### 字母数字标点组合
egrep -o '[《]([^《》]+)[》]|[0-9]+:[0-9][0-9]:[0-9][0-9]|[0-9]+:[0-9][0-9]|[0-9]{3,4}-[0-9]+-[0-9]+|[0-9a-zA-Z./\-]+' $file > temp
cat temp | awk '{print tolower($0)}' > bag
sort bag > temp
uniq temp > bag
sed -i '1,39d' bag
${python} ./library/user/sep.py bag
cat other | awk 'BEGIN{}{print $0"\tother\t10"}' > ./library/user/other
cat nword | awk 'BEGIN{}{print $0"\tnword\t100"}' > ./library/user/nword
cat wordd | awk 'BEGIN{}{print $0"\twordd\t100"}' > ./library/user/wordd
cat nwordd | awk 'BEGIN{}{print $0"\tnwordd\t100"}' > ./library/user/nwordd
rm temp wordd nword nwordd other bag


########################### 生成ansj用户词典
rm ./library/user/user.dic ./library/default.dic
cat ${user_dic} > ./library/user/user.dic
cat ./library/user/default.dic ./library/user/user.dic > ./library/default.dic

date +'%Y.%m.%d %H:%M:%S'

