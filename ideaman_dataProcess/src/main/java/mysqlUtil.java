import java.sql.*;

/**
 * @program: Storm2hive
 * @description: hive处理工具类
 * @create: 2020-05-06 11:59
 **/
public class mysqlUtil {
    public static final String URL = "jdbc:mysql://192.168.27.136:3306/ideaman";
    private static final String DRIVER = "com.mysql.jdbc.Driver";
    private static final String USER = "root";
    private static final String PASSWORD = "Delete1350$&";

    public static mysqlUtil instance;

    private mysqlUtil() {

    }

    public void write(String sql) {
        /**
         * @description 将数据写入到hive中
         * @param
         * @param sql 执行sql语句
         * @return
         * @date 2020/5/11  by 贾敬哲
         */
        try {
            Class.forName(DRIVER);
            Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
            Statement st = conn.createStatement();

            // create table
            st.execute(sql);

        } catch (SQLException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    public ResultSet read(String sql) {
        try {
            Class.forName(DRIVER);
            Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
            Statement st = conn.createStatement();
            PreparedStatement prepareStatement = conn.prepareStatement(sql);
            ResultSet rs = prepareStatement.executeQuery();
            return rs;
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
        return null;
    }

    public static synchronized mysqlUtil getInstance() {
        if (instance == null) {
            instance = new mysqlUtil();
        }
        return instance;
    }


}