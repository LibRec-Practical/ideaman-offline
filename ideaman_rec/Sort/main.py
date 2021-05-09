# import random
#
# from milvus import Milvus, MetricType
# from DataSet import cur
#
# milvus = Milvus(host='1.14.43.148', port='19530')
#
# # param = "{'collection_name': 'ideaman', 'dimension': 128, 'index_file_size': 1024, 'metric_type': MetricType.L2}"
# # milvus.create_collection(param)
#
# # cur.execute("""SELECT id,doc_vector FROM paper
# # WHERE doc_vector <> ''
# # LIMIT 20;""")
# #
# # res = cur.fetchall()
# # vecs = []
# # ids = []
# # for i in res:
# #     id = i[0]
# #     vec = i[1].split(",")
# #     vec = [str(j) for j in vec]
# #     ids.append(id)
# #     vecs.append(vec)
# # milvus.insert('ideaman', records=vecs, ids=ids)
# # milvus.flush(collection_name_array=["ideaman"])
#
# print(milvus.get_collection_info('ideaman'))
# vec = "2.83141062e-03,-1.52981491e-03,-2.89479131e-03,1.11671735e-03,1.60708360e-03,1.65594276e-04,-2.53079087e-03,1.34985417e-03,1.52541237e-04,-2.08212249e-03,-2.50211428e-03,1.97276962e-03,-2.34853663e-03,2.83116620e-04,-3.28816148e-03,1.56361595e-04,-1.16526976e-03,-1.53907889e-03,2.48870347e-03,1.77415228e-03,1.01623498e-03,3.76819517e-04,7.30450498e-04,4.31343913e-04,5.65730035e-04,3.48676019e-03,2.62405281e-03,-8.81784246e-04,-1.57360721e-03,-1.15166500e-03,1.80622190e-03,3.71138495e-03,1.39448140e-03,-4.21128381e-04,2.63785385e-03,-1.41143287e-03,5.55513179e-06,9.61986254e-04,-3.47682717e-03,-1.33801228e-03,-6.48551213e-04,-2.03440432e-03,-1.62887663e-04,1.74150895e-03,-2.83462997e-03,2.56391871e-03,6.00477390e-04,5.99798048e-04,1.11659686e-03,1.73763768e-03,-1.10918292e-04,1.55647378e-03,-3.54456436e-03,1.78201572e-05,-1.38656038e-03,2.11979568e-04,-1.15091272e-03,-3.44586704e-04,-4.75173234e-04,-1.44363556e-03,-2.27558558e-04,2.26298091e-03,-1.32401870e-03,-3.01422621e-03,1.86910655e-03,-3.82621307e-03,-3.43073509e-03,-2.31505930e-03,-4.38009913e-04,3.38146533e-03,1.30376336e-03,-3.16078891e-04,-1.16388511e-03,-7.96445529e-04,-1.63145061e-03,1.33535825e-03,1.14564179e-03,-2.80131795e-03,3.30589293e-03,-1.40037481e-03,1.61177386e-03,-1.78966729e-03,-1.04177394e-04,-3.79238417e-03,3.65764648e-03,1.45591112e-04,3.46867228e-03,-2.86291144e-03,-1.17454142e-03,-2.69611808e-03,1.60712609e-03,-1.78643491e-03,-4.80060553e-05,1.68093015e-03,-5.58539003e-04,3.41827306e-03,2.46422249e-03,-1.40769628e-03,-1.90261262e-03,2.69527826e-03,-3.07544461e-03,-3.68624320e-03,7.84107833e-04,-1.73611077e-03,-2.09632446e-03,3.65290418e-03,1.62900728e-03,-2.11484614e-03,1.86304876e-03,-1.22147077e-03,2.40145088e-03,-3.65896500e-03,2.15274538e-03,1.78084895e-03,2.84394482e-03,-1.56630785e-03,-2.81768478e-03,8.59288906e-04,-1.00879418e-03,-5.88789815e-04,3.37906735e-04,-3.05184536e-03,-1.33803638e-03,-3.54570989e-03,3.56874708e-03,1.39728340e-03,-1.55330845e-03,-6.36251993e-04"
# vec = vec.split(",")
# vec = [str(j) for j in vec]
# print(milvus.get_collection_stats('ideaman'))
# search_param = "{'nprobe': 16}"
# print(len(vec))
# res = milvus.search(collection_name='ideaman', query_records=[vec], top_k=20, params=search_param)
# print(res)

import pymysql
import random

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=",/Qa+sk.mGB48", db="ideaman",
                       charset='utf8')
cur = conn.cursor()

for i in range(1, 3000):

    hot_recall = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    interestTag_recall = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    item_recall = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    topic_recall = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    als_recall = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    total_recall = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    lr_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    gbdt_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    lr_gbdt_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    dnn_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    deepcf_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    kd_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])
    total_sort = ",".join([str(random.randint(1, 100000)) for _ in range(200)])

    sql = """INSERT INTO user_rec VALUES("{id}","{hot_recall}","{interestTag_recall}","{item_recall}","{topic_recall}",
    "{als_recall}","{lr_sort}","{gbdt_sort}","{lr_gbdt_sort}","{dnn_sort}","{deepcf_sort}","{kd_sort}","{total_recall}" ,"{total_sort}")""".format(
        id=i,
        hot_recall=hot_recall,
        interestTag_recall=interestTag_recall,
        item_recall=item_recall,
        topic_recall=topic_recall,
        als_recall=als_recall,
        lr_sort=lr_sort,
        gbdt_sort=gbdt_sort,
        lr_gbdt_sort=lr_gbdt_sort,
        dnn_sort=dnn_sort,
        deepcf_sort=deepcf_sort,
        kd_sort=kd_sort,
        total_recall=total_recall,
        total_sort=total_sort
    )
    cur.execute(sql)
