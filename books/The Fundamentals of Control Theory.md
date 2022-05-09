# notes of <The Fundamentals of Control Theory>

## Convolution Integral
* "Since we have the area under this slice we can replace just this small section
of f (t) with a single scaled impulse function. "这句话就把一个“连续输入函数f(t)”，划分成无数个脉冲函数，每个脉冲就是“f(dτ)·dτ·δ(t−dτ)”，即对dτ时刻的脉冲“δ(t−dτ)”，进行“f(dτ)·dτ”倍的缩放。（脉冲函数的缩放，参照P52页对δ(t)与1/2·δ(t−T)的解释）
* MATLAB的conv()函数，是卷积和多项式乘法函数，返回向量u 和v 的卷积。如果u 和v 是多项式系数的向量，对其卷积与将这两个多项式相乘等效。
* Convolution gives us the ability to determine an LTI system’s response to any arbitrary input as long as we know the impulse response of the system.即：用LTI系统的脉冲响应函数f，与LTI系统的输入函数g做卷积，就能得出LTI在输入g下的输出响应(f*g)(t)。

* the convolution integral seems pretty messy and preforming that integration for arbitrary inputs would be overly cumbersome.  We can perform convolution with transfer functions as well, but the good news is that we do that using multiplication rather than integration. So  we need to leave the comfort of the time domain and venture out into the frequency domain.  ==> next topic:The Frequency Domain and the Fourier Transform.

## The Frequency Domain and the Fourier Transform
* Fourier transform maps a continuous signal in the time domain to its continuous frequency domain representation: maps functions f (t) and g(t) to F(ω) and G(ω).
*  the inverse Fourier transform, to map from the frequency domain back to the time domain.
* what is the Fourier transform of (f∗g)(t)? : the Fourier transform of convolution is just the multiplication of the individual Fourier transforms.
  1.  Fourier transform of g(t−τ), or the delay constant e<sub>−jωτ</sub> times G(ω).
  2. When you’re working in the frequency domain and you multiply two functions you are really accomplishing the same result as convolution in the time domain.
  3.  if you have a frequency domain representation of your system’s impulse response and arbitrary input signal then you can calculate the system’s response to that input by multiplying the two.
* Transfer functions are not represented entirely in the frequency domain,however. They are in a higher order domain called the s domain where one dimension is in fact frequency, but the second dimension is exponential growth and decay. 

## The s domain and the Laplace Transform
* [common Fourier transforms](https://blog.csdn.net/Varalpha/article/details/104964650),[pic](./appendix/Fourier_transforms.png) you’ll find that for both Fourier transforms and Laplace transforms you’ll more often than not just memorize the common ones or look up the conversion in a table. 
* calculating the magnitude and phase is a matter of converting the rectangular coordinate representation, which are the real and imaginary parts, to polar coordinate representation.即：将时域信号经过傅立叶变换转换成频域信号后，有2种表示方法：(1)用两个直角坐标系图分别表示幅值与频率、相位与频率的关系；(2)用一个极坐标系，表示幅值与相位之间的关系，而频率值没那么明显，需要根据公式反推一下。
* take a one-dimensional time domain function, and turn it into a two-dimensional frequency domain function.the two dimensions are the real and imaginary components which, through some additional algebra, are the magnitude and phase of the cosine waves that make up the original time domain function.
* The Laplace transform takes the idea of the Fourier transform one step further. 

## The s Plane
* Instead of just cosine waves, the Laplace transform decomposes a time domain signal into both cosines and exponential functions. 
* s is a complex number, which means that it contains values for two dimensions; one dimension that describes the frequency of a cosine wave and the second dimension that describes the exponential term. It is defined as s = σ + jω. 
* Therefore, the equation e<sup>st</sup> is really just an exponential function
multiplied by a sinusoid, e<sup>st</sup> = e<sup>(σ+jω)t</sup> = e<sup>σt</sup> e<sup>jωt</sup> .
* The value of s provides a location in this plane and describes the resulting signal, est , as function of the selected ω and σ .(the real axis is the exponential line and the imaginary axis is the frequency line)
* 

## The Laplace Transform
* Laplace transform and Fourier transform are Mathematically exceedingly similar,but they are used in different way.Obviously, the difference is that we’ve replaced jw with s(s = σ + jω). (1) Fourier transform maps time to frequency; (2) Laplace transform maps time to s. 
* If σ = 0 on S plane, the Laplace transform for values of s along imaginary axis is exactly equal to the Fourier transform.
* Remember that the results of the Fourier transform are a set of two-dimensional numbers that represent magnitude and phase for a given frequency. The results of the Laplace transform are still the same two-dimensional numbers,but now we plot them on a 3-dimensional s plane rather than just the along the frequency line.
* In fact, that is exactly what we’re doing with the Laplace transform; we’re probing the time domain function with e−st across the entire s plane to see what it’s made of. We are basically breaking it down into its base frequencies and exponential properties.
* [Laplace性质](./appendix/laplace1.png)、[常见Laplace变换](./appendix/laplace2.png)、[reference](https://blog.csdn.net/qq_29695701/article/details/105993116)
* The Fourier transform decomposes a function into sinusoids. Then the Laplace transform decomposes a function into both sinusoids and exponentials.
* The important thing to note is that the solution of ordinary differential equations can only consist of sinusoids and exponentials. That’s because they are the only wave forms that don’t change shape when subjected to any combination of the six legal operations. (所以Laplace变换将信号分解成正弦信号、指数信号。也就是e<sup>st</sup>形式)
* So it makes sense that we are defining a system’s impulse response in terms of these wave forms and only these waveforms. The ubiquity of these types of physical relationships is why the Laplace transform is one of the most important techniques you’ll learn for system analysis.
* 

## Putting this all Together: Transfer Functions
* Per the definition of a transfer function, we need to take the Laplace transform of the impulse response of our system. (So we set the single input to an impulse function, F<sub>input</sub>(t) = δ(t), and solve for the response, x(t).)
  1. Solving linear, ordinary differential equations in the time domain can be time consuming. We can make the task easier by taking the Laplace transform of the entire differential equation, one term at a time, and solve for the impulse response in the s domain directly.
  2. we multiply in the s domain it is the same as convolution in the time domain. Therefore,when we did the division to solve for X(s) we were really doing a deconvolution operation in the time domain.This is the power of manipulating system models in the s domain. Every time you perform a simple multiplication or division with a transfer function just imagine the complicated mathematics that would have had to occur in the time domain to produce the same result.
*  We can use the fact that we can multiply and divide transfer functions to simplify the feedback loops in systems, and by simplifying them we can start to understand how they affect the larger system.


# 3 Block Diagrams
## 3.2 The nomenclature (let’s all speak the same language)
seven nomenclatures:arrows, blocks, summing junctions, take off points, nodes, paths, loops.
1.  transfer functions are Single-Input, Single-Output (SISO) functions so it doesn’t make sense to have a block diagram with multiple inputs or multiple outputs.(也就是说，传递函数不仅整个系统是单输入单输出；就连系统中的每个传递函数的block，也都是SISO。但是传递函数系统框图中也能见到多输入多输出的框图，这些框图往往仅是一些简单的数学运算For example, a system might take the two inputs and simply multiply them together to generate the single output.但是这种运算框可以使用“Summing junctions and take off points”替换)。
    State space representation does allow for multi-input, multi-output system.
2. It is helpful to give names to and define some of the patterns that come up often in block diagrams.(Because even though the diagram above consists of only 4 different symbols, there is additional complexity in the patterns that are created. )
3. Nodes are different from blocks. Summing junctions and blocks create new nodes (because they change the signal) but take off points do not. 
4. two different paths:The forward path, Parallel paths.
5. Four loop types:a closed loop system,  cascaded loops, Non-touching loops, overlapping or interlocked loops. (The classic feedback system is often called a closed loop system and you can see how it clearly meets the definition of a loop.)
6. SUMMARY: The thing to remember is that block diagrams are created using just four symbols; arrows,
blocks, take off points, and summing junctions. The rest of the terms we covered, and most of the complexities of block diagrams, come from the patterns that emerge from those four symbols.
## 3.3 Block diagram algebra
* remember that the algebra rules we will cover here are only possible if the system is LTI and that the systems
are represented by transfer functions - that is, in the s domain.
### 3.3.1 Why is LTI necessary?
* Remember that LTI systems obey the properties of homogeneity, superposition, and time invariance. These properties are what allow us to move blocks around and simplify diagrams.
* swapping the order of the blocks has no impact on the output.(but but the intermediate signals do change, and frequently lose their real physical meaning.)
### 3.3.2 Why are transfer functions necessary?
...





