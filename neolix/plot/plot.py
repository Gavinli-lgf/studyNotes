#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By yongcong.wang @ 31/03/2021

import pandas as pd
import matplotlib.pyplot as plt
import math


def fill_err(data, ref):
    # first point
    x = data.at[0, "loc_x"]
    y = data.at[0, "loc_y"]
    #print(data["loc_x"])
    min_val = 1000
    min_idx = 0
    for i in range(len(ref)):
        ref_x = ref.at[i, "ref_x"]
        ref_y = ref.at[i, "ref_y"]
        curr_val = math.sqrt((ref_x - x)**2 + (ref_y - y)**2)
        if curr_val < min_val:
            min_val = curr_val
            min_idx = i
    #print("curr_x: ", x, "curr_y: ", y, "min_val: ", min_val, "min_idx: ", min_idx)

    # others
    size = len(ref)
    lat_err = []
    for i in range(len(data)):
        start_idx = min_idx - 5
        end_idx = min_idx + 5
        #print("start: ", start_idx, "end: ", end_idx)

        curr_x = data.at[i, "loc_x"]
        curr_y = data.at[i, "loc_y"]
        #print("curr_x: ", curr_x, "curr_y: ", curr_y)

        for j in range(start_idx, end_idx):
            idx = (j + size) % size
            ref_x = ref.at[idx, "ref_x"]
            ref_y = ref.at[idx, "ref_y"]
            curr_val = math.sqrt((ref_x - curr_x)**2 + (ref_y - curr_y)**2)
            if curr_val < min_val:
                min_val = curr_val
                min_idx = j
        lat_err.append(min_val)
        min_val = 1000

    data.insert(len(data.columns), 'lat_err', lat_err)
    #print("lat_size:", len(lat_err))


def plot_longitude(data):
    lon_list = [
      "current_speed",
      #"filted_current_speed",
      #"station",
      #"lateral",
      #"path_remain",
      #"low_speed_control",
      #"target_station",
      "target_speed",
      #"filted_target_speed",
      #"speed_error",
      #"distance_error",
      #"pitch_angle_slope",
      #"speed_compensation",
      #"station_compensation",
      #"error_limit",
      #"compute_value",
      #"control_value",
      #"filted_control_value",
      #"compensation_throttle",
      #"clamp_compensation_throttle",
      #"ramp_comp_throttle",
      #"throttle",
      #"brake",
      #"throttle_final",
      #"brake_final",
    ]
    data.plot(y=lon_list)
    plt.show()


def plot_lateral(data):
    lat_list = [
    "is_current_backward",
    "steer_angle_feedbackterm",
    "steer_angle_feedforwardterm",
    #"steer_angle",
    #"steer_angle_final",
    #"lateral_compensation",
    #"current_lateral_error",
    #"f_current_lateral_error",
    #"ff_current_lateral_error",
    #"current_curvature",
    #"current_ref_heading",
    #"current_heading",
    #"current_heading_error",
    #"heading_error_rate",
    #"lateral_error_rate",
    ]
    #ref = pd.read_csv("./ref_line.csv").drop(
    #        labels=range(203), axis=0).reset_index(drop=True)
    #error = pd.concat([data, ref], axis=1)
    #ax = error.plot(x="loc_x", y="loc_y")
    #ax = error.plot(x="ref_x", y="ref_y", ax=ax)
    #plt.show()

    fill_err(data, ref)

    data.plot(y=lat_list)
    plt.show()
    lat_err = data["lat_err"][400:8360]
    print("max_err:", lat_err.max())
    print("less than 0.2 percent: ",
          lat_err.between(-0.2, 0.2).sum() / lat_err.count())
    print("less than 0.3 percent: ",
          lat_err.between(-0.3, 0.3).sum() / lat_err.count())


def main():
    #data = pd.read_csv("./DATA.csv")
    data = pd.read_csv("./data/20220407-080101.csv")
    #plot_longitude(data)
    plot_lateral(data)


main()
