# 状态空间方程
## [状态空间wiki](https://zh.m.wikipedia.org/zh-cn/%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4)
* 状态是指在系统中可决定系统状态、最小数目变量的有序集合;
* 状态空间则是指该系统全部可能状态的集合;简单来说，状态空间可以视为一个以状态变数为坐标轴的空间，因此系统的状态可以表示为此空间中的一个向量。 
* 各个矩阵的名称与维数
* 状态变数的系统方块图
* 典型有反馈的状态空间模型图
* 输出回授及目标值输入的状态空间模型图

# [MPC理论](https://github.com/YuXianYuan/model-predictive-control-demo):
## 一个模型预测控制(mpc)的简单实现.docx
1. MPC生活中的启示
* “控制时域”、“预测时域”
* 模型预测控制的基本思想就蕴含在上述过程中，它利用一个已有的模型、系统当前的状态和未来的控制量，来预测系统未来的输出，然后与我们期望的系统输出做比较，得到一个损失函数，即：损失函数=（未来输出（模型，未来控制量，当前状态）-期望输出）^2。
  由于上式中模型、当前状态、期望输出都是已知的，因此只有未来控制量一个自变量。采用二次规划的方法求解出某个未来控制量，使得损失函数最小，这个未来控制量的第一个元素就是当前控制周期的控制量。
2. 实际控制的例子
* 问题描述 -> 预测模型 -> 预测模型离散化 -> 预测 -> 优化
* MPC方法的一个独特之处就是需要对未来系统状态进行预测，我们记未来p个控制周期内预测的系统状态X<sub>k</sub>，p称为预测时域，括号中k+1|k表示在当前k时刻预测k+1时刻的系统状态，以此类推，得到p个等式。（等式也说明了：系统在时间上的因果关系，即k+1时刻的输入对k时刻的输出没有影响，k+2时刻的输入对k和k+1时刻没有影响，等等（即输入只向后影响，不向前影响）。）
* 预测动态系统未来状态时，还需要知道预测时域内的控制量U<sub>k</sub>。（“通过离散化状态方程依次对未来p个控制周期的系统状态进行预测”得出的方程组中，x(k)可以实时测量，x(k+1)~x(k+p)、u(k+1)~u(k+p)都是未知量。怎么根据p个等式，求解两组未知量呢？）
* 新定义一个目标函数J，J中引入P个参考值；再将P个未来状态x(k+1)~x(k+p)都用上面P个等式进行代入替换，值得到J与x(k)、r(k+1)~r(k+p)、u(k+1)~u(k+p)的等式。此式中只有标量J与u(k+1)~u(k+p)未知，因此可以求出J值最小的优化问题，来求解u(k+1)~u(k+p)。
* 对目标函数J处理后，可得最终优化目标函数，至此可直接调用matlab quadprog函数求解Uk，将Uk的第一个元素提取出来，作为本控制周期的控制量。
3. 仿真
* simulink的框图也能很好的对系统有个认知。
* 模型预测控制原理图

# [OSQP](https://osqp.org/docs/examples/mpc.html) 
简写（OASES 简写“online active set strategy”）
## [a parametric active-set algorithmfor quadratic programming](https://link.springer.com/article/10.1007/s12532-014-0071-1)
* Abstarct: One relatively recent approach to solve QP problems are parametric active-set methods that are based on tracing the solution along a linear homotopy between a QP problem with known solution and the QP problem to be solved. This approach seems to make them particularly suited for applications where a-priori information can be used to speed-up the QP solution or where high solution accuracy is required. In this paper we describe the open-source C++ software package qpOASES, which implements a parametric active-set method in a reliable and efficient way.主要应用于small- to medium-scale convex test examples, Finally, we describe how qpOASES can be used to compute critical points of nonconvex QP problems（也可用于非凸问题）.
1. Introduction
* This paper describes the current release 3.0 of the open-source software package [qp OASES](https://github.com/coin-or/qpOASES).This software package implements a parametric active-set method for solving convex quadratic programming (QP) problems and for computing critical points of nonconvex quadratic programming problems.Linear model predictive control (MPC)(说明MPC应用与线性系统吗？) As MPC is frequently applied to processes with very fast dynamics, it becomes crucial to solve the resulting convex QP problems at very high rates; possibly within a millisecond or less [57]. Moreover, as MPC controllers typically need to run autonomously without further user-interaction, QP solution needs to be highly reliable.
* We consider quadratic programming problems of the following form：（见论文，与[《一个模型预测控制（MPC）的简单是线.docx》]()中推导的格式相同）. A quadratic program of the form (1) is convex (strictly convex) if and only if its Hessian matrix H is positive semidefinite (positive definite); it is nonconvex otherwise. 
* Existing methods： active-set and interior-point methods,  fast gradient methods. Interior-point methods are mainly used in two different variants: primal barrier methods and primal-dual methods.  Active-set methods can be divided into primal, dual, and parametric methods. The current state vector v0 is repeatedly estimated from real-world measurements, and at each sampling instant problem (6) is solved on-line to find the optimal feedback control u0 ∈ Rn u . This optimized control is then used to control the process, until the next, more recent feedback control has been computed from the next state observation.
2. Algorithm
4. Software design and algorithmic parameters
* cold-start & hot-start: qpOASES distinguishes two different ways of solving a QP problem of the form (1).First, it can be solved by performing a cold-start, i.e. without any prior solution information. This is the usual situation if just a single QP problem is to be solved. Second,provided that a QP problem with same dimensions has been already solved before,the current QP problem can be solved by performing a hot-start based on the optimal solution and the internal matrix factorizations of the previously solved QP problem.
* three different QP solver classes:  The QProblem class, The class QProblemB, the class SQProblem. 
* offer user-functions, All internal data members are hidden from the user.

# [MPC APOLLO](https://blog.csdn.net/u013914471/article/details/83824490)
## 理论分析
* Apollo中MPC controller的代码主体集成了横、纵向控制，在计算控制命令时，计算了横、纵向误差。
* 模型预测控制的三要素：预测模型、滚动优化、反馈矫正。
* 线性模型预测控制较非线性模型预测控制有更好的实时性，且更易于分析和计算。但是无论是运动学模型，还是动力学模型，所搭建的均为非线性系统。因此，需要将非线性系统转化为线性系统。方法大体可分为精确线性化和近似线性化，多采用近似的线性化方法。（此处采用泰勒级数展开进行近似）
* Apollo的MPC模块中的状态变量共有6个。每个状态都是可测量的（测量方法即计算方法，与pid、lqr方法中的一致）。
* 控制变量有2个，control_matrix=[δf​a​]。（前轮转向角、纵向加速度）
* mpc总的运动学模型方程，见帖子。车辆模型体现再A、B、C矩阵上。（比《车辆运动力学及控制》多了2个维度）
* A、B、C矩阵离散化（双线性变换离散法）。
* 最终离散化的模型为：x(k+1)=Ax(k)+Bu(k)+C  系统的输出方程为：y(k)=Dx(k)。
* 综上所述，MPC控制器的工作原理大致如帖子
* x(t)为 t 时刻车辆的观测状态，x(t)^​为 t时刻车辆的估计状态，u^*(t)为t时刻的最优控制解，y(t)为 t t t时刻的系统输出。
## 代码分析
* 还有反馈矩阵K，1*6
* q、r都是对角矩阵，时线二次优化中的平方
* 

