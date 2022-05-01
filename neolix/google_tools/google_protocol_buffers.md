# Protocol use method
## 命名空间
* 每个'.proto'文件开头，使用'package'声明本文件所归属的命名空间。例如global_adc_status.proto文件开头，使用‘package neodrive.global.status;’声明本文件在‘neodrive::global::status’命名空间中。
* '.proto'文件中每定义一个'message'就会生成一个类class，比如global_adc_status.proto文件中定义了'message Chasis{}',那么就会生存类'class Chasis'。
* 同上，'class Chasis{}'的命名空间就是‘neodrive::global::status::Chasis’。此时C++源码中想使用'message Chasis{}'中定义的消息，就可以使用‘using neodrive::global::status::Chasis;’的方式进行命名空间声明。
1. 
2. 


