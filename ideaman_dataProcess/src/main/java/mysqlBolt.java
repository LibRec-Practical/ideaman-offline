//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

import com.alibaba.fastjson.JSON;
import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonParser;
import java.util.Map;
import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.topology.base.BaseRichBolt;
import org.apache.storm.tuple.Tuple;

public class mysqlBolt extends BaseRichBolt {
    private static final long serialVersionUID = 9063211371729556973L;

    public mysqlBolt() {
    }

    public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
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

    public void execute(Tuple input) {
        String input_str = input.getString(0);
        if (input_str.indexOf(123) < 0) {
            System.out.println("Not Json");
        } else {
            input_str = input_str.substring(input_str.indexOf(123));
            System.out.println("JSON:" + input_str);
            new Gson();
            Map maps = (Map)JSON.parse(input_str);
            ideamanLog ideamanlogger = new ideamanLog();
            if (maps.containsKey("headers")) {
                ideamanlogger.headers = String.valueOf(maps.get("headers"));
            } else {
                ideamanlogger.headers = "";
            }

            String data_str = String.valueOf(maps.get("data"));
            Map map = (Map)JSON.parse(data_str);
            System.out.println("MAP:" + map.keySet());
            if (map.containsKey("distinct_id")) {
                ideamanlogger.distinct_id = String.valueOf(map.get("distinct_id"));
            } else {
                ideamanlogger.distinct_id = "";
            }

            if (map.containsKey("timestamp")) {
                ideamanlogger.timeStamp = String.valueOf(map.get("timestamp"));
            } else {
                ideamanlogger.timeStamp = "";
            }

            if (map.containsKey("event_type")) {
                ideamanlogger.event_type = String.valueOf(map.get("event_type"));
            } else {
                ideamanlogger.event_type = "";
            }

            if (map.containsKey("event")) {
                ideamanlogger.event = String.valueOf(map.get("event"));
            } else {
                ideamanlogger.event = "";
            }

            if (map.containsKey("project")) {
                ideamanlogger.project = String.valueOf(map.get("project"));
            } else {
                ideamanlogger.project = "";
            }

            if (map.containsKey("properties")) {
                ideamanlogger.properties = String.valueOf(map.get("properties"));
            } else {
                ideamanlogger.properties = "";
            }

            if (map.containsKey("system")) {
                ideamanlogger.system = String.valueOf(map.get("system"));
            } else {
                ideamanlogger.system = "";
            }

            if (map.containsKey("extra_para")) {
                ideamanlogger.extra_para = String.valueOf(map.get("extra_para"));
            } else {
                ideamanlogger.extra_para = "";
            }

            if (map.containsKey("recommend_scene_id")) {
                ideamanlogger.recommend_scene_id = String.valueOf(map.get("recommend_scene_id"));
            } else {
                ideamanlogger.recommend_scene_id = "";
            }

            if (map.containsKey("buket_id")) {
                ideamanlogger.buket_id = String.valueOf(map.get("buket_id"));
            } else {
                ideamanlogger.buket_id = "";
            }

            if (map.containsKey("strategy_id")) {
                ideamanlogger.strategy_id = String.valueOf(map.get("strategy_id"));
            } else {
                ideamanlogger.strategy_id = "";
            }

            if (map.containsKey("p_datetime")) {
                ideamanlogger.p_datetime = String.valueOf(map.get("p_datetime"));
            } else {
                ideamanlogger.p_datetime = "";
            }

            if (map.containsKey("is_del")) {
                ideamanlogger.is_del = String.valueOf(map.get("is_del"));
            } else {
                ideamanlogger.is_del = "";
            }

            System.out.println(ideamanlogger.toMysql());
            mysqlUtil.getInstance().write(ideamanlogger.toMysql());
            Map map_cf = (Map)JSON.parse(ideamanlogger.properties);
            System.out.println("MAP:" + map_cf.keySet());
            String sql = "INSERT INTO click_log (u_id,item_id,event_type) VALUES ('" + map_cf.get("userId") + "','" + map_cf.get("paperId") + "','" + map_cf.get("event") + "')";
            System.out.println(sql);
            mysqlUtil.getInstance().write(sql);
            System.out.println("写入完成");
        }
    }

    public void declareOutputFields(OutputFieldsDeclarer declarer) {
    }
}
