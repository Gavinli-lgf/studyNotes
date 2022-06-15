# [无人车横向控制综述](https://zhuanlan.zhihu.com/p/46377932)
## 1. 简介
1. 2004 年起美国国防部高级研究计划局(DARPA)举办的三届 DARPA 无人驾驶挑战赛是现代无人驾驶发展的重要里程碑事件，许多无人驾驶横向控制算法在 DARPA 系列挑战赛中发挥重要作用。
2. 大赛中采用的横向控制方法有多种：
  1. 根据横向控制是否使用车辆模型，可以将其分为2种类型：**无模型的横向控制方法**和**基于模型的横向控制方法**。
  2. 无模型的横向控制即传统的 PID 控制算法。
  3. 基于模型的横向控制方法又可分2种为：基于**车辆运动学模型**的横向控制方法、基于**车辆动力学模型**的横向控制方法。
  4. 基于车辆运动学模型的横向控制算法有3种：纯跟踪控制(Pure Pursuit)算法、后轮反馈控制(Rear wheel feedback)、前轮反馈控制(Front wheel feedback)算法
  5. 基于车辆动力学模型的横向控制算法有3种：二次型调节器(Linear Quadratic Regulator，LQR)控制算法、MPC算法、tube MPC算法。
3. 基于模型的控制算法普遍来讲有更好的效果，因此熟悉车辆的模型最重要。
## 2. 基于车辆运动学模型的横向控制算法
1. 车辆运动学模型
  车辆的运动学约束、两轮的自行车模型、假设车辆的前后轮均为刚体，只能沿着车轮滚动的方向前进，无侧向滑动。可以求的可得[自行车模型的运动微分方程](./appendix/pic_2_1.png)。
2. **纯跟踪控制算法(Pure Pursuit)**
  * 该算法的思想：基于当前车辆后轮中心位置，在参考路径上向前l<sub>d</sub>的距离匹配一个预瞄点，假设车辆后轮中心点可以按照一定的转弯半径R行驶抵达该预瞄点，然后根据预瞄距离l<sub>d</sub>，转弯半径R，车辆坐标系下预瞄点的朝向角α之间的几何关系来确定前轮转角δ。（输入、输出，已知、未知，输入都是已知量/可测量量，输出都是未知量/待求量。）
  * 该方法对外界的鲁棒性较好，在DARPA比赛中有多辆车采用该控制算法对车辆进行横向控制，并取得了很好的控制效果。
3. **[后轮反馈控制算法（Rear wheel feedback）](https://zgh551.github.io/2020/02/26/%E6%8E%A7%E5%88%B6%E7%AE%97%E6%B3%95-%E5%90%8E%E8%BD%AE%E4%BD%8D%E7%BD%AE%E5%8F%8D%E9%A6%88/)**
  * 该算法的思想：使用后轮位置反馈的路径跟踪算法，使用李亚普洛夫稳定判据，推导控制率。
  具体的是根据后轮与参考轨迹的位置误差e<sub>b</sub>、横摆角偏差e<sub>Φ</sub>，再使用李亚普洛夫稳定判据，推导转向角δ；然后将δ、v<sub>ref</sub>输入车辆作为控制量；最后将车辆的实际位置与横摆角(x,y),Φ，作为反馈与目标曲线一起重新用于控制系统。
  * 后轴位置反馈控制对于曲率连续变化的曲线控制较好，但对于曲率恒定的曲线 (圆弧)，控制输出存在抖动。实际车辆控制时，由于执行器本身可以等效为一个低通滤波器，实测控制抖动较小。
  * 基于“仿真的系统框图”可以更好的加深对系统的理解。
4. **[前轮反馈控制（Front wheel feedback）/Stanley方法](https://zgh551.github.io/2020/02/23/%E6%8E%A7%E5%88%B6%E7%AE%97%E6%B3%95-Stanley%E6%B3%95/)**
  * 该算法的思想：根据前轮与参考轨迹的位置误差e<sub>f</sub>、横摆角偏差e<sub>Φ</sub>、系数k、车速v<sub>x</sub>，推导转向角δ；然后将δ输入车辆作为控制量；最后将车辆的实际位置与横摆角(x,y),Φ，作为反馈与目标曲线一起重新用于控制系统。
  * 适合低速下的车辆路劲跟踪。
## 3. 基于车辆动力学模型的横向控制算法
1. 车辆线性二自由度动力学模型
2. 车辆路径跟踪偏差状态方程
3. LQR横向控制算法
4. MPC横向控制算法
5. tube MPC控制算法

## 4. 总结与展望
（只有知道了各个算法的优缺点、适用条件、算力需求等等各种特性后，才能进行更好的排列组合、优化二次开发等方式，开发出适合不同车型的最优控制方式）
1. 总结
  1. PID 控制算法：根据偏差进行控制，没有考虑车辆本身的特性，因此算法对外界干扰的鲁棒性较差，无法满足车辆在高速行驶过程中的有效控制。
  2. 
2. 展望

## 5. 参考文献
1.     陈慧岩, 陈舒平, 龚建伟. 智能汽车横向控制方法研究综述[J]. 兵工学报, 2017, 38(6):1203-1214.
2. J. P. Hespanha et al., “Trajectory-tracking and path-following of under-actuated autonomous vehicles with parametric modeling uncertainty,”Transactions on Automatic Control, vol. 52, pp. 1362–1379, 2007. 
3. 佐思产研, 谈谈无人车横向控制, https://mp.weixin.qq.com/s/pqs8UccxqfzaEnLauI7WBQ.[4
4. R. Wallace, A. Stentz, C. E. Thorpe, H. Maravec, W. Whittaker, and T. Kanade, “First results in robot road-following.,” in IJCAI, pp. 1089–1095, 1985. 
5. Paden B, Čáp M, Yong S Z, et al. A Survey of Motion Planning and Control Techniques for Self- Driving Urban Vehicles[J]. IEEE Transactions on Intelligent Vehicles, 2016, 1(1):33-55. 
6. Rajamani R. Vehicle Dynamics and Control[M]. Springer Science, 2006. 
7. Snider J M. Automatic Steering Methods for Autonomous Automobile Path Tracking[J]. Robotics Institute, 2009.
8. [控制算法 - 后轮位置反馈](https://zgh551.github.io/2020/02/26/%E6%8E%A7%E5%88%B6%E7%AE%97%E6%B3%95-%E5%90%8E%E8%BD%AE%E4%BD%8D%E7%BD%AE%E5%8F%8D%E9%A6%88/)
9. [控制算法 - Stanley 法](https://zgh551.github.io/2020/02/23/%E6%8E%A7%E5%88%B6%E7%AE%97%E6%B3%95-Stanley%E6%B3%95/)






