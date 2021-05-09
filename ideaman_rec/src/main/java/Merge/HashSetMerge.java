package Merge;

import Util.HbaseUtil.HbaseThrift;
import org.apache.thrift.TException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

/**
 * @author pytho
 */
public class HashSetMerge implements Merge {
    public String rowkey = "";
    public HashSet<Integer> idSet = new HashSet<Integer>();
    public ArrayList<String> colNames = new ArrayList<String>();

    // 格式为 "列族名:列名"
    public HashSetMerge(String rowkey, ArrayList<String> colNames) {
        this.rowkey = rowkey;
        this.colNames = colNames;
    }

    public String readHbase() throws TException {
        ArrayList<String> list = new ArrayList<String>();
        for (String s : colNames) {
            String[] s_list = s.split(":");
            HashMap<String, String> recall_res = HbaseThrift.getInstance().Get_By_rowkey(this.rowkey, s_list[0], s_list[1]);
            list.add(recall_res.getOrDefault(s, ""));
        }

        return String.join(",", list);
    }

    @Override
    public String merge() {
        try {
            String ids = this.readHbase();
            String[] id_list = ids.split(",");
            for (int i = 0; i < id_list.length; i++) {
                this.idSet.add(i);
            }
            String[] id_set = new String[this.idSet.size()];
            this.idSet.toArray(id_set);
            return String.join(",", id_set);
        } catch (TException e) {
            e.printStackTrace();
        }
        return null;
    }
}
