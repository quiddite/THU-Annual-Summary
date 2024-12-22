import pandas as pd
import json 
import os

if __name__ == '__main__':
    print('请输入年份')
    year = input()

    # 创建结果文件夹
    result_path = f'./results/{year}/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
        print(f'创建文件夹 {result_path}.')

    # 读取json文件
    with open(f'data_{year}.json', 'r') as f:
        data = json.load(f)
    #print(type(data))

    # 将有效数据转化为DataFrame
    df_origin = pd.DataFrame(data['resultData']['rows'])

    # 选择相关的列
    df = df_origin[['meraddr','mername','txamt','txdate','txname','username']]
    df['txamt'] = df['txamt'].astype(float)
    # 将金额转化为元，并保留两位小数
    df['txamt'] = df['txamt']/100
    df['txamt'] = df['txamt'].round(2)

    # 检查username
    username = df['username'].drop_duplicates()
    username = username.iloc[0]
    username = str(username)
    print('当前用户为：',username)

    # 存储username
    with open('username.txt', 'w') as f:
        f.write(username)

    # 将txdate转化为年月日时分秒
    df['year'] = df['txdate'].apply(lambda x: x[:4])
    df['month'] = df['txdate'].apply(lambda x: x[5:7])
    df['day'] = df['txdate'].apply(lambda x: x[8:10])
    df['hour'] = df['txdate'].apply(lambda x: x[11:13])
    df['minute'] = df['txdate'].apply(lambda x: x[14:16])
    df['second'] = df['txdate'].apply(lambda x: x[17:19])

    # 将处理过的有效信息表格保存为csv文件
    df.to_csv(result_path + f'data_{year}_{username}.csv',index=False,encoding='utf-8-sig')