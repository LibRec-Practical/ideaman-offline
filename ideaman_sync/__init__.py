import milvus
import sys, os

sys.path.append("../../")
sys.path.extend([os.path.join(root, name) for root, dirs, _ in os.walk("../../") for name in dirs])
from ideaman_util.paper import Paper
from ideaman_util.config import *
from ideaman_util.db import conn, cur

from milvus import Milvus

def run_offline_paper():
    client = Milvus(host='42.193.21.38', port='19530')
    cur.execute("SELECT ID ,doc_vector FROM paper ORDER BY id LIMIT 2000")
    papers = cur.fetchall()
    for i in papers:
        id = i[0]
        vec = i[1].split(",")
        vec = [eval(j) for j in vec]
        res = client.search(collection_name='ideaman', query_records=[vec], top_k=51)

        status = res[0].code
        if status == 0:
            topKqueryResult = [str(j) for j in res[-1]._id_array[0]]
            paper_vecs = ",".join(topKqueryResult[1:])
            sql = 'INSERT INTO offline_paper(paper_id , recs) VALUES({} , "{}")'.format(id, paper_vecs)
            cur.execute(sql)
            conn.commit()
if __name__ == '__main__':
    client = Milvus(host='42.193.21.38', port='19530')
    print(client.get_collection_stats(collection_name="ideaman"))
    print(client.get_collection_info("ideaman"))
    run_offline_paper()
    # client.drop_collection("ideaman")
    # param = {'collection_name': 'ideaman', 'dimension': 128, 'index_file_size': 1024, 'metric_type': MetricType.L2}
    # client.create_collection(param)