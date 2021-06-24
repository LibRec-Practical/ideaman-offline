package Recall;

import Util.HbaseUtil.HbaseThrift;
import Util.MySqlUtil.mySqlJDBC;
import org.apache.parquet.Strings;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TTransportException;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Map;

/**
 * @ClassName: HotRecall
 * @Description: 热门召回, 获得近七天的热门召回结果,数量为2000
 * @author：贾敬哲
 * @date： 2020年12月15日15:48:38
 */
public class HotRecall implements Recall {

    @Override
    public void train() {

    }

    @Override
    public Map<String, Double> predict(String paper_id) {
        return null;
    }

    /**
     * @Name: run
     * @Author: jingzhe jia
     * @Description: 热门召回, 获得近七天的热门召回结果,数量为2000,从Mysql读取数据，并将其写入到Hbase
     * @Date: 2020/12/15 15:58
     **/

    @Override
    public void run() {
        try {
            ArrayList<String> user_ids = mySqlJDBC.getInstance().getUserIds();
            ResultSet res = mySqlJDBC.getInstance().read(
                    "SELECT item_id,COUNT(u_id) as \"click_num\" FROM `click_log`\n" +
                            "WHERE event_type=1 AND add_time >= DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 99 DAY),'%Y-%m-%d') \n" +
                            "GROUP BY item_id\n" +
                            "ORDER BY click_num DESC\n" +
                            "LIMIT 2000"
            );
            ArrayList<String> item_ids_list = new ArrayList<>();
            while (true) {
                if (!res.next()) {
                    break;
                }
                item_ids_list.add(res.getString("item_id"));
                // 从res中获取item_id
            }
            String item_ids = Strings.join(item_ids_list, ",");
            for (String uid : user_ids
            ) {
                String sql = String.format("UPDATE user_rec SET hot_recall = \"%s\" WHERE user_id = %s;\n", item_ids, uid);
                mySqlJDBC.getInstance().write(sql);
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }

    }

    public static void main(String[] args) {
        HotRecall hotRecall = new HotRecall();
        hotRecall.run();
    }
}
