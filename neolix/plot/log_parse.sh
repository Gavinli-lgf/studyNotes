#!/bin/bash
# By guofeng.li @ 08/04/2022

#change LOG_FILE to your log file
LOG_FILE="control.log.INFO.20220504-110922.26363"

#1 support sectence, that is multiple words divided by space like "after ramp filter steer angle".
#2 make sure how many times did the word appear in one circle, frequency in cycle means different time index.
#3 you can analysis one or several words once.
WORDS=(
  # longitude
  #"path_remain"
  #"target_speed"
  #"curr_station"
  #target_station"
  #"speed_error"
  #"diastance_error"
  #"current_acc"
  #"current_calc_throttle"
  #"current_calac_brake"
  "chassis_speed"

  # lateral
  #"lateral_contribution"
  #"lateral_rate_contribution"
  #"heading_contribution"
  #"heading_rate_contribution"
  #"lateral_evaluation"
  #"heading_evaluation"
  "pt x"
  "pt y"

  # other test datas
  #"q[0]"
  #"q[1]"
  #"q[2]"
  #"q[3]"
  #"r[0]"
)

[ ! -d data ] && mkdir data
save_name="data/$(date -u +"%Y%m%d-%H%M%S").csv"
touch ${save_name}

#print every result of every command executed after "set -x"
set -x

#test command in console is:
#egrep -o 'current_acc: -*[[:digit:]]{1,}\.[[:digit:]]{1,}' log/control.log.INFO.20220407-104449.9422 | 
#     egrep -o '\-*[[:digit:]]{1,}\.[[:digit:]]{1,}'
#command explain:'current_acc: -*[[:digit:]]{1,}\.[[:digit:]]{1,}'表示一个字符串，以“urrent_acc: ”开头，负号‘-’的个数>=0，紧接着数字的个数>=1，再接1个小数点‘.’，在接数字的个数>=1
# 限制搜索日志的时间范围
# 限制搜索的内容
# “-v” 排除搜索中包含"control.cpp:248"与"Steer_Detail"的行
# “-o” 只显示搜索出的数字部分
# 后面2行打印到.csv文件中
#reference url: https://www.cyberciti.biz/faq/grep-regular-expressions/
for word in "${WORDS[@]}"; do
  egrep " 11:15:1" ${LOG_FILE} \
  | egrep -o "${word}: -*"'[[:digit:]]{1,}\.[[:digit:]]{1,}' \
      | egrep -o '\-*[[:digit:]]{1,}\.[[:digit:]]{1,}' \
      | awk -va="${word}" 'BEGIN{print a}; {print $1}' \
      | paste -d, ${save_name} - > .tmp && cp .tmp ${save_name}
done

ln -sf data/${save_name} DATA.csv
[ -f .tmp ] && rm -f .tmp

