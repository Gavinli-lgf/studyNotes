# 线性代数理论
## Liner Algebra Done Right
1. 向量空间（复数、向量空间的定义、向量空间的性质）
* 有限维向量空间，线性映射；实数、复数与域field（以后考虑运算性质都是指F域的）；
* 标量包括“复数”（与实数），标量与向量相对；向量、组(tuple)的概念；组的长度是有限的，且长度是一个非负整数（可以为0）；组与集合的区别；F<sup>n</sup>为F域上的高维组（n为正整数，F也包括R、C）；R<sup>1</sup>、R<sup>2</sup>、R<sup>3</sup>的几何模型很明显，分别为线、面、体，R<sup>4</sup>及以上的物理意义就很难想象了；但是对应到C<sup>n</sup>，C<sup>1</sup>是面，但是C<sup>2</sup>及以上的物理意义就很难想象了；F<sup>n</sup>的n较大时，虽然物理意义很难想象，但是“代数”运算法则是不变的（所以叫“线性代数”，而非“线性几何”）；
* 用单个字母来表示含有n个元素的组，而不明确的写出每一个坐标，可以使F<sup>n</sup>上的代数运算表达式更加简洁；（在必须列出坐标时，可以使用该单个字母，加上适当下标的形式来表示；）向量的表示也是相同的逻辑；
* 向量的运算有4个：加法，标量乘法（标量当然包括复数），点积（高维空间的内积），叉积（在高维空间中无推广）；
* 通常说向量空间默认都是F上的（如果只说C、R上的会说明“复向量空间”、“实向量空间”）；
* 向量空间的定义：vector space就是带有加法和标量乘法的集合V，使得交换性、结合性、加法单位元、加法逆、乘法单位元、分配性这6个性质成立（及主要用到2种运算：加法，标量乘法（标量当然包括复数））；
* **1. 向量空间的定义，将向量空间的构成，从“组”拓展到“抽象的对象”，这些抽象的对象包括“函数、其他满足向量空间定义的稀奇古怪的对象”。  2. 因此，向量空间可以是关于多项式的，即多项式的集合。  3. 例如p(F)为系数在F中的所有多项式构成的集合，即所有多项式构成了向量空间。（也就是说只要多项式的系数属于F，那么该多项式都属于这个向量空间）**
* __记住多项式向量空间的加法与标量乘法的表示方式：(P+Q)(z) = P(z)+Q(z) z属于F、(aP)(z) = aP(z) z属于F。那么多项式向量空间的加法单位元是所有系数都为0的多项式。__





## 零散知识整理
1. 梯度向量：
（梯度（英语：gradient）是一种关于多元导数的概括[1]。平常的一元（单变量）函数的导数是标量值函数，而多元函数的梯度是向量值函数。多元可微函数f在点P上的梯度，是以f在P上的偏导数为分量的向量[2]。
  就像一元函数的导数表示这个函数图形的切线的斜率[3]，如果多元函数在点P上的梯度不是零向量，则它的方向是这个函数在P上最大增长的方向、而它的量是在这个方向上的增长率[4]。）
2. 正定矩阵：给定一个大小为 n*n 的实对称矩阵 A，若对于任意长度为 n 的非零向量 x ，有 x<sup>T</sup>Ax > 0 恒成立，则矩阵 A 是一个正定矩阵。
  半正定矩阵：给定一个大小为 n*n 的实对称矩阵 A，若对于任意长度为 n 的非零向量 x ，有 x<sup>T</sup>Ax >= 0 恒成立，则矩阵 A 是一个半正定矩阵。
  正定矩阵和半正定矩阵的直观解释：若给定任意一个正定矩阵 A 和一个非零向量 x ，则两者相乘得到的向量 y=Ax 与向量 x 的夹角恒小于 90度 . (等价于： x<sup>T</sup>Ax > 0 .)
3. 稀疏矩阵/稠密矩阵/稠密度/特殊矩阵：矩阵中非零元素的个数远远小于矩阵元素的总数，并且非零元素的分布没有规律，通常认为矩阵中非零元素的总数比上矩阵所有元素总数的值小于等于0.05时，则称该矩阵为稀疏矩阵(sparse matrix)，该比值称为这个矩阵的稠密度；与之相区别的是，如果非零元素的分布存在规律（如上三角矩阵、下三角矩阵、对角矩阵），则称该矩阵为特殊矩阵。
4. ## linear operation
* "AB"两个矩阵的“点乘”能成立的前提条件是“A的列数 == B的行数”。（而“A的行数”、“B的列数”这两个因素不用管）
5. 矩阵的秩：在线性代数中，一个矩阵 A 的列秩是 A 的线性无关的纵列的极大数目。类似地，行秩是 A 的线性无关的横行的极大数目。矩阵的列秩和行秩总是相等的，因此它们可以简单地称作矩阵 A 的秩。通常表示为 r ( A )， r a n k ( A ) 或 r k ( A )。 

# 线性代数工具

## dlqr()
* 离散lqr计算使用的Matrix Difference Riccati Equation，一般迭代几十次就可以收敛；
* Matrix Difference Riccati Equation有2种表示形式，但是不同表示形式的计算量不同（参考老王视频）；

## Eigen的使用
* 矩阵的定义形式有2种：Matrix<_Scalar, _Rows, _Cols, _Options, _MaxRows, _MaxCols>、Matrix2d；
  1. Matrix<_Scalar, _Rows, _Cols, _Options, _MaxRows, _MaxCols>的形式，只要指明3个参数_Scalar、_Rows、_Cols即可，其他的可不管。
  2. Matrix2d也有多种形式，具体形式如下：
  *\li \c Matrix2d is a 2x2 square matrix of doubles (\c Matrix<double, 2, 2>)
  *\li \c Vector4f is a vector of 4 floats (\c Matrix<float, 4, 1>)
  *\li \c RowVector3i is a row-vector of 3 ints (\c Matrix<int, 1, 3>)
  *
  *\li \c MatrixXf is a dynamic-size matrix of floats (\c Matrix<float, Dynamic, Dynamic>)
  *\li \c VectorXf is a dynamic-size vector of floats (\c Matrix<float, Dynamic, 1>)
  *
  *\li \c Matrix2Xf is a partially fixed-size (dynamic-size) matrix of floats (\c Matrix<float, 2, Dynamic>)
  *\li \c MatrixX3d is a partially dynamic-size (fixed-size) matrix of double (\c Matrix<double, Dynamic, 3>)
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
* 动态大小矩阵与固定大小矩阵
  Fixed-size means that the numbers of rows and columns are known are compile-time. In this case, Eigen allocates the array of coefficients as a fixed-size array, as a class member. This makes sense for very small matrices, typically up to 4x4, sometimes up to 16x16. Larger matrices should be declared as dynamic-size even if one happens to know their size at compile-time.
* _MaxRows and _MaxCols参数的使用
  In most cases, one just leaves these parameters to the default values.These parameters mean the maximum size of rows and columns that the matrix may have. They are useful in cases when the exact numbers of rows and columns are not known are compile-time, but it is known at compile-time that they cannot exceed a certain value. This happens when taking dynamic-size blocks inside fixed-size matrices: in this case _MaxRows and _MaxCols are the dimensions of the original matrix, while _Rows and _Cols are Dynamic.
* 文件CwiseNullaryOp.h中return type of the Ones(), Zero(), Constant(), Identity() and Random() methods
* block()的使用：block(Index startRow, Index startCol, Index blockRows, Index blockCols)中：
  1. /// \param startRow the first row in the block
  2. /// \param startCol the first column in the block
  3. /// \param blockRows the number of rows in the block
  4. /// \param blockCols the number of columns in the block
* 


