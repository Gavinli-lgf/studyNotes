#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By guofeng.li @ 10/03/2022

import os
import matplotlib
import matplotlib.pyplot as plt
import statistics
import math
import pandas


def AnalyseControlMain():
    test_ = 0
  
    #get file list in file directory,and sorting in alphabetical order by file name
    path_ = './input_csv/'
    file_names_ = [f for f in os.listdir(path_)]
    file_names_.sort()

    out_path_ = './output_file/'

    steer_files_ = []
    speed_files_ = []
    mpc_files_ = []

    for f in file_names_:
        if 'steer' in f:
            steer_files_.append(f)
        elif 'speed' in f:
            speed_files_.append(f)
        elif 'mpc' in f:
            mpc_files_.append(f)
    
    if test_ == 0:
        if len(steer_files_) == len(speed_files_):
            for i in range(len(steer_files_)):
                matplotlib.rcParams['figure.figsize'] = [20, 10]
                fig, axs = plt.subplots(nrows=3, ncols=2)
                #The order of sterr files and speed files are the same according to file name
                AnalysisLqr(path_ +steer_files_[i],axs)
                AnalysisPid(path_ +speed_files_[i],axs)
                name = out_path_ + steer_files_[i] + '.jpg'
                plt.savefig(name)
    else:
       for i in range(len(mpc_files_)):
            AnalysisMpc(path_ +mpc_files_[i])
            name = out_path_ + mpc_files_[i] + '.jpg'
            plt.savefig(name)
            

def AnalysisLqr(name,axs):
    col_list_ = [" time"," x"," y"," lateral_evaluation"," heading_evaluation"," expected_x"," expected_y"]
    lqr_data_ = pandas.read_csv(name, usecols=col_list_)
    time_ = lqr_data_[" time"]
    real_x_ = lqr_data_[" x"]
    real_y_ = lqr_data_[" y"]
    lateral_ = lqr_data_[" lateral_evaluation"]
    heading_ = lqr_data_[" heading_evaluation"]
    expect_x_ = lqr_data_[" expected_x"]
    expect_y_ = lqr_data_[" expected_y"]
    
    #plot trajectory and expected (note Offset notation and scientific notation on the graph)
    axs[0][0].plot(real_x_,real_y_,"b-",label='real pos')
    axs[0][0].plot(expect_x_,expect_y_,"r-",label='taget pos')
    axs[0][0].ticklabel_format(axis="both", style="scientific", scilimits=(0,0),useOffset=False)
    axs[0][0].legend()
    axs[0][0].set_xlabel('X [m]')
    axs[0][0].set_ylabel('Y [m]')
    axs[0][0].grid(True)

    #plot lateral error
    ax3_twin_ = axs[1][0].twinx()
    time_ = time_ - time_[0]
    p1_,  = axs[1][0].plot(time_,lateral_,"b-",label='Lat')
    p2_,  = ax3_twin_.plot(time_,heading_,"r-",label='Head')
    axs[1][0].legend(handles=[p1_,p2_])
    axs[1][0].set_xlabel('time [s]')
    axs[1][0].set_ylabel('Lateral Error [m]')
    ax3_twin_.set_ylabel('Heading Error [rad]')
    axs[1][0].grid(True)

    #calc numerical evaluation index
    lateral_threshold_ = [0.05, 0.1, 0.2, 0.3]
    lat_mean_ = lateral_.mean()
    lat_rms_ = math.sqrt(sum([x**2 for x in lateral_]) / len(lateral_))
    lat_min_ = lateral_.min()
    lat_max_ = lateral_.max()
    lat_ratio_ = AnalysisArray(lateral_, lateral_threshold_)
    
    heading_threshold_ = [0.05, 0.1, 0.2, 0.3]
    head_mean_ = heading_.mean()
    head_rms_ = math.sqrt(sum([x**2 for x in heading_]) / len(heading_))
    head_min_ = heading_.min()
    head_max_ = heading_.max()
    head_ratio_ = AnalysisArray(heading_, heading_threshold_)

    #show numerical evaluation index in ax5
    axs[2][0].axis('off')
    str_show_ = []
    str_show_.append('Lat error detail:')
    str_show_.append('lat min: ' + str(lat_min_) + 'm')
    str_show_.append('lat max: ' + str(lat_max_) + 'm')
    str_show_.append('lat mean: ' + str(lat_mean_) + 'm')
    str_show_.append('lat rms: ' + str(lat_rms_) + 'm')
    for val_,threshold_ in zip(lat_ratio_, lateral_threshold_):
        str_show_.append(str(val_ * 100) + '% < ' + str(threshold_) + 'm')

    #in ax5,the value range of axe x and y are both 0~1.
    pos_x_ = 0
    pos_y_ = 1
    delta_y_ = 1/len(str_show_)
    for line in str_show_:
        pos_y_ -= delta_y_
        axs[2][0].text(pos_x_,pos_y_,line)

    str_show_ = []
    str_show_.append('Head error detail:')
    str_show_.append('head min: ' + str(head_min_) + 'rad')
    str_show_.append('head max: ' + str(head_max_) + 'rad')
    str_show_.append('head mean: ' + str(head_mean_) + 'rad')
    str_show_.append('head rms: ' + str(head_rms_) + 'rad')
    for val_,threshold_ in zip(head_ratio_, heading_threshold_):
        str_show_.append(str(val_ * 100) + '% < ' + str(threshold_) + 'rad')

    pos_x_ = 0.5
    pos_y_ = 1
    for line in str_show_:
        pos_y_ -= delta_y_
        axs[2][0].text(pos_x_,pos_y_,line)


def AnalysisPid(name,axs):
    col_list_ = ["time"," vel"," target_speed"," speed_error"]
    pid_data_ = pandas.read_csv(name, usecols=col_list_)
    time_ = pid_data_["time"]
    vel_ = pid_data_[" vel"]
    target_ = pid_data_[" target_speed"]
    error_ = pid_data_[" speed_error"]
    time_ = time_ - time_[0]

    #plot vel and target
    axs[0][1].plot(time_,vel_,"b-",label='real vel')
    axs[0][1].plot(time_,target_,"r-",label='taget vel')
    axs[0][1].legend()
    axs[0][1].set_xlabel('Time [s]')
    axs[0][1].set_ylabel('Velocity [m/s]')
    axs[0][1].grid(True)

    #plot error
    axs[1][1].plot(time_,error_,"b-")
    axs[1][1].set_xlabel('Time [s]')
    axs[1][1].set_ylabel('Vel Error [m/s]')
    axs[1][0].grid(True)

    #calc and show numerical evaluation index
    max_target_ = max(target_)
    vel_ratio_threshold_ = [0.05, 0.1, 0.15, 0.2]
    vel_threshold_ = [threshold_*max_target_ for threshold_ in vel_ratio_threshold_]
    vel_mean_ = error_.mean()
    vel_rms_ = math.sqrt(sum([x**2 for x in error_]) / len(error_))
    vel_min_ = error_.min()
    vel_max_ = error_.max()
    vel_ratio_ = AnalysisArray(error_, vel_threshold_)

    str_show_ = []
    str_show_.append('Vel error detail:')
    str_show_.append('vel min: ' + str(vel_min_) + 'm/s')
    str_show_.append('vel max: ' + str(vel_max_) + 'm/s')
    str_show_.append('vel mean: ' + str(vel_mean_) + 'm/s')
    str_show_.append('vel rms: ' + str(vel_rms_) + 'm/s')
    for val_,threshold_ in zip(vel_ratio_, vel_ratio_threshold_):
        str_show_.append(str(val_ * 100) + '% < ' + str(threshold_ * 100) + '%')

    axs[2][1].axis('off')
    pos_x_ = 0
    pos_y_ = 1
    delta_y_ = 1 / len(str_show_)
    for line in str_show_:
        pos_y_ -= delta_y_
        axs[2][1].text(pos_x_,pos_y_,line)


#The data format in mpc log file is not sure now, AnalysisArray function will be realised after the format ensured.
def AnalysisMpc(name):
    print('mpc') 


#caculate the ratio of values in one-dimensional array which less than threshold
def AnalysisArray(array, thresh):
    output_ = []
    for i in range(len(thresh)):
        output_.append(0)

    for i in range(len(thresh)):
        for val_ in array:
            if val_ < thresh[i]:
                output_[i] += 1

        output_[i] = output_[i] / len(array)
    
    return output_


if __name__ == '__main__':
    AnalyseControlMain()

