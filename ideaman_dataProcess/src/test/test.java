import com.google.common.collect.Maps;
import com.google.gson.Gson;

import java.util.Map;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import java.util.Map;
public class test {
    public static void main(String[] args) {
        String str = "{\"headers\":{\"host\":\"localhost:7000\",\"connection\":\"keep-alive\",\"content-length\":\"696\",\"user-agent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36\",\"content-type\":\"application/x-www-form-urlencoded\",\"accept\":\"*/*\",\"origin\":\"http://localhost:8082\",\"sec-fetch-site\":\"same-site\",\"sec-fetch-mode\":\"cors\",\"sec-fetch-dest\":\"empty\",\"referer\":\"http://localhost:8082/about\",\"accept-encoding\":\"gzip, deflate, br\",\"accept-language\":\"zh-CN,zh;q=0.9,en;q=0.8\"},\"data\":{\"distinct_id\":\"2b0a6f51a3cd6775\",\"timeStamp\":1434556935000,\"event_type\":\"$Track\",\"event\":\"$PageView\",\"project\":\"project1\",\"properties\":{\"page_name\":\"网站首页\",\"url\":\"www.demo.com\",\"referer\":\"www.referer.com\",\"page_id\":\"/home\",\"page_path\":\"/home\",\"product_id\":12345,\"product_name\":\"物料1\",\"product_classify\":\"物料类型1\",\"product_price\":14,\"residence_time\":193000},\"system\":{\"$ip\":\"192.168.0.1\",\"$app_version\":\"1.3\",\"$wifi\":1,\"$province\":\"辽宁\",\"$city\":\"沈阳\",\"$user_agent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/58.0.3029.113 Mobile/14F89 Safari/602.1\",\"$screen_width\":320,\"$screen_height\":640},\"extra_para\":{}}}";
        //第一种方式
        Map maps = (Map) JSON.parse(str);
        System.out.println("这个是用JSON类来解析JSON字符串!!!");
        for (Object map : maps.entrySet()) {
            System.out.println(((Map.Entry) map).getKey() + "     " + ((Map.Entry) map).getValue());
        }
    }
}
