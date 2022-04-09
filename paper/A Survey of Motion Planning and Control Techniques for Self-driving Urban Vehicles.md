## Vehicle Control
  Depending on the reference provided by the motion planner, the control objective may be path stabilization or trajectory stabilization.An overview of these controllers is provided in Table II.
| Controller | Model | Url |
| ------ | ------ | ------ |
| Pure Pursuit | Kinematic | [一种几何跟踪控制算法，也被称为纯跟踪控制算法](https://blog.csdn.net/Ronnie_Hu/article/details/115817922) |
| Rear wheel based feedback | Kinematic | [None] |
| Front wheel based feedback | Kinematic | [None] |
| Feedback linearization | Steering rate controlled kinematic | [输入-输出反馈线性化控制算法](https://zhuanlan.zhihu.com/p/344837550) |
| Control Lyapunov design | Kinematic | [None] |
| Linear MPC | C<sup>1</sup> (R<sup>n</sup> × R<sup>m</sup> ) model | [介绍](http://www.kostasalexis.com/linear-model-predictive-control.html) |
| Nonlinear MPC | C<sup>1</sup> (R<sup>n</sup> × R<sup>m</sup> ) model | [介绍](http://apmonitor.com/do/index.php/Main/NonlinearControl) |

  Subsection V-A details a number of effective control strategies for path stabilization of the kinematic model, and subsection V-B2 discusses trajectory stabilization techniques. Predictive control strategies, discussed in subsection V-C, are effective for more complex vehicle models and can be applied to path and trajectory stabilization.

