package Recall;


import Util.HbaseUtil.HbaseThrift;
import Util.MySqlUtil.mySqlJDBC;
import com.google.gson.JsonObject;
import io.milvus.client.*;
import org.apache.parquet.Strings;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

/**
 * @ClassName: ItemRecall
 * @Description: 根据用户最近3天浏览的论文，在Milvus中查找相似的1000篇论文
 * @author：贾敬哲
 * @date： 2020年12月15日15:48:38
 */
public class ItemRecall implements Recall {

    @Override
    public void train() {
        return;
    }

    @Override
    public Map<String, Double> predict(String paper_id) {
        return null;
    }

    @Override
    public void run() {
        try {
            ResultSet res = mySqlJDBC.getInstance().read(
                    "SELECT click_logs.u_id,papers.id,papers.doc_vector\n" +
                            "FROM\n" +
                            "(\n" +
                            "\tSELECT u_id,item_id FROM `click_log`\n" +
                            "\tWHERE event_type=1 AND add_time >= DATE_FORMAT(DATE_SUB(NOW(),INTERVAL 3 DAY),'%Y-%m-%d')\n" +
                            "\tGROUP BY u_id,item_id\n" +
                            ") click_logs\n" +
                            "INNER JOIN\n" +
                            "(\n" +
                            "\tSELECT id,doc_vector FROM `paper`\n" +
                            ") papers\n" +
                            "ON click_logs.item_id = papers.id\n"
            );

            Map<String, List<List<Float>>> uid2doc_vec = new HashMap<>();
            while (true) {
                if (!res.next()) {
                    break;
                }
                String uid = res.getString(1);
                String p_docvec = res.getString(3);
                List<List<Float>> tmp = null;
                if (!uid2doc_vec.containsKey(uid)) {
                    //进行初始化
                    tmp = new ArrayList<>();
                } else {
                    tmp = uid2doc_vec.get(uid);
                }

                // 处理每篇论文的vec
                String[] elems = p_docvec.split(",");
                List<Float> p_doclist = new ArrayList<>();
                for (String s : elems
                ) {
                    p_doclist.add(Float.parseFloat(s));
                }
                tmp.add(p_doclist);
                uid2doc_vec.put(uid, tmp);
            }

            for (String uid : uid2doc_vec.keySet()) {
                // 链接Milvus
                String host = "1.14.43.148";
                int port = 19530;
                ConnectParam connectParam = new ConnectParam.Builder().withHost(host).withPort(port).build();
                MilvusClient client = new MilvusGrpcClient(connectParam);

                List<List<Float>> vectorsToSearch = uid2doc_vec.get(uid);
                final long topK = 200;
                JsonObject searchParamsJson = new JsonObject();
                searchParamsJson.addProperty("nprobe", 16);
                SearchParam searchParam =
                        new SearchParam.Builder("ideaman")
                                .withFloatVectors(vectorsToSearch)
                                .withTopK(topK)
                                .withParamsInJson(searchParamsJson.toString())
                                .build();
                SearchResponse searchResponse = client.search(searchParam);
                List<List<Long>> resultIds = searchResponse.getResultIdsList();


                String item_ids = Strings.join((Iterator<String>) resultIds.get(0), ",");
                String sql = String.format("UPDATE user_rec SET item_recall = \"%s\" WHERE user_id = %s;\n",  item_ids , uid);
                mySqlJDBC.getInstance().write(sql);
            }

        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
    }

    public static void main(String[] args) {
        ItemRecall it = new ItemRecall();
        it.run();
    }
}
