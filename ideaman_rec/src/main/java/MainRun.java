import Recall.HotRecall;
import Recall.TopicRecall;
import Recall.UserKNNRecall;
import Util.MySqlUtil.mySqlJDBC;
import net.librec.common.LibrecException;

import java.io.IOException;
import java.sql.SQLException;

public class MainRun {

    public static void main(String[] args) {
        try {
            mySqlJDBC.getInstance().initUser_rec();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
        //运行热门召回
        HotRecall ht = new HotRecall();
        ht.run();

        //运行Topic招呼
        TopicRecall tr = new TopicRecall();
        tr.run();
        //运行userknn召回
        UserKNNRecall userKNNRecall = null;
        try {
            userKNNRecall = new UserKNNRecall();
            userKNNRecall.run();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (LibrecException e) {
            e.printStackTrace();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }


    }
}
