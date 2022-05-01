# 傅立叶变换&欧拉公式
* e<sup>iwt</sup>=coswt + i sinwt的推导，见[欧拉公式](https://zhuanlan.zhihu.com/p/53961508)
1. 复数实际上是将实数这个一维数域扩展到了二维数域。
2. 欧拉公式实现了是代数和几何的统一。
3. 复指数函数的实部和三角函数是等价的。
4. 复振幅实际包含了振幅及相位的信息。
5. 复指数函数表示波信息也是完备的（虽然用三角函数表示波表面看更符合我们的直观认知），且e<sup>i \theta </sup>与e<sup>iwt</sup>的代数结构完美契合了简谐运动的物理本质（正交、周期、归一），因此用欧拉公式来分析简谐运动是比较合适的。
* 以上就是**傅里叶变换**：一种线性积分变换，用于信号在时域（或空域）和频域之间的变换。经傅里叶变换生成的函数 f ^ {\displaystyle {\hat {f}}} \hat f 称作原函数 f {\displaystyle f} f 的傅里叶变换、亦称频谱。 f {\displaystyle f} f 是实数函数，而 f ^ {\displaystyle {\hat {f}}} \hat f 则是复函数，用一个复数来表示振幅和相位。 （傅立叶变换说明自然界的很多现象，都可以用三角函数进行分解）
1. 傅立叶变换、傅立叶逆变换就是两种积分形式（具体可搜索）
2. 傅里叶级数、离散傅里叶。

# Laplace变换&傅立叶变换
（傅里叶变换是将函数分解到频率不同、幅值恒为1的单位圆上；拉普拉斯变换是将函数分解到频率幅值都在变化的圆上。因为拉普拉斯变换的基有两个变量，因此更灵活，适用范围更广。）
* [通俗解释1](https://blog.csdn.net/ciscomonkey/article/details/85067036)
1. **赫维赛德的微积分算子**：一阶微分用p表示，n阶微分用p<sup>n</sup>表示，积分算子用1/p表示（这与控制理论中的积分表示方式也相同）。
2. 赫维赛德的微积分算子，就是拉普拉斯变换的前身。
3. **傅里叶变换**是轻量版拉普拉斯变换。
4. 傅里叶变换有一个很大局限性，那就是信号必须满足狄利赫里条件才行(特别是那个绝对可积的条件),这就导致一大批函数无法使用傅立叶变换。数学家们想到了一个绝佳的主意：把不满足绝对的可积的函数乘以一个快速衰减的函数，这样在趋于无穷 时原函数也衰减到零了，从而满足绝对可积。从而就形成了Laplace变换。
5. 傅里叶变换是将函数分解到频率不同、幅值恒为1的单位圆上；拉普拉斯变换是将函数分解到频率幅值都在变化的圆上。因为拉普拉斯变换的基有两个变量，因此更灵活，适用范围更广。
* [常用的Laplace变换公式](https://blog.csdn.net/qq_29695701/article/details/105993116)
* [Laplace变化公式的简单推导](https://zhuanlan.zhihu.com/p/36980082)


# linear operation
* "AB"两个矩阵的“点乘”能成立的前提条件是“A的列数 == B的行数”。（而“A的行数”、“B的列数”这两个因素不用管）

# Eigen的使用
* 矩阵的定义形式有2种：Matrix<_Scalar, _Rows, _Cols, _Options, _MaxRows, _MaxCols>、Matrix2d；
1. Matrix<_Scalar, _Rows, _Cols, _Options, _MaxRows, _MaxCols>的形式，只要指明3个参数_Scalar、_Rows、_Cols即可，其他的可不管。
2. Matrix2d也有多种形式，具体形式如下：
  * \li \c Matrix2d is a 2x2 square matrix of doubles (\c Matrix<double, 2, 2>)
  * \li \c Vector4f is a vector of 4 floats (\c Matrix<float, 4, 1>)
  * \li \c RowVector3i is a row-vector of 3 ints (\c Matrix<int, 1, 3>)
  *
  * \li \c MatrixXf is a dynamic-size matrix of floats (\c Matrix<float, Dynamic, Dynamic>)
  * \li \c VectorXf is a dynamic-size vector of floats (\c Matrix<float, Dynamic, 1>)
  *
  * \li \c Matrix2Xf is a partially fixed-size (dynamic-size) matrix of floats (\c Matrix<float, 2, Dynamic>)
  * \li \c MatrixX3d is a partially dynamic-size (fixed-size) matrix of double (\c Matrix<double, Dynamic, 3>)
注：MatrixXf is a dynamic-size matrix of floats (\c Matrix<float, Dynamic, Dynamic>) //说明“MatrixXf”是一个动态矩阵，但不一定是方阵。
* 矩阵的访问：You can access elements of vectors and matrices using normal subscripting:
  *Eigen::VectorXd v(10);
  *v[0] = 0.1;
  *v[1] = 0.2;
  *v(0) = 0.3;
  *v(1) = 0.4;
  *
  *Eigen::MatrixXi m(10, 10);
  *m(0, 1) = 1;
  *m(0, 2) = 2;
  *m(0, 3) = 3;





