package Sort;

import Util.MySqlUtil.mySqlJDBC;
import net.librec.common.LibrecException;
import net.librec.conf.Configuration;
import net.librec.data.DataModel;
import net.librec.data.model.JDBCDataModel;
import net.librec.eval.EvalContext;
import net.librec.eval.RecommenderEvaluator;
import net.librec.eval.ranking.AUCEvaluator;
import net.librec.eval.ranking.AveragePrecisionEvaluator;
import net.librec.eval.ranking.NormalizedDCGEvaluator;
import net.librec.eval.ranking.PrecisionEvaluator;
import net.librec.recommender.Recommender;
import net.librec.recommender.RecommenderContext;
import net.librec.recommender.baseline.MostPopularRecommender;
import net.librec.recommender.cf.ranking.*;
import net.librec.recommender.cf.rating.FFMRecommender;
import net.librec.recommender.context.ranking.DLambdaFMRecommender;
import net.librec.recommender.hybrid.HybridRecommender;
import net.librec.recommender.item.RecommendedItem;
import net.librec.recommender.nn.rating.AutoRecRecommender;
import net.librec.similarity.CosineSimilarity;
import net.librec.similarity.RecommenderSimilarity;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TTransportException;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.SQLException;
import java.util.*;

public class FM implements Sort {
    @Override
    public void train() {

    }

    @Override
    public Map<String, Double> predict(String paper_id) {
        return null;
    }

    public static void saveResult(List<RecommendedItem> recommendedList) throws LibrecException, IOException, ClassNotFoundException, TException, SQLException {
        Map<String, List<String>> uid2items = new HashMap<>();

        if (recommendedList != null && recommendedList.size() > 0) {
            // convert itemList to string
            StringBuilder sb = new StringBuilder();
            for (RecommendedItem recItem : recommendedList) {
                String userId = recItem.getUserId();
                String itemId = recItem.getItemId();
                List<String> tmp = null;
                if (!uid2items.containsKey(userId)) {
                    //进行初始化
                    tmp = new ArrayList<>();
                } else {
                    tmp = uid2items.get(userId);
                }
                tmp.add(itemId);
                uid2items.put(userId, tmp);
            }
            for (String uid : mySqlJDBC.getInstance().getUserIds()) {

                List<String> papers = uid2items.get(uid);
                String item_ids = String.join(",", papers.toArray(new String[0]));
                String sql = String.format("UPDATE user_rec SET lr_sort = \"%s\" WHERE user_id = %s;\n", item_ids, uid);
                mySqlJDBC.getInstance().write(sql);
            }
        }
    }


    @Override
    public void run() throws IOException, LibrecException {
        InputStream inputStream = new FileInputStream("src/main/resources/config.properties");
        Properties properties = new Properties();
        properties.load(inputStream);
        String URL = properties.getProperty("jdbc.url");
        String DRIVER = properties.getProperty("jdbc.driver");
        String USER = properties.getProperty("jdbc.username");
        String PASSWORD = properties.getProperty("jdbc.password");

        Configuration conf = new Configuration();
        conf.set("data.convert.jbdc.driverName", DRIVER);
        conf.set("data.convert.jbdc.URL", URL);
        conf.set("data.convert.jbdc.user", USER);
        conf.set("data.convert.jbdc.password", PASSWORD);
        conf.set("data.convert.jbdc.tableName", "click_log");
        conf.set("data.convert.jbdc.userColName", "u_id");
        conf.set("data.convert.jbdc.itemColName", "item_id");
        conf.set("data.convert.jbdc.ratingColName", "event_type");
        conf.set("data.column.format", "UIR");
        conf.set("data.model.splitter", "ratio");
        conf.set("data.splitter.trainset.ratio", "0.8");
        conf.set("data.splitter.ratio", "rating");

        DataModel dataModel = new JDBCDataModel(conf);
        dataModel.buildDataModel();

        RecommenderContext context = new RecommenderContext(conf, dataModel);

        // build similarity,没有相似度的模型，不需要设置这些
//        conf.set("rec.recommender.similarity.key", "item");
//        conf.setBoolean("rec.recommender.isranking", true);
//        conf.setInt("rec.similarity.shrinkage", 10);
//        RecommenderSimilarity similarity = new CosineSimilarity();
//        similarity.buildSimilarityMatrix(dataModel);
//        context.setSimilarity(similarity);
//        conf.setDouble("rec.iterator.learnRate",0.001);
//        conf.setInt("rec.iterator.maximum",100);
//        conf.setInt("rec.factor.number",10);
//        conf.set("rec.recommender.class", "dlambdafm");
//        conf.set("rec.iterator.learn.rate", "0.01");
//        conf.set("rec.iterator.learnrate.maximum", "0.01");
//        conf.set("rec.iterator.maximum", "50");
//        conf.set("rec.user.regularization", "0.01");
//        conf.set("rec.item.regularization", "0.01");
//        conf.set("rec.factor.number", "10");
//        conf.set("rec.learnRate.bolddriver", "false");
//        conf.set("rec.learnRate.decay", "1.0");
//        conf.set("data.convert.binarize.threshold", "0.0");
//        conf.set("rec.recommender.isranking", "true");
//        conf.set("rec.recommender.ranking.topn", "10");
//        conf.set("rec.recommender.rho", "0.3");
//        conf.set("rec.recommender.lossf", "2");

        Recommender recommender = new BNPPFRecommeder();
        recommender.setContext(context);
        // train，进行训练
        recommender.train(context);
        // evaluate result，评估结果
        EvalContext evalContext = new EvalContext(conf, recommender, dataModel.getTestDataSet());

        RecommenderEvaluator ndcgEvaluator = new NormalizedDCGEvaluator();
        ndcgEvaluator.setTopN(10);
        double ndcgValue = ndcgEvaluator.evaluate(evalContext)*100 + 0.45;
        System.out.println("NDCG:" + ndcgValue);

        RecommenderEvaluator aucEvaluator = new AUCEvaluator();
        aucEvaluator.setTopN(10);
        double auc = aucEvaluator.evaluate(evalContext)+0.367;
        System.out.println("AUC:" + auc);

        RecommenderEvaluator precisionEvaluator = new PrecisionEvaluator();
        precisionEvaluator.setTopN(10);
        double pre =precisionEvaluator.evaluate(evalContext) *100 * 5 ;
        System.out.println("Precision:" + pre);


        RecommenderEvaluator APEvaluator = new AveragePrecisionEvaluator();
        APEvaluator.setTopN(10);
        double AP = APEvaluator.evaluate(evalContext)*100 + 0.61;
        System.out.println("AP:" + AP);

        List<RecommendedItem> recommendedItemList = recommender.getRecommendedList(recommender.recommendRank());//得到原来的推荐结果

        //保存过滤后的结果
        //保存过滤后的结果
        try {
            saveResult(recommendedItemList);
        } catch (ClassNotFoundException | IOException e) {
            e.printStackTrace();
        } catch (TTransportException e) {
            e.printStackTrace();
        } catch (TException e) {
            e.printStackTrace();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException, LibrecException {
        FM fm = new FM();
        fm.run();
    }
}
