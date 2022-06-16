# cmake使用说明：
以Apollo中常见的CMakeLists.txt文件为例，说明使用过程：
## 概述
    CMake是一個跨平台的編譯工具，可以用簡單的語句來描述所有平台的編譯過程，可以根據不同平台、不同的編譯器，生成相應的MakeFile或者vcproj文件，爲項目的跨平台開發提供了便捷。CMake的所有的語句都寫在CMakeLists.txt的文件中。在CMakeLists.txt文件中可以用cmake命令對相關的變量值進行配置，配置完成後，應用cmake命令生成相應的makefile或者project文件。
    
1. gcc与CMake的对应关系
    GCC的编译的具体过程其实是通过gcc命令的参数进行控制的，这些参数的作用就和CMake的命令有对应的关系。GCC的编译过程大概是：
* 预处理：将源文件处理为.ii/.i，处理各种预处理指令，如#include、#ifdef、#if等等，同时也会清除注释；
* 编译：将.ii/.i处理为.S/.asm，即机器语言的汇编文件；
* 汇编：将.asm/.S处理为.o，把汇编文件变成机器码；
* 链接：将各种依赖的静态/动态库文件、.o文件、启动文件链接成最终的可执行文件或者共享库文件。

2. 整体使用流程：

## 各选项说明
1. add_subdirectory：
    如果要在现有工程目录下，增加使用gtest工具，有2个问题需要考虑：（1）gtest的源码放在哪里？（2）怎么将gtest的编译工作放在整个工程的编译工作中？
    例如，如果当前项目中有src/目录，改目录下原有一个CMakeLists.txt文件，为src/CMakeLists.txt。并且想把gtest源码也放在src/目录下。那么第（1）个问题已经解决。
    第（2）个问题就需要执行2步操作。首先在src/CMakeLists.txt文件中增加一句“add_subdirectory("gtest")”，然后再在src/gtest/目录下再新建一个CMakeLists.txt文件，为src/gtest/CMakeLists.txt，来执行gtest的编译。
    如此，就將gtest和test子項目添加到總項目的編譯列表中。在項目編譯時便會一起編譯gtest和test子項目。
2. cmake_minimum_required：定義項目要求的cmake最低版本；
    例如：cmake_minimum_required(VERSION 3.10)
3. project：給測試項目命名，編譯成功之後便是測試項目的文件名
    例如：project(aeb)
4. set(CMAKE_CXX_STANDARD/CMAKE_CXX_STANDARD_REQUIRED)：設置C++標準；
5. message(STATUS )：編譯過程正常輸出語句」C++ 11 support …」；**就像是输出log日志一样，要充分使用。**
6. 例如：file(GLOB_RECURSE SRCS "${CMAKE_CURRENT_SOURCE_DIR}/*.cc")
    將${CMAKE_CURRENT_SOURCE_DIR}文件夾下所有的編碼文件（*.cc）組成一個列表，並存儲在變量SRCS中，後續便可以使用${SRCS}代表這些文件；
7. 预处理相关：
* add_definitions：
    对于gcc，使用“gcc -D UPPER_CASE ...”；而在CMake中，可以使用命令：add_definitions(-D UPPER_CASE)。相当于源码中对如下代码的处理：
#ifdef UPPER_CASE
#define name "REAL_COOL_ENGINEER"
#else
#define name "real_cool_engineer"
8. 编译相关：
    在编译的时候，需要把源文件处理成机器代码，主要有两个方面：（1）对于源文件里面的代码具体怎样进行编译？（2）源文件内部调用的外部函数怎么查找？
    对于gcc有很多选项可以设置，对应CMake，主要是add_compile_options、include_directories两个选项：
* 使用add_compile_options命令指定编译选项；
* 使用include_directories命令指定头文件搜索路径；
    示例：
add_compile_options(-Os -g -Wall -Wextra -pedantic -Werror)
include_directories(src/c)
9. 链接相关：
    链接需要做的就是把最终目标依赖的东西都组装起来。对于这里的可执行文件来说，先从demo.o的main函数开始，链接整个程序执行过程中需要的所有函数的实现；不同实现可能在不同的.o文件或者库文件内，通过头文件声明的函数名，在.o和.a文件里面查找需要的实现；如果找不到，就会引发一个链接错误。
    对于gcc而言，项目内部的构建目标库文件及其他的.o文件，在链接的时候直接使用即可，而对于外部的第三方库或者系统的库文件，则需要使用-L和-l参数来告知链接器。
    对应地，CMake对应可以使用的命令为：
* 对于-L，使用link_directories或者target_link_directories命令；
* 对于-l，使用link_libraries或者target_link_libraries命令；
* 指定链接器的选项，使用add_link_options或者target_link_options命令。
上述命令中，以target_开头的是针对特定的目标进行设置，否则是针对所有的目标。
7. add_executable：使用${...}存儲的文件爲項目構建一個可執行文件，一般默認文件名與項目名相同，比如ProjectTest.exe；
8. 
9. 





参考文献：
1. [CMake官方文档](https://cmake.org/cmake/help/v3.10/command/target_link_libraries.html)
2. [cmake-gtest單元測試](https://ppfocus.com/0/ed6850c98.html)
2. [CMake应用：从编译过程理解CMake](https://zhuanlan.zhihu.com/p/385152470)






