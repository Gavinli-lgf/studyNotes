(V2Ray客户端)[https://itlanyan.com/v2ray-clients-download/]
V2Ray是近几年兴起的科学上网技术，采用新的协议，因功能强大、能有效抵抗墙的干扰而广受好评。V2Ray官网是 https://v2ray.com(V2fly社区官网是 https://www.v2fly.org/)，目前已无法直接打开。

1. V2Ray是一种技术，而现有的这些工具，都是基于这种技术开发的。
2. V2rayN和Qv2ray等都是一些第三方工具，是在V2ray官方内核的基础上开发的。（所以这些工具如果包含了V2ray的核，就不需要重新单独下载；否则下载了这些第三方工具后，还要单独下载V2ray的核。）
3. V2ray使用vmess协议。
4. Qv2ray除了支持V2ray的vmess协议外，还可以通过安装插件的方式，额外增加对SS/SSR/Trojan等代理协议的支持，可作为V2ray/SS/SSR/Trojan客户端使用。(相当于Qv2ray这个第三方工具，通过插件的形式，可以当作多种代理协议的客户端使用。不只是V2ray的客户端。)
5. 代理协议有很多种，V2ray的Vmess只是其中一种。
6. Qv2ray自身相当于一个外壳，并不包含V2ray内核。在作为V2ray客户端使用时，需要另外下载V2ray官方内核搭配使用。（同第2点说明，就是一个第三方工具。）
7. 默认情况下，Qv2ray并不支持V2ray以外的代理协议，因此在作为SS/SSR/Trojan等客户端使用前，需要在Qv2ray中添加相应插件（注意插件版本号和Qv2ray版本号要对应）。

8. Qv2ray使用的基本步骤：所以Qv2ray的使用步骤如下：先下载Qv2ray工具 -> 下载v2ray内核 -> 将内核v2ray导入Qv2ray -> 安装插件(可选) -> 给Qv2ray添加代理服务器（所以在[gatern](https://gatern.com)上买的仅仅是代理节点）-> 如果安装了其他代理协议的内核，这里也可以添加其他协议的代理服务器（可选）
9. 客户端需要配置/购买 v2ray节点 才能上外网
10. Qv2ray常用菜单设置




Qv2ray使用错误日志：
1. 显示启动时，显示Cannot Start Qv2ray,对下面3个目录没有写权限；
2. 显示加载配置文件失败。弹窗见手机；日志如下：
V2Ray 4.22.1 (V2Fly, a community-driven edition of V2Ray.) Custom (go1.13.5 linux/amd64)
A unified platform for anti-censorship.
main: failed to load config: generated/config.gen.json > v2ray.com/core/main/confloader/external: config file not readable > open generated/config.gen.json: no such file or directory


解决方案：
1. 权限问题：
  sudo chown root Qv2ray.v2.7.0.AppImage
  sudo chgrp root Qv2ray.v2.7.0.AppImage

2. 大概率是Qv2ray的安装问题，重新安装试试。


20220604
[Linux怎么配置Qv2ray](https://iyuantiao.com/fenxiangfuli/jiaocheng/v2ray.html#:~:text=Qv2ray%20%E6%98%AF%E4%B8%80%E4%B8%AA%E7%94%A8%20Qt%20%E7%BC%96%E5%86%99%E7%9A%84%E8%B7%A8%E5%B9%B3%E5%8F%B0%20v2ray%20%E5%9B%BE%E5%BD%A2%E5%89%8D%E7%AB%AF%EF%BC%8C%E7%9B%AE%E5%89%8D%E6%94%AF%E6%8C%81%E7%9A%84%E7%89%88%E6%9C%AC%E6%98%AF%20v2.7.0-pre2%E3%80%82%20%E6%94%AF%E6%8C%81Linux,%E4%BD%BF%E7%94%A8%20C%2B%2B%20%2F%20Qt%20%E5%BC%80%E5%8F%91%20%7C%20%E5%8F%AF%E6%8B%93%E5%B1%95%E6%8F%92%E4%BB%B6%E5%BC%8F%E8%AE%BE%E8%AE%A1%E3%80%82%20%E4%BA%8C%E3%80%81%E4%B8%8B%E8%BD%BD%E5%8F%8A%E9%85%8D%E7%BD%AEQV2ray%EF%BC%9A)
1. Qv2ray目前支持版本是v2.7.0-pre2，



