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
    public String headers ;

    public String toMysql() {
        return String.format("INSERT INTO `ideaman`.`ideaman_log`(`distinct_id`, `user_id`, `timeStamp`, `event_type`, `event`, `project`, `properties`, `system`, `extra_para`, `recommend_scene_id`, `buket_id`, `strategy_id`, `p_datetime`, `is_del`,`headers`) VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')", this.distinct_id, this.user_id, this.timeStamp, this.event_type, this.event, this.project, this.properties, this.system, this.extra_para, this.recommend_scene_id, this.buket_id, this.strategy_id, this.p_datetime, this.is_del,this.headers);

    }

    public static void main(String[] args) {
        ideamanLog a = new ideamanLog();
        a.distinct_id = "asiodjaiodj31231231";
        a.user_id = "asiodjaiodj31231231";
        a.timeStamp = "2342342342342";
        a.event_type = "asiodjaiodj31231231";
        a.event = "asiodjaiodj31231231";
        a.project = "asiodjaiodj31231231";
        a.properties = "asiodjaiodj31231231";
        a.system = "asiodjaiodj31231231";
        a.extra_para = "asiodjaiodj31231231";
        a.recommend_scene_id = "asiodjaiodj31231231";
        a.buket_id = "asiodjaiodj31231231";
        a.strategy_id = "asiodjaiodj31231231";
        a.p_datetime = "asiodjaiodj31231231";
        a.is_del = "asiodjaiodj31231231";


        System.out.println(a.toMysql());
    }
}
