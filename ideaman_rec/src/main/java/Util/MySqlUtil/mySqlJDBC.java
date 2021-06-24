package Util.MySqlUtil;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.*;
import java.util.ArrayList;
import java.util.Properties;

/**
 * @author pytho
 * @program: Storm2hive
 * @description: hive处理工具类
 * @create: 2020-05-06 11:59
 **/
public class mySqlJDBC {
    public static String URL = "";
    private static String DRIVER = "";
    private static String PASSWORD = "";
    private static String USER = "";

    public static mySqlJDBC instance;

    private mySqlJDBC() throws IOException {
        InputStream inputStream = new FileInputStream("src/main/resources/config.properties");
        Properties properties = new Properties();
        properties.load(inputStream);
        URL = properties.getProperty("jdbc.url");
        DRIVER = properties.getProperty("jdbc.driver");
        USER = properties.getProperty("jdbc.username");
        PASSWORD = properties.getProperty("jdbc.password");
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

    public ArrayList<String> getUserIds() throws SQLException {
        ResultSet res = read("SELECT id FROM user WHERE username NOT LIKE '%tmp%'");
        ArrayList<String> user_ids = new ArrayList<>();
        while (res.next()) {
            user_ids.add(res.getString(1));
        }
        return user_ids;
    }

    public void initUser_rec() throws SQLException {
        ArrayList<String> user_ids = this.getUserIds();
        for (String s : user_ids
        ) {
            String sql = String.format("INSERT INTO user_rec (user_id ) VALUES( %s )",s);
            try{
                this.write(sql);
            }
            catch (Exception e){
                if (e instanceof SQLIntegrityConstraintViolationException){
                    break;
                }
            }
        }
    }

    public static synchronized mySqlJDBC getInstance() {
        if (instance == null) {
            try {
                instance = new mySqlJDBC();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return instance;
    }

    public static void main(String[] args) throws SQLException, ClassNotFoundException, IOException {

    }

}