from ideaman_util.db import *
import pandas as pd
def download_data():
    sql = """SELECT
            title,
            description,
            tags,
            `authors`,
            doc_vector,
            pwc_tasks 
        FROM
            paper 
        WHERE
            pwc_tasks <> '' 
            AND doc_vector IS NOT NULL
        """
    cur.execute(sql)
    res = cur.fetchall()
    f = open("./data/paper.csv",'w',encoding='utf8')
    f.write("title|description|tags|authors|doc_vector|pwc_tasks\r\n")
    for i in res:
        txt = i[0] +"|" +i[1] +"|" +i[2]+"|" +i[3]+"|" +i[4]+"|" +i[5] +'\r\n'
        # print(txt)
        f.write(txt)
    f.close()

def load_data():
    dataframe = pd.read_csv("./data/paper.csv",sep='|' ,header=0)
    print(dataframe)

if __name__ == '__main__':
    download_data()
