package Recall;

import net.librec.common.LibrecException;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.ml.evaluation.RegressionEvaluator;
import org.apache.spark.ml.recommendation.ALS;
import org.apache.spark.ml.recommendation.ALSModel;
import org.apache.spark.sql.*;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;
import java.util.Map;
import java.util.Properties;

class Rating implements Serializable {
    private int userId;
    private int paperId;
    private float rating;
    private long timestamp;

    public Rating(int userId, int paperId, float rating, long timestamp) {
        this.userId = userId;
        this.paperId = paperId;
        this.rating = rating;
        this.timestamp = timestamp;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public int getPaperId() {
        return paperId;
    }

    public void setPaperId(int paperId) {
        this.paperId = paperId;
    }

    public float getRating() {
        return rating;
    }

    public void setRating(float rating) {
        this.rating = rating;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }


    public static Rating parseRating(String str) {
        String[] fields = str.split("::");
        if (fields.length != 4) {
            throw new IllegalArgumentException("Each line must contain 4 fields");
        }
        int userId = Integer.parseInt(fields[0]);
        int paperId = Integer.parseInt(fields[1]);
        float rating = Float.parseFloat(fields[2]);
        long timestamp = Long.parseLong(fields[3]);
        return new Rating(userId, paperId, rating, timestamp);
    }
}

public class ALSRecall implements Recall {


    @Override
    public void train() {

    }

    @Override
    public Map<String, Double> predict(String paper_id) {
        return null;
    }

    @Override
    public void run() throws LibrecException, IOException {

    }

    public static void main(String[] args) throws IOException {
        InputStream inputStream = new FileInputStream("src/main/resources/config.properties");
        Properties properties = new Properties();
        properties.load(inputStream);
        String URL = properties.getProperty("jdbc.url");
        String DRIVER = properties.getProperty("jdbc.driver");
        String USER = properties.getProperty("jdbc.username");
        String PASSWORD = properties.getProperty("jdbc.password");


        //创建SparkConf用于读取系统信息并设置运用程序的名称
        SparkConf conf = new SparkConf().setAppName("SparkSQLJDBCToMySQL").setMaster("local");
        //创建JavaSparkContext对象实例作为整个Driver的核心基石
        JavaSparkContext sc = new JavaSparkContext(conf);
        //设置输出log的等级,可以设置INFO,WARN,ERROR
        sc.setLogLevel("ERROR");
        //创建SQLContext上下文对象，用于SqL的分析
        SQLContext sqlContext = new SQLContext(sc);
        /**
         * 1.通过format("jdbc")的方式来说明SparkSQL操作的数据来源是JDBC，
         *  JDBC后端一般都是数据库，例如去操作MYSQL.Oracle数据库
         * 2.通过DataframeReader的option方法把要访问的数据库信息传递进去，
         * url：代表数据库的jdbc链接的地址和具体要连接的数据库
         * datable：具体要连接使用的数据库
         * 3.Driver部分是SparkSQL访问数据库的具体驱动的完整包名和类名
         * 4.关于JDBC的驱动jar可以使用在Spark的lib目录中，也可以在使用
         * spark-submit提交的时候引入，编码和打包的时候不需要这个JDBC的jar
         */

        DataFrameReader reader = sqlContext.read().format("jdbc");//指定数据来源
        reader.option("url", URL);//指定连接的数据库
        reader.option("dbtable", "click_log");//操作的表
        reader.option("driver", "com.mysql.jdbc.Driver");//JDBC的驱动
        reader.option("user", USER); //用户名
        reader.option("password", PASSWORD); //用户密码
        Dataset userinforDataSourceDS = reader.load();//基于userinfor表创建Dataframe
//        Dataset<Row> ratings = spark.createDataFrame(ratingsRDD, Rating.class);
//        ALS als = new ALS()
//                .setMaxIter(5)
//                .setRegParam(0.01)
//                .setUserCol("userId")
//                .setItemCol("paperId")
//                .setRatingCol("rating");
//        ALSModel model = als.fit(ratings);

    }
}
