#!/bin/bash
# By guofeng.li @ 08/04/2022

#change LOG_FILE to your log file
LOG_FILE="log/control.log.INFO.20220407-104449.9422"

#1 only support a whole word,multiple words like "after ramp filter steer angle" is wrong.
#2 make sure how many times did the word appear in one circle, means appear different times in log file.
#3 you can analysis one or several words once.
WORDS=(
  # longitude
  #"path_remain"
  "target_speed"
  "curr_station"
  "target_station"
  #"speed_error"
  "diastance_error"
  "current_acc"
  "current_calc_throttle"
  "current_calac_brake"

  # lateral
  #"curr_steer"
)

[ ! -d data ] && mkdir data
save_name="data/$(date -u +"%Y%m%d-%H%M%S").csv"
touch ${save_name}

#print every result of every command executed after "set -x"
#set -x

#test command in console is:
#egrep -o 'current_acc: -*[[:digit:]]{1,}\.[[:digit:]]{1,}' log/control.log.INFO.20220407-104449.9422 | 
#     egrep -o '\-*[[:digit:]]{1,}\.[[:digit:]]{1,}'
#command explain:'current_acc: -*[[:digit:]]{1,}\.[[:digit:]]{1,}'表示一个字符串，以“urrent_acc: ”开头，负号-的个数>=0，紧接着数字的个数>=1，再接1个小数点.，在接数字的个数>=1
#reference url: https://www.cyberciti.biz/faq/grep-regular-expressions/
for word in "${WORDS[@]}"; do
  egrep -o "${word}: -*"'[[:digit:]]{1,}\.[[:digit:]]{1,}' ${LOG_FILE} \
      | egrep -o '\-*[[:digit:]]{1,}\.[[:digit:]]{1,}' \
      | awk -va=${word} 'BEGIN{print a}; {print $1}' \
      | paste -d, ${save_name} - > .tmp && cp .tmp ${save_name}
done

ln -sf data/${save_name} DATA.csv
[ -f .tmp ] && rm -f .tmp

