
# 开启hadoop
bash /opt/hadoop/hadoop-2.7.7/sbin/start-all.sh
# 开启ZK
/opt/zookeeper/apache-zookeeper-3.6.1-bin/bin/zkServer.sh start
# 开启Hbase
/opt/hbase/hbase-1.4.13/bin/start-hbase.sh
# 开启flume
cd /opt/flume/apache-flume-1.9.0-bin && bin/flume-ng agent --conf conf --conf-file job/ideaman_txtlog2kafka.conf --name a1 -Dflume.root.logger=INFO,console&
# 开启kakfa
cd /opt/kafka/kafka_2.13-2.6.0/ &&  bin/kafka-server-start.sh -daemon config/server.properties
# 开启Spark
bash /opt/spark/spark-2.4.7-bin-hadoop2.7/sbin/start-all.sh
# 开启Zeppelin
/opt/zeppelin/zeppelin-0.9.0-preview2-bin-all/bin/zeppelin-daemon.sh start
#开启 Milvus
sudo docker start milvus_cpu_0.11.0
# 开启es
su esuser && nohup /opt/es/elasticsearch-7.9.3/bin/elasticsearch  -d
