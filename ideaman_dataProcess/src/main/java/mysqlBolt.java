//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

import com.alibaba.fastjson.JSON;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

public class mysqlBolt extends BaseRichBolt {
    private static final long serialVersionUID = 9063211371729556973L;
    private OutputCollector collector;

    public mysqlBolt() {
    }

    @Override
    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
        this.collector = collector;

    }

    public static boolean validate(String jsonStr) {
        JsonElement jsonElement;
        try {
            jsonElement = (new JsonParser()).parse(jsonStr);
        } catch (Exception var3) {
            return false;
        }

        if (jsonElement == null) {
            return false;
        } else {
            return jsonElement.isJsonObject();
        }
    }

    @Override
    public void execute(Tuple input) {

        String input_str = input.getString(0);

        if (input_str.indexOf(123) < 0) {
        } else {
            input_str = input_str.substring(input_str.indexOf(123));
//            System.out.println("JSON:" + input_str);
            new Gson();
            Map maps = (Map) JSON.parse(input_str);
            ideamanLog ideamanlogger = new ideamanLog();
            if (maps.containsKey("headers")) {
                ideamanlogger.headers = String.valueOf(maps.get("headers"));
            } else {
                ideamanlogger.headers = "";
            }
            if (input_str.indexOf(123) < 0) {
            } else {
                input_str = input_str.substring(input_str.indexOf(123));
                new Gson();
                Map input_maps = (Map) JSON.parse(input_str);

                String data_str = String.valueOf(input_maps.get("data"));
                Map data_map = (Map) JSON.parse(data_str);

                String event = String.valueOf(data_map.get("event"));
                if (event.equals("click")) {
                    String params_str = String.valueOf(data_map.get("params"));
                    Map params_map = (Map) JSON.parse(params_str);

                    if (String.valueOf(params_map.get("paper_id")).length() < 1|| params_map.get("paper_id") == null) {
                        collector.ack(input);
                        return;
                    }
                    if (String.valueOf(params_map.get("userId")).length() <1 || params_map.get("userId") == null) {
                        collector.ack(input);
                        return;
                    }
                    String sql = "INSERT INTO click_log (u_id,item_id,event_type) VALUES ('" + params_map.get("userId") + "','" + params_map.get("paper_id") + "','1')";
                    mysqlUtil.getInstance().write(sql);
                    ResultSet rs = null;
                    System.out.println("@@@@@@@"+params_map.get("userId"));
                    sql = "SELECT item_ids from seq_log where user_id = " + params_map.get("userId");
                    System.out.println("###########"+sql);
                    rs = mysqlUtil.getInstance().read(sql);
                    String item_ids = "";

                    try {
                        while (true) {
                            if (rs == null || !rs.next()) {
                                break;
                            }
                            item_ids = rs.getString("item_ids");
                        }
                    } catch (SQLException throwables) {
                        collector.ack(input);
                        return;
                    }

                    if (item_ids.length() == 0) {
                        item_ids = String.valueOf(params_map.get("paper_id"));
                        mysqlUtil.getInstance().write("INSERT INTO seq_log VALUES(" + params_map.get("userId") + ",\"" + item_ids + "\");");
                    } else {
                        item_ids = item_ids + "," + params_map.get("paper_id");
                        mysqlUtil.getInstance().write("UPDATE seq_log set item_ids = \"" + item_ids + "\" WHERE user_id = " + params_map.get("userId"));
                    }
                }
            }
        }

        collector.ack(input);


    }


    @Override
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
    }
}
