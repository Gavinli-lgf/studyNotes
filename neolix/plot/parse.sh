#!/bin/bash
# By yongcong.wang @ 30/03/2021

LOG_FILE="log/control.INFO"

WORDS=(
  # longitude
  "current_speed"
  "filted_current_speed"
  "station"
  "lateral"
  "path_remain"
  "low_speed_control"
  "target_station"
  "target_speed"
  "filted_target_speed"
  "speed_error"
  "distance_error"
  "pitch_angle_slope"
  "speed_compensation"
  "station_compensation"
  "error_limit"
  "compute_value"
  "control_value"
  "filted_control_value"
  "compensation_throttle"
  "clamp_compensation_throttle"
  "ramp_comp_throttle_brake"
  "throttle"
  "brake"
  "throttle_final"
  "brake_final"

  # lateral
  "is_current_backward"
  "steer_angle_feedbackterm"
  "steer_angle_feedforwardterm"
  "steer_angle"
  "steer_angle_final"
  "loc_x"
  "loc_y"
  "lateral_compensation"
  "current_lateral_error"
  "f_current_lateral_error"
  "ff_current_lateral_error"
  "current_curvature"
  "current_ref_heading"
  "current_heading"
  "current_heading_error"
  "heading_error_rate"
  "lateral_error_rate"
  "veh_angle"
  "lat_angle"
  "head_angle"
  "steer_angle"
)

[ ! -d data ] && mkdir data
save_name="data/$(date -u +"%Y%m%d-%H%M%S").csv"
touch ${save_name}.csv

for word in "${WORDS[@]}"; do
  grep "XXX: ${word}:" ${LOG_FILE} \
      | awk -va=${word} 'BEGIN{print a}; {print $7}' \
      | paste -d, ${save_name} - > .tmp && cp .tmp ${save_name}
done

ln -sf data/${save_name} DATA.csv
[ -f .tmp ] && rm -f .tmp

