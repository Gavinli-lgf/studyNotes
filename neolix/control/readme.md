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
22. 横向计算时，预瞄点的选取有2个标准；而纵向计算时，预瞄点选取又有第3个标准。这样是有问题的吧？
23. 

## lqr_lateral_controller理论知识需要完善的地方
1. 正向行驶、倒车行驶时的control逻辑与运算方式都是相同的吗？
2. SteerComponentCalc()中，对于倒车时，steer_angle_lateral_contribution_变量的处理原理要搞清。
3. 预瞄点与这个(record_x,record_y)点的0.1s的关系要搞清
4. lateral_error_rate_、heading_error_rate_两者的计算公式待搞清？...（参照代码）
5. [状态空间模型的离散化](https://www.guyuehome.com/13948)的2种方法：精确离散化方法、近似离散化方法。其中“近似离散化方法”分为3中：向前欧拉法、向后欧拉法、中点欧拉法（对应了老王视频中讲的离散化方法）。根据对状态空间方程dot{x}=Ax+Bu两边积分分别去前边界点、后边界点、中间点可得。离散化后得x(k+1)=Gx(k)+Hu(k)，（1）向前欧拉法：G = I + A * delta T, H = B * delta T;（2）...；（3）neolix中对G使用中点欧拉法，对H使用向前欧拉法。（注意称呼：是“状态空间模型的离散化”，而不是“矩阵的离散化”。）
6. [无人车横向控制综述](https://zhuanlan.zhihu.com/p/46377932)


# 车辆动力学模型(参照b站老王的推导)
1. 
车辆航向角： 地面坐标系下，车辆质心速度与横轴的夹角
车辆质心侧偏角：车辆质心速度方向与车头指向的夹角
车辆横摆角 = 航向角 - 质心侧偏角
如下图： θ \theta θ是航向角； β \beta β是质心侧偏角； ϕ \phi ϕ是横摆角
θ = β + ϕ \theta=\beta+\phi θ=β+ϕ
  1. 实际求解中使用的是车辆“航向角”，而非“横摆角”；但是横摆角方向与车辆坐标系的x轴一致，所以车辆“航向角”与车身坐标系的坐标轴并不重合。
  2. 横向控制的2个状态分别是横向偏差ed、横摆角偏差eϕ。（而非航向角偏差eθ）
2. frenet坐标系下的关键点就是2个：切向量τ、发向量n对于dt的微分结果。dτ/ds=kn , dn/ds=-kτ (从向量的平行四边形法则来理解记忆)
3. 使用向量法求出车辆相对trajectory上matched_point的“s、d、s_dot、d_dot”的计算公式是控制的基础。
4. “运动学方程”适用于大、小转角都可以，而泊车、掉头等低速模式下的转角从小到大变化范围都很大，因此需要使用运动学方程来求解；
    “动力学方程”例如lqr，适用于小转角（因方程推导中有近似），而对车速高低没有要求，因此“运动学方程”常用于高速模式。
5. "路径规划"、“轨迹规划”，名词区别。前者不包含时间信息，后包含时间信息、速度、加速度、曲率等。（因此预瞄点的选取不仅与位置有关，还与时间有关。）
    因此，“轨迹”其实是一系列与时间t相关的函数：x(t)、y(t)、v(t)、a(t)、kpa(t)等。
6. “规划的轨迹”要有“切线、曲率、速度、加速度”等因素的另一个原因是：车辆不能单独做横向运动，其横向运动必须由纵向运动进行诱发。（与机器人不同）
7. 汽车规划的边界条件，不仅与时间有关，还与坐标有关。因此有"d/dt"与"d/dx"两种限制条件。（在Frenet坐标系中为d/ds）。
8. 解释了为什么能使用5次多项式进行轨迹规划的求解。
9. "轨迹规划"是基于直角坐标系，控制是基于自然坐标系（Frenet）。
10. 利用向量点乘计算出来的误差，还要注意正负问题。
11. 一般汽车都会轻度转向不足（为了安全），而赛车一般调校为中性转向（为了更灵敏的转向效果）。


1. [车辆航向角、横摆角、质心侧偏角](https://blog.csdn.net/qq_31880107/article/details/86542879)


# apollo 7.0源码解析
## control源码解析
* [（五十一）通俗易懂理解——apollo Control模块(3)横纵向控制](https://zhuanlan.zhihu.com/p/350195931)
* [Apollo control模块横向控制原理及核心代码逐行解析](https://blog.csdn.net/weixin_39199083/article/details/122228076)

## 程序中的单位
* max_steer_angle: 6.6323  //方向盘从中间位置单向打到底，所转过的rad。和轮距一起可以用于计算max_kappa。（此外min_turn_radius也决定了max_kappa）
* 

# neolix中一些逻辑汇总
## 程序中需要区别的量
* “车辆侧偏角”区别于“轮胎侧偏角”
* 

1. control失败，会产生什么效果？
	答：以GetAbsoluteTimeLateralAndHeadingError()为例，失败后会导致estop、hard_estop、ESTOP_CONTROLFAIL。（hard_estop:65%; soft_estop:45%;）
2. trajectory每次都是以子车位置为规划起点。（reference_line时，以routing上离ego最近的位置为规划起点）。
3. trajectory是100Hz，即使按最大7m/s算，一般trajectory的前0.7m范围内，都能找到最近点。（0.5m的预瞄，一般处理长度不会超过trajectory的前1.2m范围。）
    但是，正常的trajectory给的点数是400左右，但是每个点的取法，会按时2种取法：时间间隔、距离间隔。时间间隔时，从dv看trajectory的线会根据速度不同，经常变长或变短；距离间隔时trajectory的长度会保持不变。（但是control的处理逻辑并没有适配这2种情况，待确认。）
    正常一次trajectory有400个点（20ms一个点，总时长8s。）
4. trajectory是最大0.1s的周期，人眼300ms，肉眼无法识别起点与自车不重合。
5. 正常planning_time > curr_time，delta_time > 0。这个逻辑保证了预瞄点的预瞄时间是在current_time与cur_index分别对应delta_time中取的最大值。
6. 如果快到达routing终点或者其他trajectory点较少的情况，此时找预瞄点会失败。
7. 找到预瞄点后，就要计算state_matrix:
（1）lateral_error：需要5个量就能计算出来。自车位置(x,y)、预瞄点位置(x_t,y_t)、预瞄点的heading_t。通过"x, y, x_t, y_t, heading_t"这5个量可以计算出自车在sl坐标系下的横向误差lateral_error（单位:m）。
（2）heading_error：需要5个量就能计算出来。定位的姿态信息(qx,qy,qz,qw)，预瞄点的heading_t。通过"qx,qy,qz,qw,heading_t"这5个量，算出heading_error，其在FLU、ENU、SL坐标系下值都相同。（单位:rad。所以heading_error最大值不能超过0.523，因为这是前轮最大转角30度。）
（3）lateral_error_rate_：横向误差变化率，就等于当前车速在sl坐标系下，沿预瞄点l方向的投影。（因此只与2个因素有关：当前车速、朝向误差。）
（4）heading_error_rate_：横摆误差变化率，就等于“车辆自身的横摆角速度 - 道路曲率产生的横摆角速度”。（因此与3个因素有关：自车姿态信息<横摆角速度>、车速、道路曲率）。
（5）注意：这里的state是根据两个预瞄点信息混用计算出来的。这样会有问题吧？！（即横向计算时，预瞄点的选取有2个标准；而纵向计算时，预瞄点选取又有第3个标准。这样是有问题的吧？）
8. GetAbsoluteTimeLateralAndHeadingError()中预瞄时间决定了至少，预瞄点至少在最近点0.5s后；但是日志中打印的record_x,record_y,record_head，记录的是0.1s后的点，也就是说，下一次trajectory更新时，车辆应该到达的位置。
（1）所以“record_x,record_y,record_head”与预瞄点的(x,y),heading还不一样。
（2）“record_x,record_y,record_head”除了打印，并无其他作用。
9. 正常一次trajectory有400个点（20ms一个点，总时长8s。）
10. 前馈的预瞄点和反馈的预瞄点可能不一样。在车辆车辆速度 < 2.1，或者low_speed_control时，两者相同；其他情况下不同，前馈按照配置文件找，反馈计算而来。
11. 在整个系统中，Frenet frame坐标系的定义也不是唯一的。例如control中，是以planning给的reference trajectory为Frenet坐标系的中心线的；但是planning中就可能是以routing给的reference line为Frenet坐标系的中心线的。（后者待验证？）
12. “运动学方程”适用于大、小转角都可以，而泊车、掉头等低速模式下的转角从小到大变化范围都很大，因此需要使用运动学方程来求解；
    “动力学方程”例如lqr，适用于小转角（因方程推导中有近似），而对车速高低没有要求，因此“运动学方程”常用于高速模式。

## control中档位切换的逻辑整理：
注：日志更改后，搜索关键词“set gear”。
1. 总结而言，就4种情况会设置档位：
（1）保持上次档位不变。（3种情况：control获取信息失败、处理estop、复位时，走这个逻辑。）
（2）信息获取正常，但是chasis或trajectory丢失gear信息时，低速则置P档；高速设置N档。
（3）正常根据trajectory的规划要求去切换档位。（此时注意一些中间过渡档位。）
（4）初始化时1次，默认D或N。
2. 详细情况：搜索“cmd.set_gear_location”或“cmd->set_gear_location”，出现次数多，但是总的处理逻辑就如下5处。
  1. 档位初始化：每次control模块启动时，执行一次。（初始化时要start了，就GEAR_DRIVE，否则就GEAR_NEUTRAL）
  2. 逻辑处理失败时：从list中获取status、trajectory失败时，都"cmd->set_gear_location(last_gear_planning_)"。
  3. 复位时：ResetDrivingCmd时，cmd.set_gear_location(last_gear_planning_);
  4. 急停时：当process estop时，会cmd.set_gear_location(last_gear_planning_)  （**经常触发调用**）
  5. 按照trajectory正常切换档位：只要在正常的while循环中，且list中有status与trajectory，且没被pad重置，就会调用UpdateGear()，那么一定会触发其中之一的cmd.set_gear_location()逻辑。（**经常触发调用**）

## control对trajectory的要求
1. 从速度与预瞄点的选取来看：
（1）速度要求：       速度deadzone，要求规划速度> 0.1；
（2）长度要求：	     泊车等低速模式下，trajectory最短0.1m；其他模式下根据速度不同，对最短距离要求不同，速度区间分别为0~2~3~5~max者4个区间，对应最短长度分别为：0.3m 1.0m 2.0m 3.0m。
（3）预瞄点要求-纵向：纵向预瞄点可根据速度不同进行插值来选择不同的预瞄点，但是目前都是按照0.3m的预瞄距离、0.3s的预瞄时间来选取的。
（4）预瞄点要求-横向：横向预瞄点也可根据速度不同进行插值选择不同的预瞄点，目前速度v与预瞄距离、预瞄时间的对应关系为：0.0~2.5m/s时，lateral_preview_time: 0.5，min_preview_dis: 0.5；3.0~7.0m/s时，lateral_preview_time: 0.3，min_preview_dis: 0.3。

## control设置刹车指令的逻辑
1. 刹车的逻辑点有4个：（通过搜索“set_brake”进行定位）
（1）控制器控制刹车：	  pid_lon_controller中，计算与其他所有处理完成后，cmd.set_brake。
（2）各模块急停信号刹车：  有estop时，会cmd.set_brake。
（3）换档与坡道时刹车辅助：当“when there is an obstacle for 10 minutes the gear_location is Parking”时，会cmd.set_brake。
（4）重置清除刹车：	  reset cmd时，会cmd.set_brake(0)。
其中需要细化理解的点有：
（1）pid_lon_controller中有2中情况：纵向控制时，根据计算处的acc计算brake；横向控制时，如果转角过大，也会限制acc到-2（对应brake约为22%）。
（2）有estop时，分2种情况处理：如果需要smooth_estop_brake时，就从当前刹车值开始，每个周期增加1%，最大增加到hard_estop_brake(65%)或soft_estop_brake(45%)。
如果不需要smooth时，直接根据当前brake值与estop_brake值之间取一个max值，直接写入到cmd中。（当然estop_brake分soft与hard。）
（3）当车辆正好在障碍物或者斜坡上时，根据当前的档位状态是否会溜车，确定是否需要刹车，并设置刹车值。


## 对于转角的控制逻辑
1. 计算出来的转角，在发送到channel之前，已经对转角变化率做了限制。速度小时变化率大，速度大时变化率小，大小范围在0.8% ~ 3%之间。
2. 通过曲率快速计算方向盘转角的方法1：最大曲率0.25时，方向盘转角100%；那么假设道路曲率是0.04是，对应方向盘转角应该是“0.04/0.25*100% = 16%”。
  方法2：R=L/tan(alpha) 或 kpa = tan(alpha) / L。
3. 方向盘单向最大转动370度，传动比12.33，对应转向轮最大转向角30度，对应100%的曲率0.25。
   而lqr计算出来的是rad，因此最大转角为0.523。
4. 根据预瞄点曲率，计算前馈转角的公式：...。
5. 根据前轮转角，计算当前

## 定位相关内容：
1. 缩略语：
  1. “dr”: localization_dr、DRResult等中的“dr”是“dead reckoning”的缩写，汉语意思“航位推导”。即odometry位置就是通过航位推导获得的。所以proto文件localization_dead_reckoning.proto就是odometry的定位信息。
  2. "pnt"：localization_gnss_pnt_result.proto文件中的“pnt”是“Positioning, Navigation and Timing Systems”首字母的缩写，就是卫星定位信息。最终处理后的卫星定位信息在localization_pose.proto文件中。
  3. "rtk":"Real-time kinematic positioning"实时运动定位。
  4. “FCW”：Forward Collision Warning (FCW)前方碰撞预警系统。
  5. “DRIFT”：drift，漂移、侧滑、甩尾。（在这里指“定位的漂移”）
  6. "EPB"：“Electrical Park Brake”电子驻车制动的简称。该系统可以实现“静态驻车、静态释放（关闭）、自动时放（关闭）、自动驻车、动态驻车”，但是Neolix上的功能还不清楚。
  7. "4WS":四輪轉向（英語：Four-wheel steering, 4WS）指後軸同樣具備轉向能力.


2. 根据[飞书世界模型](https://r3c0qt6yjw.feishu.cn/wiki/wikcnTx1NZnwmdrMuBg5MjojFgc)中的定义：
  * “base_link坐标系”，是随车而动的，原点在后轴中心，FLU为方向；
  * “imu坐标系”，随车而动的，方向为RFU；（IMU提供的是一个相对的定位信息，它的作用是测量相对于起点物体所运动的路线，所以它并不能提供你所在的具体位置的信息，因此，它常常和GPS一起使用，当在某些GPS信号微弱的地方时，IMU就可以发挥它的作用，可以让汽车继续获得绝对位置的信息，不至于“迷路”。）
  * “odometry坐标系”，全局坐标系，原点固定，一般说车辆在Odometry的位置和位姿指的是base_link在Odometry的位置和位姿！
  * “UTM坐标系”，全局坐标系，原点不固定，取每次车辆启动时的位置为原点，方向ENU，Position of the vehicle reference point (IMU) in the map reference frame.
3. [IMU](https://zhuanlan.zhihu.com/p/98113366)：IMU通常包含陀螺仪(Gyroscope)、加速度计(Accelermeters)，有的还包含磁力计(Magnetometers)。陀螺仪用来测量三轴的角速度，加速度计用来测量三轴的加速度，磁力计提供朝向信息。因此IMU可以测量3个方面的信息：物體三軸姿態角（或角速率）、三轴加速度、朝向信息。（三轴加速第常用于于GPS融合定位；三轴姿态、朝向信息用于车身姿态的计算，用于车辆模型的计算。实际车辆朝向heading，也是从定位IMU的四元数中获得的。）
    一般的，一個IMU內會裝有三軸的陀螺儀和三個方向的加速度計，來測量物體在三維空間中的角速度和加速度，並以此解算出物體的姿態。為了提高可靠性，還可以為每個軸配備更多的傳感器。一般而言IMU要安裝在被測物體的重心上。 
  * 原理：机体坐标，一般计算位置信息，需要将其通过姿态角（roll、pitch、yaw）转换到导航坐标下去，然后减去重力加速度，得到线性加速度后再去积分。
  * IMU提供的是一个相对的定位信息，它的作用是测量相对于起点物体所运动的路线，所以它并不能提供你所在的具体位置的信息，因此，它常常和GPS一起使用，当在某些GPS信号微弱的地方时，IMU就可以发挥它的作用，可以让汽车继续获得绝对位置的信息。
  * 众所周知，GPS可以为车辆提供精度为米级的绝对定位，差分GPS或RTK GPS可以为车辆提供精度为厘米级的绝对定位，然而并非所有的路段在所有时间都可以得到良好的GPS信号。因此，在自动驾驶领域，RTK GPS的输出一般都要与IMU，汽车自身的传感器（如轮速计、方向盘转角传感器等）进行融合。(GPS：数据准确，更新频率低，100Hz；IMU：更新频率高，但误差随着时间增长而变大；因此可用GPS每100ms修正一次汽车的实际位置，而IMU在两个100ms之间预测9次，两者结合可以提供很准确的100Hz的定位结果。)
4. Odometry:
    [Odometry Introduction](https://chargerkong.github.io/2021/09/09/0909%E9%85%8D%E7%BD%AE%E9%87%8C%E7%A8%8B%E8%AE%A1/)
    里程计系统根据机器人的运动提供了机器人的姿态和速度的局部精确估计。里程表信息可以从各种来源获得，如IMU、LIDAR、RADAR、VIO和轮编码器。需要注意的是，imu随时间漂移，而轮式编码器随移动距离漂移，因此它们经常被一起使用来抵消彼此的负面特性。
    odom坐标系和与之相关的变换使用机器人的里程计系统发布连续的定位信息，但随着时间或距离(取决于传感器的形态和漂移)变得不那么准确。尽管如此，机器人仍然可以利用这些信息在其附近导航(例如避免碰撞)。为了在一段时间内获得一致准确的里程数信息，地图框架提供了全球准确的信息，用于校正odom框架。

# 泊车相关内容：
## Reeds-Shepp和Dubins曲线简介
**无障碍物时**
1. 什么是Reeds-Shepp曲线：要把车停到车位里，想找一条最短的路径把车停进去，该最短路径就是Reeds-Shepp曲线。Reeds-Shepp曲线由Reeds和Shepp二人在1990年的论文《Optimal paths for a car that goes both forwards and backwards》中提出。
2. Reeds-Shepp曲线是什么样的曲线：由于汽车都有一个最小转向半径，当汽车从不同的初始位置和朝向进入同一个停车位时，Reeds-Shepp曲线一般是由几段半径固定的圆弧和一段直线段拼接组成，而且圆弧的半径就是汽车的最小转向半径。这里的路径长度是指汽车中心运动轨迹的长度，也就是所有圆弧的弧长和直线段的长度之和。
3. 什么是Dubins曲线：Dubins曲线和Reeds-Shepp曲线差不多，只不过多了一个约束条件：汽车只能朝前开，不能后退（不能挂倒挡）。
4. Reeds-Shepp曲线和Dubins曲线对任意的起止位姿都是存在的。（二者有时是重合的）
5. Reeds-Shepp曲线和Dubins曲线特指没有障碍物时的最短路径。如果存在障碍物，那么这样的曲线不再是传统意义上的RS和Dubins曲线了，不过为了保持一致我们还是这么称呼它们吧。
**有障碍物时**
1. 有障碍物的情况，对于RS曲线、Dubins曲线的情况是不同的：
  * RS曲线：只要存在连接起止位姿的无碰撞路径，那么就存在无碰撞的Reeds-Shepp曲线。
  * Dubins曲线：然而这个结果对Dubins曲线却不适用。
**Reeds-Shepp和Dubins曲线的启发**
  Reeds-Shepp和Dubins曲线只不过是最优曲线的两个特殊情况，我们可以考虑各种各样的机器人约束或者目标函数，这时的曲线就更有意思了，当然也更难了。Reeds-Shepp和Dubins曲线之所以有名，是因为它们刚好存在解析形式，而且形式还不是太复杂，类似的曲线还有Balkcom-Mason曲线。其它更复杂的最优曲线要想求解析解是非常困难的。


# 涉及的理论知识：
1. [OptimalTrajectoryGenerationforDynamicStreetScenariosinaFrenetFrame](https://www.cnblogs.com/kin-zhang/p/15006838.html)用于...。
2. [黄金分割搜索算法（一维搜索算法）](https://en.wikipedia.org/wiki/Golden-section_search)，用于control求轨迹中最近点的插值方法。
3. [IMU：自动驾驶定位系统最后一道防线](https://www.autoinfo.org.cn/autoinfo_cn/content/news/20191230/1856850.html)
4. [无人驾驶中用到的八大坐标系](https://cloud.tencent.com/developer/news/404364)
5. [Reeds-Shepp和Dubins曲线简介](https://blog.csdn.net/robinvista/article/details/95137143)
6. Reeds-Shepp和Dubins曲线相关论文：
[1]　Optimal Paths for a Car That Goes both Forwards and Backwards，J. A. Reeds and L. A. Shepp，Pacific Journal of Mathematics.
[2]　On Curves of Minimal Length with a Constraint on Average Curvature, and with Prescribed Initial and Terminal Positions and Tangents，Lester E. Dubins，American Journal of Mathematics.




