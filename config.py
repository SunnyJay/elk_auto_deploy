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
	'filebeat':
	["10.1.5.75"，"10.1.5.76",
	 "10.1.5.77"，"10.1.5.78",
	 "10.1.5.65"，"10.1.5.66",
	 "10.1.5.91",
	 "10.1.5.86",
	 "10.1.5.89"，"10.1.5.90",
	 "10.1.5.69"，"10.1.5.70",
	 "10.1.5.84"，"10.1.5.85",
	 "10.1.5.63"，"10.1.5.64",
	 "10.1.5.67"，"10.1.5.68",
	 "10.1.5.79"，"10.1.5.80",
	],
}

###############################
# filebeat log path name config
###############################
filebeat_roles=[
"as", "as",
"fs", "fs",
"gs", "gs",
"mbkq", 
"mbks", 
"mbks-mysql", "mbks-mysql", 
"mes", "mes",
"mysql", "mysql",
"pcs", "pcs",
"security", "security",
"ums", "ums"
]


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