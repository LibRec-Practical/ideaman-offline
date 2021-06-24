import com.alibaba.fastjson.JSON;
import com.google.gson.Gson;

import java.util.Map;

public class ideamanLog {
    public String distinct_id;
    public String user_id;
    public String timeStamp;
    public String event_type;
    public String event;
    public String project;
    public String properties;
    public String system;
    public String extra_para;
    public String recommend_scene_id;
    public String buket_id;
    public String strategy_id;
    public String p_datetime;
    public String is_del = "0";
    public String headers;

    public String toMysql() {
        return String.format("INSERT INTO `ideaman`.`ideaman_log`(`distinct_id`, `user_id`, `timeStamp`, `event_type`, `event`, `project`, `properties`, `system`, `extra_para`, `recommend_scene_id`, `buket_id`, `strategy_id`, `p_datetime`, `is_del`,`headers`) VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')", this.distinct_id, this.user_id, this.timeStamp, this.event_type, this.event, this.project, this.properties, this.system, this.extra_para, this.recommend_scene_id, this.buket_id, this.strategy_id, this.p_datetime, this.is_del, this.headers);

    }

    public static void main(String[] args) {
        String input_str = "[2021-05-29T15:32:25.149] [INFO] file - {\"headers\":{\"host\":\"42.193.18.137:7000\",\"connection\":\"keep-alive\",\"content-length\":\"256\",\"accept\":\"application/json, text/plain, */*\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36\",\"content-type\":\"application/json;charset=UTF-8\",\"origin\":\"http://localhost:3000\",\"referer\":\"http://localhost:3000/\",\"accept-encoding\":\"gzip, deflate\",\"accept-language\":\"zh-CN,zh;q=0.9\"},\"data\":{\"timestamp\":1622273544861,\"app_id\":8104,\"app_name\":\"LibRec Paper\",\"headers\":{\"x_dust_log_id\":\"123456\"},\"event\":\"click\",\"params\":{\"app_id\":8104,\"fe_flag\":\"React\",\"userId\":35001,\"username\":\"lisikuanreno@163.com\",\"paper_id\":1741,\"page\":\"home\",\"from\":\"home\"}}}";

        if (input_str.indexOf(123) < 0) {
            System.out.println("Not Json");
        } else {
            input_str = input_str.substring(input_str.indexOf(123));
            new Gson();
            Map input_maps = (Map) JSON.parse(input_str);

            String data_str = String.valueOf(input_maps.get("data"));
            Map data_map = (Map) JSON.parse(data_str);

            String event = String.valueOf(data_map.get("event"));
            if (event.equals("click")){
                String params_str = String.valueOf(data_map.get("params"));
                Map params_map = (Map) JSON.parse(params_str);


            }
        }
    }


}
