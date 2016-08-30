#elk_auto_deploy
版本:v1.1

这是一个用于自动部署 ELK 日志分析平台的 python fabric 项目。

---

###elk_auto_deploy 实现功能
- 一键上传ELK各组件安装包和配置文件

- 一键安装和调优ELK服务

- 一键部署ELK服务（即统一了上述两个功能）

- 一键卸载和清理ELK服务

- 一键管理（启动、停止、重启、查看状态）ELK服务

###ELK 日志分析平台架构如下

filebeat ===> logstash ====> elasticsearch =======> kibana    

各组件部署:
- filebeat部署多个，分别部署于各个需要被监控日志的服务器上。
- logstash部署多个，各自部署于独立的服务器上。
- elasticsearch部署多个，各自部署于独立的服务器上，构成集群。
- kibana部署一个，部署于独立的服务器上。




###本工具目录构成如下：

    elk_tools_temp/
    fabfile.py
    config.py
    -elasticsearch/
        elasticsearch.rpm
        elasticsearch.yml
        elasticsearch-kopf-master.zip
        elasticsearch-head-master.zip
    logstash/
        logstash.rpm
        logstash.yml
    filebeat/
        filebeat.rpm
        filebeat.yml
    kibana/
        kibana.rpm
        kibana.yml
        sense-2.0.0-beta5.tar.gz

- fabfile.py是Fabric所必须的管理文件，其使用默认名称fabfile，这样使用fab命令无需使用 -f 指定管理文件。
- config.py是工具的配置文件，用于配置ssh账户信息、各组件地址信息、各组件调优信息等。
- 其他各目录分别包含了各组件的rpm安装包和主配置文件。其中，配置文件中包含了主要的基本配置。

###使用方法

注意，正确安装了Fabric后才能进行工具的各项操作。 

####初次一键部署
本功能适用于在全新的环境中一键自动部署日志平台，包括上传、安装、配置、清理等。
步骤如下：
1. 上传elk_tools_rpm至目录~（home）下
2. 根据需求修改后config.py配置文件，包括：
   - linux账号和密码
   - 主机角色：即各个组件对应的主机地址，格式依照默认配置文件
   - filebeat角色：对应主机角色中的filebeat地址
   - 组件调优：各组件对应的系统调优设置
3. 运行 fab deploy执行一键自动部署。其中，deploy执行了以下任务:
   - 在各服务器上创建临时目录 ~/elk_tools_temp，用来存储安装文件与配置文件
   - 上传相应的安装文件和配置文件至各个服务器
   - 安装各组件
   - 配置各组件
   - 设置filebeat配置文件
   - 删除临时目录

####一键创建临时目录
除了在一键部署中创建临时目录，也可以针对特定组件和角色单独执行该功能，如：
- 如果需要创建所有组件的临时目录，执行:
  `fab create_temp_folders_all`
- 如果只需要创建elasticsearch的临时目录，执行:
   `fab create_temp_folders:elasticsearch`
- 如果只需要在特定主机上创建elasticsearch的临时目录，执行:
   `fab create_temp_folders:elasticsearch, hosts =“host1;host2”`
  其中，host1或host2位目标主机IP地址。

####一键上传安装与配置文件
注意，执行该功能之前务必确保相关组件临时目录已创建。
除了在一键部署中进行组件的上传，也可以针对特定组件和角色单独执行该功能，如：
- 如果需要上传所有组件，执行：
  `fab upload_all`
- 如果只需要上传elasticsearch相关文件到所有elasticsearch主机，执行：
  `fab upload:elasticsearch`
- 如果只需要上传elasticsearch相关文件到特定elasticsearch主机，执行：
  `fab upload:elasticsearch, hosts =“host1;host2"`

####一键安装
注意，执行该功能之前务必确保相关组件安装文件已上传。
除了在一键部署中进行组件的安装，也可以针对特定组件和角色单独执行该功能，如：
- 如果需要上传所有组件，执行：
  `fab install_all`
- 如果只需要安装所有主机上elasticsearch组件，执行：
  `fab install:elasticsearch`
- 如果只需要在特定主机上安装elasticsearch组件，执行：
  `fab install:elasticsearch, hosts =“host1;host2”`

####一键配置
注意，执行该功能之前务必确保相关组件已安装。
除了在一键部署中进行组件的安装，也可以针对特定组件和角色单独执行该功能，如：
- 如果需要配置所有组件，执行：
  `fab configure_all`
- 如果只需要配置所有主机上elasticsearch组件，执行：
  `fab configure:elasticsearch`
- 如果只需要配置特定主机上elasticsearch组件，执行：
  `fab configure:elasticsearch, hosts =“host1;host2”`

####一键安装插件
注意，执行该功能之前务必确保相关组件已安装。
除了在一键部署中进行组件相关插件的安装，也可以针对特定组件和角色单独执行该功能，如：
- 如果需要安装所有插件，执行：
  `fab install_plugins`
- 如果只需要安装特定插件，执行：
  `fab install_plugin_pluginname_exec`
  其中，pluginname为插件名称，如kopf、head、sense等。

####一键卸载
注意，执行该功能之前务必确保相关组件已安装。
可以针对特定组件和角色单独执行该功能，如：
- 如果需要卸载所有组件，执行：
  `fab uninstall_all`
- 如果只需要卸载所有主机上elasticsearch组件，执行：
  `fab uninstall:elasticsearch`
- 如果只需要卸载特定主机上elasticsearch组件，执行：
  `fab uninstall:elasticsearch, hosts =“host1;host2”`

####一键管理
注意，执行该功能之前务必确保相关组件已安装并配置完毕。start、stop、restart、status类似。
- 如果需要启动所有elasticsearch组件，执行：
  `fab start:elasticsearch`
- 如果只需要启动特定主机上elasticsearch组件，执行：
  `fab start:elasticsearch, hosts =“host1;host2”`