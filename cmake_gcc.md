# 1. control模块的编译过程：
1. 整理编译流程：整体编译入口是build.sh脚本。当执行“bash build.sh build_pc”后的执行流程如下：
* build.sh脚本 -> build_pc() -> build.sh同级目录下的CMakeLists.txt -> add_subdirectory(src)与add_subdirectory(unit_tests) -> 再分别执行src/CMakeLists.txt与unit_tests/CMakeLists.txt。
2. build_pc()中就执行了以下几步：
* mkdir -p build
* cmake -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR -DCMAKE_BUILD_TYPE=Release -DBUILD_SRC=ON -DBUILD_UNIT_TEST=ON -Bbuild -H.
* make -C build -j$(nproc) install  || { echo "$R -> Build failed! $E"  exit 1 }
* echo -e "$G -> Build release successfully! $TAIL $E"
  1. 结合[abseil库的安装-Ubuntu18.04](https://blog.csdn.net/qiuguolu1108/article/details/106445859)的具体流程可以知道，build.sh脚本就是把整个库的编译过程给写在了一起。包括“构建、安装”2个过程。
  2. 上述前2个步骤mkdir、cmake主要是通过cmake生成了CMaleLists.txt等编译用配置文件（如果该文件已经存在，就不会重复生成）
  3. 上述第3个步骤make，就是根据CMaleLists.txt等编译用配置文件进行编译；编译完成后再install。（install就是把生成的文件放置到指定的目录，就叫“安装”了。）
  4. 上述第4步，根据“编译、安装”结果进行输出提示信息。
3. 总结：
* 第三方库的编译，就可以采用将build_pc()每个步骤分开执行的方式去编译。如果中间需要增加什么细节，可以再执行完cmake步骤后，去CMaleLists.txt等生成文件中进行定制、修改。从而再进行make步骤。
* 同理，control的编译，直接修改相应的CMaleLists.txt等文件即可。具体的修改内容，参见下方的说明。

# 2. apollo build
1. 概述：
    Apollo uses ROS (Apollo 3.0 and before) and then change to Apollo Cyber RT (Apollo 3.5 and after). ROS use CMake as its build system but Cyber RT use bazel. In a ROS project, CmakeLists.txt and package.xml are required for defining build configs like build target, dependency, message files and so on. As for a Cyber RT component, a single bazel BUILD file covers. Some key build config mappings are listed below.
   Cmake与Bazel的两个示例的对应关系，见文档[CyberRT_Migration_Guide.md](https://github.com/ApolloAuto/apollo/blob/master/docs/cyber/CyberRT_Migration_Guide.md)
* For example, pb_talker and src/talker.cpp in cmake add_executable setting map to name = "talker" and srcs = ["talker.cc"] in BUILD file cc_binary.
2. Folder structure
    As shown below, Cyber RT remove the src folder and pull all source code in the same folder as BUILD file. BUILD file plays the same role as CMakeLists.txt plus package.xml. Both Cyber RT and Apollo ROS talker/listener example have a proto folder for message proto files but Cyber RT requires a separate BUILD file for proto folder to set up the proto library.
3. Apollo ROS与Apollo Cyber RT的一些api对应关系、tools的对应关系，在这里不是重点，不再赘述。

# 3. cmake使用说明：
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

## CMake各选项说明
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
7. add_executable：使用文件创建一個可執行文件，一般默認文件名與項目名相同。比如add_executable(pb_talker src/talker.cpp)，使用src/talker.cpp创建一个可执行文件pb_talker。
8. list:List operations.
  * list(APPEND <list> [<element> ...]): "APPEND" will append elements to the list.
  * list(REMOVE_ITEM <list> <value> [<value> ...])
    list(REMOVE_AT <list> <index> [<index> ...])
    :REMOVE_AT and REMOVE_ITEM will remove items from the list. The difference is that REMOVE_ITEM will remove the given items, while REMOVE_AT will remove the items at the given indices.

9. include: Load and run CMake code from a file or module.
    include(<file|module> [OPTIONAL] [RESULT_VARIABLE <VAR>]
                      [NO_POLICY_SCOPE])
10. install: This command generates installation rules for a project. Rules specified by calls to this command within a source directory are executed in order during installation. The order across directories is not defined.
* 选项：DIRECTORY、DESTINATION。
    Installing Directories。The DIRECTORY form installs contents of one or more directories to a given destination. 
11. file:File manipulation command.
* file(GLOB_RECURSE <variable> [FOLLOW_SYMLINKS]
     [LIST_DIRECTORIES true|false] [RELATIVE <path>]
     [<globbing-expressions>...])
  Generate a list of files that match the <globbing-expressions> and store it into the <variable>. Globbing expressions are similar to regular expressions, but much simpler. If RELATIVE flag is specified, the results will be returned as relative paths to the given path. The results will be ordered lexicographically.
12. add_library:Add a library to the project using the specified source files.
add_library(<name> [STATIC | SHARED | MODULE]
            [EXCLUDE_FROM_ALL]
            source1 [source2 ...])
  Adds a library target called <name> to be built from the source files listed in the command invocation. The <name> corresponds to the logical target name and must be globally unique within a project. The actual file name of the library built is constructed based on conventions of the native platform (such as lib<name>.a or <name>.lib).
  **STATIC, SHARED, or MODULE** may be given to specify the type of library to be created. STATIC libraries are archives of object files for use when linking other targets. SHARED libraries are linked dynamically and loaded at runtime. MODULE libraries are plugins that are not linked into other targets but may be loaded dynamically at runtime using dlopen-like functionality. If no type is given explicitly the type is STATIC or SHARED based on whether the current value of the variable BUILD_SHARED_LIBS is ON.
13. aux_source_directory(<dir> <variable>): Find all source files in a directory.
  Collects the names of all the source files in the specified directory and stores the list in the <variable> provided. This command is intended to be used by projects that use explicit template instantiation. Template instantiation files can be stored in a “Templates” subdirectory and collected automatically using this command to avoid manually listing all instantiations.
14. 



# 4. 编译过程分析：
1. 一般来说.so文件就是常说的动态链接库, 都是C或C++编译出来的。Linux下的.so文件时不能直接运行的,一般来讲,.so文件称为共享库
2. /usr/bin/ld: cannot find -lxxx 的解决办法
  1. 示例：/usr/bin/ld: cannot find -lhdf5
这表示找不到库文件 libhdf5.so，若是其它库文件，则是 cannot find -lxxx 了，其中 xxx 是库文件的名字。
  2. 解决方法
  * 安装此库文件和相关软件：一般库文件属于某个软件，google搜索该软件并安装，或者使用 yum 安装。
  * 将库文件所在路径添加到gcc的搜索路径：
（1）使用命令"$ gcc -lhdf5 --verbose"查询gcc能否搜寻到指定的库文件；若安装了软件，找到了库文件的路径。但是依然会提示上述错误。则表示gcc的搜索路径不包含该库文件所在的路径。将库文件所在的路径加入到搜寻路径中的方法为：
（2） 使用 /etc/ld.so.conf 配置文件
将库文件所在的路径加入到 /etc/ld.so.conf 尾部，并使之生效：
$ sudo echo '/opt/biosoft/hdf5-1.8.15-patch1/lib/' >> /etc/ld.so.conf
//libhdf5.so 在路径 /opt/biosoft/hdf5-1.8.15-patch1/lib/ 下，将该路径加添加到配置文件中
$ sudo ldconfig
//运行该命令，重新载入 /ext/ld.so.conf 中的路径，使修改生效。
（3）修改环境变量
$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/biosoft/hdf5-1.8.15-patch1/lib/
//修改环境变量 LD_LIBRARY_PATH，加入库文件所在路径。使用 export 命令使修改生效。
$ echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/biosoft/hdf5-1.8.15-patch1/lib/' >> ~/.bashrc
$ source ~/.bashrc
//将上述 export 命令加入到配置文件 ~/.bashrc，使之永久生效。
$ export LIBRARY_PATH=/opt/biosoft/hdf5-1.8.15-patch1/lib/:$LIBRARY_PATH
//若修改变量 LD_LIBRARY_PATH 不奏效，则修改变量 LIBRARY_PATH 。
3. .o, .a, .so文件和可执行文件解释：
* .o 就相当于windows里的obj文件 ，一个.c或.cpp文件对应一个.o文件
* .a 是好多个.o合在一起,用于静态连接 ，即STATIC mode，多个.a可以链接生成一个exe的可执行文件
* .so 是shared object,用于动态连接的,和windows的dll差不多，使用时才载入。



# 参考文献：
1. [CMake官方文档](https://cmake.org/cmake/help/v3.10/command/target_link_libraries.html)
2. [cmake-gtest單元測試](https://ppfocus.com/0/ed6850c98.html)
3. [CMake应用：从编译过程理解CMake](https://zhuanlan.zhihu.com/p/385152470)
4. [CyberRT_Migration_Guide.md](https://github.com/ApolloAuto/apollo/blob/master/docs/cyber/CyberRT_Migration_Guide.md)
5. [/usr/bin/ld: cannot find -lxxx 的解决办法](https://www.cnblogs.com/zhming26/p/6164131.html)
6. [abseil库的安装-Ubuntu18.04](https://blog.csdn.net/qiuguolu1108/article/details/106445859)







