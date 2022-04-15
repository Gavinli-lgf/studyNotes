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
