# ControlMath
## dot_product
* 输入：二维向量坐标；
* 输出：标量
* [说明](https://www.zhihu.com/question/21080171):假如 向量a 为（x1, y1），向量b为(x2, y2):点积（也叫内积）结果 为 x1 * x2 + y1 * y2 = |a||b| cos<a,b>，可以理解为向量a在向量b上投影的长度乘以向量b的长度。应用有如下2方面
1. 计算长度和角度 cos(theta)=(A.B)/(|A||B|)
2. 检测正交性:当角度为90度时，即点积为0时，两个向量正交。

## CrossProduct
* 输入：二维向量坐标；
* 输出：标量（叉乘结果向量的大小）
* 同样假如 向量a 为（x1, y1），向量b为(x2, y2)：叉积（也叫外积）的模为 x1 * y2 - x2 * y1 = |a||b| sin<a,b>，可以理解为平行四边形的有向面积（三维以上为体积）。外积的方向垂直于这两个方向。应用如下:求三角形面积

## UnifyAngle
* 输入：弧度；
* 输出：弧度（将角度结果统一在范围[-M_PI, M_PI)之间，去除的多值性） 

## Sign
判断输入值的正负符号：正 返回1，负 返回-1，0 返回0

## GetSL
* planning_adctrajectory.txt
* GetSL逻辑

planning_adctrajectory.txt
> 实际planning发给control的trajectory是总共8s，每20ms一个点；relative_time为负值时，意味着没有跟踪上，跟踪超调了。
> 这里使用文件planning_adctrajectory.txt模拟planning发给control的trajectory：
> relative_time:从这里可知，总共planning了9.66s的轨迹，每0.02s一个点；
> adc_trajectory_point：其中共10个量，纵向跟踪量：accumulated_s、speed、acceleration_s；横向跟踪量：theta、curvature、curvature_change_rate。每个量的单位都是标准单位，如下表
> 

| 变量名 | 单位 | comments |
| ----- | ---- | ---- |
| xyz | m |  |
| speed | m/s |  |
| acceleration_s | m/s<sup>2</sup> | Frenet coordination in s direction |
| curvature | (1/meters) |  |
| curvature_change_rate | (dk/ds) |  |
| relative_time | s | relative_time = time_of_this_state - timestamp_in_header |
| theta | 弧度 | relative to absolute coordinate system，范围[-M_PI, M_PI) |
| accumulated_s | m | calculated from the first point in this trajectory(从文件planning_adctrajectory.txt来看，accumulated_s为0.0时，relative_time接近0.0，但并不精确) |


