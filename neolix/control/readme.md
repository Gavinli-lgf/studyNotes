# control program refactoring suggestion:
## lqr_lateral_controller代码需要优化的地方
1. lqr_lateral_controller.cpp,将SteerComponentCalc()函数拆分为3部分，分别用来计算反馈量、前馈量、总的转向输入量。
2. SteerComponentCalc()中，对于steer_angle_*_contribution_这4个量的计算时机需要优化。用到时再算，用不到不算。（牵扯到倒车的一些内容）
3. lqr_lateral_controller.cpp -> GetParasFromScheduler() -> L896~L905改成if(lqr_controller_conf_.tuning_mode()){}else{GainScheduler()}的模式，即当是调试模式时，直接取forward_paras(0)，不是调试模式时再去计算。而现有逻辑不管是不是调试模式，都先按非调试模式处理一遍的逻辑是不合理的。
4. 车辆动力学模型中C<sub>r</sub>C<sub>f</sub>都是只单个轮胎的刚度，不能乘以2。
5. lqr_lateral_controller.h中定义的Config adu_data_conf_;在lqr横向控制空并没有用到，该变量可以删除（对应proto文件先留着）。
6. LqrSolver()中迭代结束条件2个:最多迭代100次 || 两次迭代结果p的差值矩阵的maxCoeff()绝对值小于eps。（确认理论上要不要矩阵delta的maxCoeff()、minCoeff()都进行判断。或者取Mtx delta = matrix_p_old - matrix_p;)
7. 

## lqr_lateral_controller理论知识需要完善的地方
1. 正向行驶、倒车行驶时的control逻辑与运算方式都是相同的吗？
2. SteerComponentCalc()中，对于倒车时，steer_angle_lateral_contribution_变量的处理原理要搞清。
3. 

## 现场调试
1. 需要在.7上为control模块录制的信息如下：nohup cyber_recorder record -c /localization/100hz/localization_pose /pnc/global_state /planning/proxy/DuDriveChassis /pnc/planning /router/routing /pnc/prediction /pnc/decision /perception/obstacles /pnc/control &
2. 需要新增的调试信息有：


control tuning说明
1. 系统无法运行问题排查
- 如果有异常确认实车版本（VCU、VCI、产出版本、地图版本要统一，测试有专门的发版checklist）
- 确认是否是稳定的产出版本(在.6与.7两个板子上，都通过“cat cyberrt/cyberrt_version”方式查看)
- 确认vcu版本与产出是否一致（可找刘迪/许京革确认）
- 地图配置
- 配置地图：恒通东侧的停车场暂时没有NDT点云地图；商量后可先使用UTM地图，使用GNSS信号进行定位数据输出。具体配置方式：改opt/conf/imu_model.yaml文件中的fuse_model，把它改成1。（#0:only ndt, 1:only gnss, 2:ndt+gnss）。只改.6板子上的就好，.7不用改。然后在.6执行"microcar start“即可。
- 拉取地图文件：地图要与实际匹配，否则无法启动车子与dv。在.7板子上用“cat adu_data/map/map.json”查看地图版本。（可找贾志杰/杨佳杰拉取地图，可找韩锐/郭晗解决具体的地图问题）
- 确认系统环境
- 通过“df -h”查看系统空间占用，如果根目录空间占用过大，系统无法正常运行。根目录“/”或者“/mnt/nvme”，任何一个使用率超过97%，都会有10%的刹车。
- 需要在.7上为control模块录制的信息如下：nohup cyber_recorder record -c /localization/100hz/localization_pose /pnc/global_state /planning/proxy/DuDriveChassis /pnc/planning /router/routing /pnc/prediction /pnc/decision /perception/obstacles /pnc/control &
- Control 配置
- 通过cyberrt/conf/control.flag 中control_enable_timer_detail=true，来显示细致的时间信息打印。
2.  横向lqr tuning
1. 更改配置
- 更改planning配置
- 配置planning发送给control的trajectory：在cyberrt/conf/planning.flag文件中增加planning_only_provide_reference_line=false时，发送参考线。（没有这一行,或者为true的情况下，默认发送实时规划线。改完记得重启planning模块。）
- 配置planning规划的速度：在cyberrt/conf/plan_config.json文件中改两个字段“max_speed、max_limit_speed”，用于设置规划时的最大车速。要保证“max_limit_speed”的数值比“max_speed”大0.5。(还有其他与规划相关的参数可以在同样的“common_config”中更改。)
- (编译前更改对应模块中的conf文件，重新编译即可；实际运行时更改对应opt/conf中的配置文件，然后重启模块即可)
2. 参考线tuning
...http://www.fzb.me/apollo/howto/how_to_tune_control_parameters.html 
- Set all elements in matrix_q to zero.
- Increase the third element of matrix_q, which defines the heading error weighting, to minimize the heading error.
- Increase the first element of matrix_q, which defines the lateral error weighting to minimize the lateral error.
 
3. 实时规划线tuning
...  
- ...
- ...
- ...
4. 纵向pid tuning
...

1. 配置
- 信号类型配置
- 文件"opt/conf/planning_research_config.json"中，更改字段“control_speed_tuning”对应的参数。"test_mode" 0：阶跃信号，1：方波信号，2：三角波信号；“start_t” 信号开始触发时间；“max_v、min_v” 方波信号时的最大速度、最小速度；“delta_t” 信号周期。
- 文件opt/conf/planning_research_config.json中，更改字段“control_path_tuning”对应的参数。
- 文件"opt/conf/control.pb.txt"中更改“lqr_lateral_controller_conf、mpc_controller_conf、lon_controller_conf“三个控制器信息。配置“use_debug_csv_file”确认是否记录csv文件。

2. 




