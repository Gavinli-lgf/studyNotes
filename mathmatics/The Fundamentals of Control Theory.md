# notes of <The Fundamentals of Control Theory>

## Convolution Integral
* "Since we have the area under this slice we can replace just this small section
of f (t) with a single scaled impulse function. "这句话就把一个“连续输入函数f(t)”，划分成无数个脉冲函数，每个脉冲就是“f(dτ)·dτ·δ(t−dτ)”，即对dτ时刻的脉冲“δ(t−dτ)”，进行“f(dτ)·dτ”倍的缩放。（脉冲函数的缩放，参照P52页对δ(t)与1/2·δ(t−T)的解释）
* MATLAB的conv()函数，是卷积和多项式乘法函数，返回向量u 和v 的卷积。如果u 和v 是多项式系数的向量，对其卷积与将这两个多项式相乘等效。
* Convolution gives us the ability to determine an LTI system’s response to any arbitrary input as long as we know the impulse response of the system.即：用LTI系统的脉冲响应函数f，与LTI系统的输入函数g做卷积，就能得出LTI在输入g下的输出响应(f*g)(t)。

* the convolution integral seems pretty messy and preforming that integration for arbitrary inputs would be overly cumbersome.  We can perform convolution with transfer functions as well, but the good news is that we do that using multiplication rather than integration. So  we need to leave the comfort of the time domain and venture out into the frequency domain.  ==> next topic:The Frequency Domain and the Fourier Transform
## The Frequency Domain and the Fourier Transform

