# 线性代数理论
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


