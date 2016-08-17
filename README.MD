#elk_auto_deploy
版本 v1.0

这是一个用于自动部署 “ELK 日志分析平台” 的 python fabric 项目。

它针对的 “ELK 日志分析平台” 架构如下：

[shipper]     [broker]     [index]      [search & storage]   [web-interface] 
filebeat ====> redis ====> logstash ====> elasticsearch =======> kibana    

如上面所示，
filebeat部署多个，分别部署于各个需要被监控日志的服务器上。
Redis部署一个，部署于独立的服务器上。
logstash部署多个，各自部署于独立的服务器上。
elasticsearch部署多个，各自部署于独立的服务器上，构成集群。
kibana部署一个，部署于独立的服务器上。

elk_auto_deploy 实现的功能有：
- 自动部署
根据上述架构，自动部署组件服务，包括 elasticsearch、logstash、kibana、redis 
- 自动调优
自动对各个组件进行性能调优，包括系统调优、组件配置调优
- 统一管理
可对各组件服务进行统一的管理，包括start、stop、status、restart