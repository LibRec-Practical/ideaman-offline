package Recall

import java.lang.Thread.sleep

import org.apache.spark._
import org.apache.spark._
import org.apache.spark.sql.SparkSession
import Util.HbaseUtil._
import org.apache.spark.ml.recommendation.ALS
import org.apache.spark.sql.functions.explode

import scala.math.random

object SparkALSRecall {
    def main(args: Array[String]): Unit = {
        // 创建Spark Session
        val ss: SparkSession = SparkSession.builder()
          .master("local")
          .appName("ALSRecall")
          .config("spark.port.maxRetries", "100")
          .getOrCreate()
        val sqlContext = ss.sqlContext
        import ss.implicits._

        // 链接Mysql,生成DataFrame
        val map = Map[String, String](
            "url" -> "jdbc:mysql://127.0.0.1/ideaman",
            "driver" -> "com.mysql.jdbc.Driver",
            "user" -> "root",
            "password" -> ",/Qa+sk.mGB48",
            "dbtable" -> "click_log"
        )
        val df = ss.read.format("jdbc").load()

        // 统计用户的听歌总数
        val user_item_total = df.select($"user_id", $"item_id")
          .groupBy($"user_id").count
          .withColumnRenamed("count", "total")
        // 点击数*10 再取对数,再用点击过的论文做占比,占比使用上面的总数左连接相除求出
        val item_ratings = df.groupBy($"user_id", $"item_id").count // groupBy统计用户对每首歌的点击
          .join(user_item_total, Seq("user_id"), "left") // 统计频数，左连接总数
          .withColumn("event_type", ($"count" + 1) * $"count" / $"total") // 计算得分
          .drop("count", "total") // 丢弃中间变量
        val Array(train, test) = item_ratings.randomSplit(Array(0.8, 0.2))

        val item_als = new ALS().setMaxIter(5).setRegParam(0.01).setColdStartStrategy("drop")
          .setUserCol("user_id").setItemCol("item_id").setRatingCol("event_type")
        val model = item_als.fit(train)
        val res = model.recommendForAllUsers(5).select($"user_id", explode($"recommendations.item_id").as("item_id"))

        


    }
}



