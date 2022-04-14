# control program refactoring suggestion:
## lqr_lateral_controller
1. lqr_lateral_controller.cpp,将SteerComponentCalc()函数拆分为3部分，分别用来计算反馈量、前馈量、总的转向输入量。
2. lqr_lateral_controller.cpp -> GetParasFromScheduler() -> L896~L905改成if(lqr_controller_conf_.tuning_mode()){}else{GainScheduler()}的模式，即当是调试模式时，直接取forward_paras(0)，不是调试模式时再去计算。而现有逻辑不管是不是调试模式，都先按非调试模式处理一遍的逻辑是不合理的。
3. 车辆动力学模型中C<sub>r</sub>C<sub>f</sub>都是只单个轮胎的刚度，不能乘以2。
4. lqr_lateral_controller.h中定义的Config adu_data_conf_;在lqr横向控制空并没有用到，该变量可以删除（对应proto文件先留着）。
5. 
