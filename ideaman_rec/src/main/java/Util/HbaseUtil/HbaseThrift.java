package Util.HbaseUtil;

import org.apache.hadoop.hbase.thrift2.generated.*;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Properties;

public class HbaseThrift {
    public static HbaseThrift instance;

    private THBaseService.Iface client = null;
    private ByteBuffer table = null;
    private String ip = "";
    private int port = 0;

    private HbaseThrift() throws IOException {
        // 读取配置文件
        InputStream inputStream = new FileInputStream("src/main/resources/config.properties");
        Properties properties = new Properties();
        properties.load(inputStream);
        ip = properties.getProperty("hbasethrift.ip");
        port = Integer.parseInt(properties.getProperty("hbasethrift.port"));
    }

    public static synchronized HbaseThrift getInstance()  {
        if (instance == null) {
            try {
                instance = new HbaseThrift();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return instance;
    }

    public void init() throws TTransportException {
        //创建连接
        TTransport transport = new TSocket(this.ip, this.port, Integer.MAX_VALUE);
        TProtocol protocol = new TBinaryProtocol(transport);
        client = new THBaseService.Client(protocol);
        transport.open();

        //指定表名
        table = ByteBuffer.wrap("user_rec".getBytes());
    }

    public HashMap<String, String> Get_By_rowkey(String rowkey, String family_name, String col_name) throws TException {
        ByteBuffer row = ByteBuffer.wrap(rowkey.getBytes());
        ByteBuffer family = ByteBuffer.wrap(family_name.getBytes());
        ByteBuffer col = ByteBuffer.wrap(col_name.getBytes());
        //查询
        TGet get = new TGet();
        get.setRow(row);
        TColumn Tcol = new TColumn()
                .setFamily(family)
                .setQualifier(col);
        get.setColumns(Arrays.asList(Tcol));
        TResult result = client.get(table, get);
        //不指定列簇,即是获取所有列簇;
        System.out.println(new String(result.getRow()));
        HashMap<String, String> res = new HashMap<>();
        result.getColumnValues().forEach(c -> {
            System.out.println(new String(result.getRow()) + "  " + new String(c.getFamily()) + "_" + new String(c.getQualifier()) + ":" + new String(c.getValue()));
            res.put(new String(c.getFamily()) + ":" + new String(c.getQualifier()), new String(c.getValue()));
        });
        return res;
    }

    public HashMap<String, String> Get_By_rowkey(String rowkey, String family_name) throws TException {
        ByteBuffer row = ByteBuffer.wrap(rowkey.getBytes());
        ByteBuffer family = ByteBuffer.wrap(family_name.getBytes());
        //查询
        TGet get = new TGet();
        get.setRow(row);
        TColumn col = new TColumn().setFamily(family);
        get.setColumns(Arrays.asList(col));
        TResult result = client.get(table, get);
        //不指定列簇,即是获取所有列簇;
        System.out.println(new String(result.getRow()));
        HashMap<String, String> res = new HashMap<>();
        result.getColumnValues().forEach(c -> {
            System.out.println(new String(result.getRow()) + "  " + new String(c.getFamily()) + "_" + new String(c.getQualifier()) + ":" + new String(c.getValue()));
            res.put(new String(c.getFamily()) + ":" + new String(c.getQualifier()), new String(c.getValue()));
        });
        return res;

    }

    public void Put_By_rowkey(String rowkey, String family_name, String col_name, String Value) throws TException {
        ByteBuffer row = ByteBuffer.wrap(rowkey.getBytes());
        ByteBuffer family = ByteBuffer.wrap(family_name.getBytes());
        TPut put = new TPut();
        put.setRow(row);
        TColumnValue colVal = new TColumnValue();
        //定义属性值
        colVal.setFamily(family);
        colVal.setQualifier(col_name.getBytes());
        colVal.setValue(Value.getBytes());
        put.setColumnValues(Arrays.asList(colVal));
        client.put(table, put);
    }

    public static void main(String[] args) throws Exception {
        HbaseThrift test = new HbaseThrift();
        test.init();
        test.Get_By_rowkey("11", "sort");
        test.Put_By_rowkey("aaa", "sort", "test_thrift", "banana");
        test.Get_By_rowkey("aaa", "sort");
    }
}

