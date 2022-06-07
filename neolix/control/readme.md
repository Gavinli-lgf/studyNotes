# control program refactoring suggestion:
## lqr_lateral_controller代码需要优化的地方
1. lqr_lateral_controller.cpp,将SteerComponentCalc()函数拆分为3部分，分别用来计算反馈量、前馈量、总的转向输入量。
2. SteerComponentCalc()中，对于steer_angle_*_contribution_这4个量的计算时机需要优化。用到时再算，用不到不算。（牵扯到倒车的一些内容）
3. lqr_lateral_controller.cpp -> GetParasFromScheduler() -> L896~L905改成if(lqr_controller_conf_.tuning_mode()){}else{GainScheduler()}的模式，即当是调试模式时，直接取forward_paras(0)，不是调试模式时再去计算。而现有逻辑不管是不是调试模式，都先按非调试模式处理一遍的逻辑是不合理的。
4. 车辆动力学模型中C<sub>r</sub>C<sub>f</sub>都是只单个轮胎的刚度，不能乘以2。
5. lqr_lateral_controller.h中定义的Config adu_data_conf_;在lqr横向控制空并没有用到，该变量可以删除（对应proto文件先留着）。
6. LqrSolver()中迭代结束条件2个:最多迭代100次 || 两次迭代结果p的差值矩阵的maxCoeff()绝对值小于eps。（确认理论上要不要矩阵delta的maxCoeff()、minCoeff()都进行判断。或者取Mtx delta = matrix_p_old - matrix_p;)
7. GetRearPos()函数与相关的变量不再使用了，也可以删除调。
8. lqr_lateral_controller_test.cpp -> 中的global_state变量可删除、对应global_state.txt文件可删除。
9. LateralAutoCompensation()实际并没有调用，是否可以删除？还涉及的相关配置、变量、函数有：lateral_error_low_threshold、lateral_error_high_threshold、lateral_error_low_threshold_、InitializeLateralCompensation()。
10. GetAbsoluteTimeLateralAndHeadingError() 中if (delta_time < 0.0) 后只保留LOG_WARN()，delta_time的计算删除。
11. StateUpdate()中，lateral_error_rate_、heading_error_rate_两者的计算可以封装为子函数。
13. “Steer_Detail, auto_mode:”的日志每10个cycle打印一次，其中大部分信息已有，这些已有的信息相互影响，不好分析；将只有此处有，其他地方没有的日志拿出来，每个cycle打印一次，此处的日志删除。（需打印的有4个steer_angle_*_contribution_变量，...）
14. 同上，“msg->ShortDebugString().c_str()”也是相同的思路。
15. 对定位信息，按"pt x" "pt y"的方式打印，不好理解。
16. 参照永聪之前分析的数据内容，没有的都加上；且注意每个日志信息的唯一性，方便搜索。
17. 合理使用好“标志位”来打印细节处的日志信息。
18. MatrixInit()中，对"matrix_a_(1, 2)"初始化时，C<sub>f</sub>与C<sub>r</sub>没有乘2，是当成2个轮胎的总刚度了。但是有的地方是当成1个轮胎的刚度算的。比如SteerComponentCalc()中，对转向率kv_的计算中，却把C<sub>f</sub>与C<sub>r</sub>乘2，当成1个车轮的刚度来处理了。（具体可以对比《车辆动力学及控制》中的公式）。应该改成与书中一致，都是1个轮胎刚度来处理。
19. MatrixInit()中，“lqr_matrix_.matrix_a_coeff_(2, 3) = 1.0;”这一行是错误的。（虽然最终将matrix_a_coeff_与matrix_a_合并时，没用到(2, 3)这个元素，但是这一行多余，应删掉。）
20. 将LqrLateralController::Control()中根据定位或chasis获取的实时车速打印到log.
21. 纵向控制GetSpeedControlRegular()中，日志“"curr_v: %.4f, target_v:”打印多次，多余了。

## lqr_lateral_controller理论知识需要完善的地方
1. 正向行驶、倒车行驶时的control逻辑与运算方式都是相同的吗？
2. SteerComponentCalc()中，对于倒车时，steer_angle_lateral_contribution_变量的处理原理要搞清。
3. 预瞄点与这个(record_x,record_y)点的0.1s的关系要搞清
4. lateral_error_rate_、heading_error_rate_两者的计算公式待搞清？...（参照代码）
5. [状态空间模型的离散化](https://www.guyuehome.com/13948)的2种方法：精确离散化方法、近似离散化方法。其中“近似离散化方法”分为3中：向前欧拉法、向后欧拉法、中点欧拉法（对应了老王视频中讲的离散化方法）。根据对状态空间方程dot{x}=Ax+Bu两边积分分别去前边界点、后边界点、中间点可得。离散化后得x(k+1)=Gx(k)+Hu(k)，（1）向前欧拉法：G = I + A * delta T, H = B * delta T;（2）...；（3）neolix中对G使用中点欧拉法，对H使用向前欧拉法。（注意称呼：是“状态空间模型的离散化”，而不是“矩阵的离散化”。）
6. 



# apollo源码解析
* [Apollo control模块横向控制原理及核心代码逐行解析](https://blog.csdn.net/weixin_39199083/article/details/122228076)

## 程序中的单位
* max_steer_angle: 6.6323  //方向盘从中间位置单向打到底，所转过的rad。和轮距一起可以用于计算max_kappa。（此外min_turn_radius也决定了max_kappa）
* 

## 程序中需要区别的量
* “车辆侧偏角”区别于“轮胎侧偏角”
* 

1. control失败，会产生什么效果？
	答：以GetAbsoluteTimeLateralAndHeadingError()为例，失败后会导致estop、hard_estop、ESTOP_CONTROLFAIL。（hard_estop:65%; soft_estop:45%;）
2. trajectory每次都是以子车位置为规划起点。（reference_line时，以routing上离ego最近的位置为规划起点）。
3. trajectory是100Hz，即使按最大7m/s算，一般trajectory的前0.7m范围内，都能找到最近点。（0.5m的预瞄，一般处理长度不会超过trajectory的前1.2m范围。）
4. trajectory是最大0.1s的周期，人眼300ms，肉眼无法识别起点与自车不重合。
5. 正常planning_time > curr_time，delta_time > 0。这个逻辑保证了预瞄点的预瞄时间是在current_time与cur_index分别对应delta_time中取的最大值。
6. 如果快到达routing终点或者其他trajectory点较少的情况，此时找预瞄点会失败。
7. 找到预瞄点后，就要计算state_matrix:
（1）lateral_error：需要5个量就能计算出来。自车位置(x,y)、预瞄点位置(x_t,y_t)、预瞄点的heading_t。通过"x, y, x_t, y_t, heading_t"这5个量可以计算出自车在sl坐标系下的横向误差lateral_error（单位:m）。
（2）heading_error：需要5个量就能计算出来。定位的姿态信息(qx,qy,qz,qw)，预瞄点的heading_t。通过"qx,qy,qz,qw,heading_t"这5个量，算出heading_error，其在FLU、ENU、SL坐标系下值都相同。（单位:rad。所以heading_error最大值不能超过0.523，因为这是前轮最大转角30度。）
（3）lateral_error_rate_：横向误差变化率，就等于当前车速在sl坐标系下，沿预瞄点l方向的投影。（因此只与2个因素有关：当前车速、朝向误差。）
（4）heading_error_rate_：横摆误差变化率，就等于“车辆自身的横摆角速度 - 道路曲率产生的横摆角速度”。（因此与3个因素有关：自车姿态信息<横摆角速度>、车速、道路曲率）。
（5）注意：这里的state是根据两个预瞄点信息混用计算出来的。这样会有问题吧？！
8. GetAbsoluteTimeLateralAndHeadingError()中预瞄时间决定了至少，预瞄点至少在最近点0.5s后；但是日志中打印的record_x,record_y,record_head，记录的是0.1s后的点，也就是说，下一次trajectory更新时，车辆应该到达的位置。
（1）所以“record_x,record_y,record_head”与预瞄点的(x,y),heading还不一样。
（2）“record_x,record_y,record_head”除了打印，并无其他作用。
9. 正常一次trajectory有400个点（20ms一个点，总时长8s。）
10. 前馈的预瞄点和反馈的预瞄点可能不一样。在车辆车辆速度<2.1，或者low_speed_control时，两者相同；其他情况下不同，前馈按照配置文件找，反馈计算而来。

## control中档位切换的逻辑整理：
搜索“cmd.set_gear_location”或“cmd->set_gear_location”，出现次数多，但是总的处理逻辑就如下5处。
1. 每次control模块启动时，执行一次。（初始化时要start了，就GEAR_DRIVE，否则就GEAR_NEUTRAL）
2. 从list中获取status、trajectory失败时，都"cmd->set_gear_location(last_gear_planning_)"。
3. ResetDrivingCmd时，cmd.set_gear_location(last_gear_planning_);
4. 当process estop时，会cmd.set_gear_location(last_gear_planning_)  （**经常触发调用**）
5. 只要在正常的while循环中，且list中有status与trajectory，且没被pad重置，就会调用UpdateGear()，那么一定会触发其中之一的cmd.set_gear_location()逻辑。（**经常触发调用**）

6. 总结而言，就3种情况会设置档位：
（1）保持上次档位不变。（处理estop时走这个逻辑，其他情况不用太关注）
（2）其他信息都正常，但是chasis或trajectory丢失gear信息时，低速则置P档；高速设置N档。
（3）正常根据trajectory的规划要求去切换档位。（此时注意一些中间过渡档位。）
注：日志更改后，搜索关键词“set gear”。

## control对trajectory的要求
1. 从速度与预瞄点的选取来看：
（1）速度deadzone，要求规划速度> 0.1；
（2）泊车等低速模式下，trajectory最短0.1m；其他模式下根据速度不同，对最短距离要求不同，速度区间分别为0~2~3~5~max者4个区间，对应最短长度分别为：0.3m 1.0m 2.0m 3.0m。
（3）纵向预瞄点可根据速度不同进行插值来选择不同的预瞄点，但是目前都是按照0.3m的预瞄距离、0.3s的预瞄时间来选取的。
（4）横向预瞄点也可根据速度不同进行插值选择不同的预瞄点，目前速度v与预瞄距离、预瞄时间的对应关系为：0.0~2.5m/s时，lateral_preview_time: 0.5，min_preview_dis: 0.5；3.0~7.0m/s时，lateral_preview_time: 0.3，min_preview_dis: 0.3。

## control设置刹车指令的逻辑
1. 刹车的逻辑点有4个：（通过搜索“set_brake”进行定位）
（1）pid_lon_controller中，计算与其他所有处理完成后，cmd.set_brake。
（2）有estop时，会cmd.set_brake。
（3）当“when there is an obstacle for 10 minutes the gear_location is Parking”时，会cmd.set_brake。
（4）reset cmd时，会cmd.set_brake(0)。
其中需要细化理解的点有：
（1）pid_lon_controller中有2中情况：纵向控制时，根据计算处的acc计算brake；横向控制时，如果转角过大，也会限制acc到-2（对应brake约为22%）。
（2）有estop时，分2种情况处理：如果需要smooth_estop_brake时，就从当前刹车值开始，每个周期增加1%，最大增加到hard_estop_brake(65%)或soft_estop_brake(45%)。
如果不需要smooth时，直接根据当前brake值与estop_brake值之间取一个max值，直接写入到cmd中。（当然estop_brake分soft与hard。）
（3）当车辆正好在障碍物或者斜坡上时，根据当前的档位状态是否会溜车，确定是否需要刹车，并设置刹车值。



