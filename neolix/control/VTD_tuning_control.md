# 概述
## 仿真内容概述
1. 需要启动4个内容：dv、dv monitor(起停算法模块)、sim bridge、sim driver；
2. 
3. docker:  root@autobot_test:/home/caros/scripts；
4. 各模块源码都在服务器目录“/home/caros/autobot/neolix/”下面；
5. 个模块的编译也需要在服务器的docker中进行。
## 常用命令
1. "sim bridge"的关闭，使用“ctrl + \”；
2. "sim driver"的关闭，使用“pnc@pnc:/home/caros/autobot/scripts$ ./driver_stop.sh”；
3. 
## 常用设置
1. 仿真场景的配置，需要修改文件“pnc@pnc:/home/caros/autobot/scripts/scenarios$ vim TestBase_gen1.xml”
2. ~/VIRES/VTD.2021.4/Data/Projects/SimProject_yz/Scenarios/1-cruising$

## 需要验证问题：
**主要3个目的：逻辑运行是否正常、怎么分析问题、性能评价标准**
1. 看仿真情况下，control收到planning的时间戳是否正常；
2. 在仿真情况下，分析如下*种情况的性能。
  1. 不带预瞄；
  * 使用延时滞后控制器；
  * 不使用延时滞后控制器；
  2. 带预瞄；
  * 使用延时滞后控制器；
  * 不使用延时滞后控制器；
3. 在学亮分析工具的基础上，添加张博的那个最大误差评价标准的统计。








