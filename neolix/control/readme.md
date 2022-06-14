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
6. 


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


# 涉及的理论知识：
1. [OptimalTrajectoryGenerationforDynamicStreetScenariosinaFrenetFrame](https://www.cnblogs.com/kin-zhang/p/15006838.html)用于...。
2. [黄金分割搜索算法（一维搜索算法）](https://en.wikipedia.org/wiki/Golden-section_search)，用于control求轨迹中最近点的插值方法。
3. 




