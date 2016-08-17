"""
    fabfile
    -------
    A fabfile which can deploy elk automatically.
    Author: Sun Nanjun<sun_coke007@163.com>
    Created on 2016-08-15
"""
from fabric.api import *
import config

env.user = config.user
env.roledefs = config.roledefs
env.password = config.password

#########################
# create_folders
#########################
@task
def create_temp_folders_all():
	create_temp_folders("elasticsearch")
	create_temp_folders("logstash")
	create_temp_folders("kibana")
	create_temp_folders("redis")
	create_temp_folders("filebeat")

@task
def create_temp_folders(tool_name):
	execute(create_temp_folders_exec, tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def create_temp_folders_exec(tool_name):
	with settings(warn_only = True):
		run("mkdir -p ~/elk_tools_temp/%s" % tool_name)

#########################
# upload
#########################
@task
def upload_all():
	upload("elasticsearch")
	upload("logstash")
	upload("kibana")
	upload("redis")
	upload("filebeat")

@task
def upload(tool_name):
	execute(upload_exec, tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def upload_exec(tool_name):
	with settings(warn_only = True):
		put("~/elk_tools_temp/%s/" % tool_name, "~/elk_tools_temp/")

#########################
# install
#########################
@task
def install_all():
	install("elasticsearch")
	install("logstash")
	install("kibana")
	install("redis")
	install("filebeat")

@task
def install(tool_name):
	if tool_name == "redis":
		execute(install_redis, hosts = env.roledefs[tool_name])
	else:
		execute(install_exec, tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def install_exec(tool_name):
	with cd("~/elk_tools_temp/%s" % tool_name):
		with settings(warn_only = True):
			run("rpm -ivh %s.rpm" % tool_name)
			run("/sbin/chkconfig --add %s" % tool_name)

@task
def install_redis():
	with cd("~/elk_tools_temp/%s" % "redis"):
		with settings(warn_only = True):
			run("mkdir -p /usr/local/bin/redis")
			run("mkdir -p /usr/local/etc/redis")
			run("mkdir -p /var/log/redis")
			run("mkdir -p /var/lib/redis")
			run("cp -f bin/* /usr/local/bin/redis/")
			run("cp -f config/redis.conf /usr/local/etc/redis/")
			run("chmod +x /usr/local/bin/redis/*")
			run("sed -i '$a \/usr\/local\/bin\/redis\/redis-server \/usr\/local\/etc\/redis\/redis.conf' /etc/rc.local")

############################
# start\stop\status\restart
############################
@task
def start(tool_name):
	if tool_name == "redis":
		execute(start_redis, hosts = env.roledefs[tool_name])
	else:
		execute(executor, command_name = "start", tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def stop(tool_name):
	if tool_name == "redis":
		execute(stop_redis, hosts = env.roledefs[tool_name])
	else:
		execute(executor, command_name = "stop", tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def status(tool_name):
	if tool_name == "redis":
		execute(status_redis, hosts = env.roledefs[tool_name])
	else:
		execute(executor, command_name = "status", tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def restart(tool_name):
	if tool_name == "redis":
		execute(restart_redis, hosts = env.roledefs[tool_name])
	else:
		execute(executor, command_name = "restart", tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def executor(command_name, tool_name):
	with settings(warn_only = True):
		run("service %s %s" % (tool_name, command_name), pty = False)

@task
def start_redis():
	with settings(warn_only = True):
		run("/usr/local/bin/redis/redis-server /usr/local/etc/redis/redis.conf", pty = False)

@task
def stop_redis():
	with settings(warn_only = True):
		run("/usr/local/bin/redis/redis-cli shutdown")

@task
def status_redis():
	with settings(warn_only = True):
		run("ps aux | grep redis-server | grep -v grep")

@task
def restart_redis():
	stop_redis()
	start_redis()

############################
# configure
############################
@task
def configure_all():
	execute(configure_elasticsearch,  hosts = env.roledefs["elasticsearch"])
	execute(configure_logstash,  hosts = env.roledefs["logstash"])
	execute(configure_kibana,  hosts = env.roledefs["kibana"])
	execute(configure_redis,  hosts = env.roledefs["redis"])
	execute(configure_filebeat,  hosts = env.roledefs["filebeat"])
	
@task
def configure_elasticsearch():
	with settings(warn_only = True):
		run("cp -f ~/elk_tools_temp/elasticsearch/elasticsearch.yml /etc/elasticsearch")
		run("sed -i 's/node.name: node-.*$/node.name: node-%s/g' /etc/elasticsearch/elasticsearch.yml" %
			str(env.roledefs["elasticsearch"].index(env.host_string)+1))
		run("sed -i 's/network.host:.*$/network.host:%s/g' /etc/elasticsearch/elasticsearch.yml" %
			env.host_string)

		for optimize in config.ela_optimize:
			run(optimize)
@task
def configure_logstash():
	with settings(warn_only = True):
		run("cp -f ~/elk_tools_temp/logstash/logstash.conf /etc/logstash/conf.d/")
		for optimize in config.logstash_optimize:
			run(optimize)
@task
def configure_kibana():
	with settings(warn_only = True):
		run("cp -f ~/elk_tools_temp/kibana/kibana.yml /opt/kibana/config/")
		for optimize in config.kibana_optimize:
			run(optimize)
@task
def configure_filebeat():
	with settings(warn_only = True):
		run("cp -f ~/elk_tools_temp/filebeat/filebeat.yml /etc/filebeat/")
		for optimize in config.filebeat_optimize:
			run(optimize)
@task
def configure_redis():
	with settings(warn_only = True):
		run("cp -f ~/elk_tools_temp/redis/config/redis.config /usr/local/etc/redis/")
		for optimize in config.redis_optimize:
			run(optimize)

############################
# uninstall
############################
@task
def uninstall_all():
	uninstall("elasticsearch")
	uninstall("logstash")
	uninstall("kibana")
	uninstall("redis")
	uninstall("filebeat")

@task
def uninstall(tool_name):
	if tool_name == "redis":
		execute(uninstall_redis, hosts = env.roledefs[tool_name])
	else:
		execute(uninstall_exec, tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def uninstall_exec(tool_name):
	with settings(warn_only = True):
		run("rpm -e %s" % tool_name)

@task
def uninstall_redis():
	stop_redis()
	with settings(warn_only = True):
		run("rm -rf /usr/local/bin/redis /usr/local/etc/redis/")
		run("sed -i 'redis-server'/d/' /etc/rc.local")

############################
# delete_temp
############################
@task
def delete_temp_all():
	delete_temp("elasticsearch")
	delete_temp("logstash")
	delete_temp("kibana")
	delete_temp("redis")
	delete_temp("filebeat")

@task
def delete_temp(tool_name):
	execute(delete_temp_exec, tool_name = tool_name, hosts = env.roledefs[tool_name])

@task
def delete_temp_exec(tool_name):
	with settings(warn_only = True):
		run("rm -rf ~/elk_tools_temp")

############################
# check_cluster
############################
@task
@roles("elasticsearch")
def check_cluster():
	run("curl %s:9200/_cluster/health" % env.host_string)


############################
# main depoly
############################
@task
@roles("elasticsearch")
@runs_once
def deploy():
	create_temp_folders_all()
	upload_all()
	install_all()
	configure_all()
	delete_temp_all()
