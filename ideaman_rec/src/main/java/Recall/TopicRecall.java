package Recall;

import Util.MySqlUtil.mySqlJDBC;
import org.apache.parquet.Strings;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * @ClassName: InterestTagRecall
 * @Description: 根据用户选择的兴趣Tag，从每个Tag里面选取最近的1000个作为召回结果。
 * @author：贾敬哲
 * @date： 2020年12月15日15:48:38
 */
public class TopicRecall implements Recall {
    @Override
    public void train() {

    }

    @Override
    public Map<String, Double> predict(String paper_id) {
        return null;
    }

    @Override
    public void run() {
        try {
            ResultSet user_interestTag = mySqlJDBC.getInstance().read(
                    "SELECT id,interest_tags FROM `user` WHERE username NOT LIKE '%tmp%'"
            );
            Map<String, String> id2tags = new HashMap<>();
            while (true) {
                if (!user_interestTag.next()) {
                    break;
                }
                id2tags.put(user_interestTag.getString("id"), user_interestTag.getString("interest_tags"));
            }
            for (String u_id : id2tags.keySet()
            ) {
                String[] tags = id2tags.get(u_id).split(",");
                ArrayList<String> paper_ids = new ArrayList<>();
                for (String tag : tags
                ) {
                    ResultSet papers4tags = mySqlJDBC.getInstance().read(
                            "SELECT id FROM `paper`\n" +
                                    "WHERE FIND_IN_SET(\"" + tag + "\",tags)\n" +
                                    "ORDER BY published DESC\n" +
                                    "LIMIT 100"
                    );
                    while (true) {
                        if (!papers4tags.next()) {
                            break;
                        }
                        paper_ids.add(papers4tags.getString("id"));
                    }
                }
                String item_ids = Strings.join(paper_ids, ",");
                String sql = String.format("UPDATE user_rec SET total_sort = \"%s\" WHERE user_id = %s;\n",  item_ids , u_id);
                mySqlJDBC.getInstance().write(sql);
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
    }

    public static void main(String[] args) {
        TopicRecall in = new TopicRecall();
        in.run();
    }
}
