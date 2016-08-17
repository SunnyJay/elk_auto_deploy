######################
# account config
######################
user = "root"
passowrd = "sinosun"

######################
# hosts config
######################
roledefs = {
	'logstash':["10.1.5.54"],
	'elasticsearch':["10.1.5.192", "10.1.5.193"],
	'kibana':["10.1.5.55"],
	'redis':["10.1.5.194"],
	'filebeat':["10.1.5.55"],
}

######################
# tools optimize
######################
#elasticsearh
ela_optimize = [
"sed -i 's/#ES_HEAP_SIZE=2g/ES_HEAP_SIZE=4g/g' /etc/sysconfig/elasticsearch",
"sed -i 's/#MAX_OPEN_FILES=65535/MAX_OPEN_FILES=65536/g' /etc/sysconfig/elasticsearch",
"sed -i 's/#MAX_LOCKED_MEMORY=unlimited/MAX_LOCKED_MEMORY=unlimited/g' /etc/sysconfig/elasticsearch",
"swapoff -a",
"sed -i '/swap/s/^/#/' /etc/fstab",
"sed -i '$a vm.swapiness=1' /etc/sysctl.conf",
"/sbin/sysctl -p",
"ulimit -l unlimited"
]

#logstash
logstash_optimize = [

]

#kibana
kibana_optimize = [

]

#filebeat
filebeat_optimize = [

]

#redis
redis_optimize = [

]