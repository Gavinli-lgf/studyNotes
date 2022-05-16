# 线性代数理论
## Liner Algebra Done Right
1. **向量空间（复数、向量空间的定义、向量空间的性质）**
* 有限维向量空间，线性映射；实数、复数与域field（以后考虑运算性质都是指F域的）；
* 标量包括“复数”（与实数），标量与向量相对；向量、组(tuple)的概念；组的长度是有限的，且长度是一个非负整数（可以为0）；组与集合的区别；F<sup>n</sup>为F域上的高维组（n为正整数，F也包括R、C）；R<sup>1</sup>、R<sup>2</sup>、R<sup>3</sup>的几何模型很明显，分别为线、面、体，R<sup>4</sup>及以上的物理意义就很难想象了；但是对应到C<sup>n</sup>，C<sup>1</sup>是面，但是C<sup>2</sup>及以上的物理意义就很难想象了；F<sup>n</sup>的n较大时，虽然物理意义很难想象，但是“代数”运算法则是不变的（所以叫“线性代数”，而非“线性几何”）；
* 用单个字母来表示含有n个元素的组，而不明确的写出每一个坐标，可以使F<sup>n</sup>上的代数运算表达式更加简洁；（在必须列出坐标时，可以使用该单个字母，加上适当下标的形式来表示；）向量的表示也是相同的逻辑；
* 向量的运算有4个：加法，标量乘法（标量当然包括复数），点积（高维空间的内积），叉积（在高维空间中无推广）；
* 通常说向量空间默认都是F上的（如果只说C、R上的会说明“复向量空间”、“实向量空间”）；
* 向量空间的定义：vector space就是带有加法和标量乘法的集合V，使得交换性、结合性、加法单位元、加法逆、乘法单位元、分配性这6个性质成立（及主要用到2种运算：加法，标量乘法（标量当然包括复数））；
* **1. 向量空间的定义，将向量空间的构成，从“组”拓展到“抽象的对象”，这些抽象的对象包括“函数、其他满足向量空间定义的稀奇古怪的对象”。  2. 因此，向量空间可以是关于多项式的，即多项式的集合。  3. 例如p(F)为系数在F中的所有多项式构成的集合，即所有多项式构成了向量空间。（也就是说只要多项式的系数属于F，那么该多项式都属于这个向量空间）**
* __记住多项式向量空间的加法与标量乘法的表示方式：(P+Q)(z) = P(z)+Q(z) z属于F、(aP)(z) = aP(z) z属于F。那么多项式向量空间的加法单位元是所有系数都为0的多项式。__
  3. 向量空间的性质
* 向量空间有唯一的加法单位元（类似叫法还有“乘法单位元”）；
* 向量空间中的每个元素都有唯一的加法逆；
* 之后定理证明中说的“向量空间”，均指“F”上的向量空间；
* 对每一个v属于V，都有0v=0;(左边0属于F，右边0属于V)
* ...
  4. 子空间（有的叫“线性子空间”）
* U是V的子集，要验证U是否构成一个“子空间”/“线性子空间”，需要验证U满足如下3个性质：加法单位元、对加法封闭、对标量乘法封闭；（向量空间的其他性质在上述性质基础上都是自然成立的）
* 空集是{},而不是{0}；{0}是V的最小子空间，V自身是V的最大子空间；向量空间至少要包含一个元素，即加法单位元；
* 实例：R<sup>2</sup>的子空间有且只有以下3种：{0}、R<sup>2</sup>自身、R<sup>2</sup>中所有过原点的直线；R<sup>3</sup>的子空间有且只有以下4种：{0}、R<sup>3</sup>自身、R<sup>3</sup>中所有过原点的直线、R<sup>3</sup>中所有过原点的平面；
  5. 和与直和（操作对象是：向量空间）
* 和： U<sub>1</sub> ， ... ， U<sub>m</sub>的和U<sub>1</sub> + ... + U<sub>m</sub>，定义为U<sub>1</sub> ， ... ， U<sub>m</sub>中元素所有可能的和所构成的集合。
* 研究向量空间，研究的是“子空间”，而不是任意子集；因为子空间的和，不等于子空间的并集；
* U<sub>1</sub> + ... + U<sub>m</sub>是V中包含U<sub>1</sub> ， ... ， U<sub>m</sub>的最小的子空间。
* 直和：如果V的每个元素都可以“唯一”的写成u<sub>1</sub> + ... + u<sub>m</sub>，其中u<sub>j</sub>属于U<sub>j</sub>，则称V是子空间U<sub>1</sub> ， ... ， U<sub>m</sub>的直和，记为“圈加内部的+号”。（1. 直和符号提醒我们这是特殊类型的子空间和; 2. 不满足唯一性，也不叫直和。）
* 直和对于多项式组成的向量空间也同样成立。
* 1.8 命题：设U<sub>1</sub> ， ... ， U<sub>m</sub>都是V的子空间，则 V = U<sub>1</sub> (+) ... （+） U<sub>m</sub>，当且仅当如下两个条件成立：（1）V = U<sub>1</sub> ， ... ， U<sub>m</sub>；（2）若0 = u<sub>1</sub> + ... + u<sub>m</sub>，u<sub>j</sub>属于U<sub>j</sub>，则每个u<sub>j</sub>都为0。
* “1.8 命题”将“和”、“直和”之间构建了联系；且联系就是0向量表示成时当向量和时表示法的唯一性，即每个分向量都是0。（所以，“和”、“直和”的区别就在“唯一性”上。）
* 1.9 命题：只有2个子空间时，将直和与交集之间建立了联系。
2. **有限维向量空间**
线性代数所关注的只是“有限维向量空间”，有限维向量空间的重要概念有：张成、线性无关、基、维数。
  1. 张成与线性无关：
* （线性）张成（span）:V中一组向量（v<sub>1</sub> , ... , v<sub>m</sub>）的线性组合所构成的集合称为（v<sub>1</sub> , ... , v<sub>m</sub>）的张成。（线性组合的系数都属于F）。
* V中任意一组向量的张成都是V的子空间（为了一致性，声明：空组()的张成等于{0}）。  V中一组向量的张成是包含这组向量的最小子空间。
* 有限维：如果一个向量空间可以由它的一组向量张成，则称该向量空间是有限维的（finite dimensional）。
* 多项式向量空间的表示方法：P<sub>m</sub>(F)，其中m为非负整数，式子表示：系数在F中并且次数不超过m的所有多项式所组成的集合。P<sub>m</sub>(F)是P(F)的子空间。  （不关注无限维向量空间，这是“泛函分析(functional analysis)”所关注的内容；线性代数不关注。）
* 线性无关：V中的一组向量（v<sub>1</sub> , ... , v<sub>m</sub>）的线性组合为0，只有所有系数都为0时才成立，则称该组向量（v<sub>1</sub> , ... , v<sub>m</sub>）是线性无关的。  （从向量无关的组中去除一些向量后，生于的向量组依然即时线性无关的。因此，人为声明空组{}也是线性无关的。）
* 一组向量线性无关，则该组向量的span中的每一个向量，都可以用该组向量的线性组合来唯一的表示。
* 线性相关：不是线性无关，就是线性相关。
* 线性相关性引理：“线性相关”与“线性无关”之间的关系。（具体看书）
* 在有限维向量中，线性无关向量组的长度小于等于张成向量组的长度。
* 有限维向量空间的子空间都是有限维的。
  2. 基
* 若V中的一个向量组既是向量无关的，又张成V，则称之为V的基（basis）。  标准基。
* 一个向量组（v<sub>1</sub> , ... , v<sub>m</sub>）是V的基，当且仅当V中的每一个向量都能用该向量组唯一的表示。
* 在向量空间中，每个张成组都可以化简成一个基。（因为张成组可以是线性相关或线性无关的，如果是线性无关，那其本身就是一个基；如果线性相关，那么总能把其中某个去掉后形成一个基，仍然张成为同一个向量空间。）
* 每个有限维向量空间都有基
* 在有限维向量空间中，每个线性无关向量组都可以拓充成为一个基。
* 设V是有限维的，U是V的一个子空间，则存在V的一个子空间W，是的V是U和W的直和。
  3. 维数
* 有限维向量空间的任意两个基的长度都相同。 任意基的长度称为这个向量空间的维数。
* 特别注意：多项式的维数。 dimP<sub>m</sub>(F) = m + 1 。（即多项式的维数是最高次幂 + 1）
* V是有限维的，并且U是V的子空间，则dimU <= dimV。
* 若V是有限维的，则V中每个长度为dimV的张成向量组都是V的一个基。（也说明了这个长度为dimV的张成向量组是线性无关的）
* 与上同理：若V是有限维的，则V中每个长度为dimV的线性无关向量组都是V的一个基。
* 如果U1 U2都是同一个向量空间的子空间，那么“dim(U1 + U2) = dimU1 + dimU2 - dim(U1交U2)”。
* “直和”与“维数”间的关系：
  设V是有限维的，并且U1，...，U<sub>m</sub>，是V的子空间，使得V = U1 + ... + U<sub>m</sub>，且dimV = dimU1 + ... + dimU<sub>m</sub>，那么V一定是U1，...，U<sub>m</sub>的直和。
3. **线性映射**
向量空间 -> 线性映射（线性变换）
* 线性映射就是一个函数T，实现从“向量空间V -> 向量空间W”的映射，该映射满足以下2个性质：加性(addivity)、齐性(homogeneity)。
* 从向量空间V到向量空间W的所有线性映射所构成的集合记为L(V,W)。







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


