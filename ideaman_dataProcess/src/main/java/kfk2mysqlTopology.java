import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.kafka.KafkaSpout;
import org.apache.storm.kafka.SpoutConfig;
import org.apache.storm.kafka.StringScheme;
import org.apache.storm.kafka.ZkHosts;
import org.apache.storm.spout.SchemeAsMultiScheme;
import org.apache.storm.topology.TopologyBuilder;

public class kfk2mysqlTopology {

    public kfk2mysqlTopology() {
    }

    public static void main(String[] args) {

        ZkHosts zkHosts = new ZkHosts("192.168.27.136:2181");
        TopologyBuilder builder = new TopologyBuilder();
        SpoutConfig spoutConfig = new SpoutConfig(zkHosts, "ideaman2", "", "librec");
        spoutConfig.scheme = new SchemeAsMultiScheme(new StringScheme());
        builder.setSpout("flume_kakfa_mysql", new KafkaSpout(spoutConfig), 1);
        builder.setBolt("mysqlBolt", new mysqlBolt(), 1).globalGrouping("flume_kakfa_mysql");
        LocalCluster cluster = new LocalCluster();
        Config conf = new Config();
        cluster.submitTopology("kfk2mysqlTopology", conf, builder.createTopology());

        try {
            System.out.println("Waiting to consume from kafka");
            Thread.sleep(30000000L);
        } catch (Exception var7) {
            System.out.println("Thread interrupted exception : " + var7);
        }

        cluster.killTopology("kfk2mysqlTopology");
        cluster.shutdown();
    }
}
