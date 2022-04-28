# 坐标系:
## [tf tree](https://blog.csdn.net/light_jiang2016/article/details/55517129) 
* TransForm 坐标变换（位置+姿态）。tf就是做坐标系的维护。例如一个可以拿酒瓶的机器人，有摄像头、关节、底座、胳膊、夹子等，实际使用时就需要摄像头的关节连在底座上，相对这个底座有个transform，需要把坐标回溯到底盘，然后再相对于胳膊，再相对于夹子（关节可能定义不止这么多，传导了很多层）。tf树就是所有这些部件组成的树型结构，tf树就是用做坐标系的维护。[机器人示例](./pic/tf_rob.png)
* [tftree](./pic/tf_tree.png)中有4个重要的tf坐标系：map，odom， base_footprint, base_link.
1. map是robot的全局坐标系， 原点上面已经说过了。
2. odom同样是个现实世界的固定坐标系，但他是变动的，是ros在运动前以当前观测到的数据建立的临时的坐标系，避免远离map原点而造成误差。
3. base_link是以底座中心为原点的坐标系，跟随robot而动，robot身上的任何零件都是已这个为母参考系的。
4. base_footprint是base_link坐标系在地面上的投影，就是z恒等于0的base_link,
* 说一些小的应用来理解下这四个坐标系:比如我要获取他前进的距离，就获取base_footprint 相对于odom的坐标，计算每次运动前后的差值就是运动的距离。再比如我想要获取目前机器人在地图上的坐标，那明显就要获取base_footprint 相对于map的坐标，然后在计算其像素坐标





