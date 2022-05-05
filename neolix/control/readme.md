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

