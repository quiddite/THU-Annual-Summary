# 整理相关参数，并记录到csv文件中

import pandas as pd
import numpy as np
import json 
import os
import matplotlib.pyplot as plt

import platform

if __name__ == '__main__':
    print('请输入年份')
    year = input()

    
    # 创建结果文件夹
    result_path = f'./results/{year}/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
        print(f'创建文件夹 {result_path}.')    
    
    # 读取username
    with open('username.txt', 'r') as f:
        username = f.read()
    print('当前用户为：',username)

    print(f"请输入你所涉及的宿舍楼，请保持与原始数据一致(如紫荆公寓6号楼)，\n可查看",result_path + f'data_{year}_{username}.csv','中的meraddr列')
    apt = input()
    apt = str(apt)

    # 读取数据
    df_all = pd.read_csv(result_path + f'data_{year}_{username}.csv')

    # 去除在线充值的数据
    df = df_all[df_all['meraddr']!='在线充值']

    # 定义记录df
    record = list()

    # 记录总交易金额与次数
    record.append({'事项':'总交易金额与次数','金额':df['txamt'].sum(),'时间':f'{year}年{df.shape[0]}次','地点':'无'})

    # 记录单次交易金额最大值
    max_txamt = df['txamt'].max()
    df_max_txamt = df[df['txamt']==max_txamt]
    df_max_txamt = df_max_txamt.iloc[0]
    record.append({'事项':'单次交易金额最大值','金额':df_max_txamt['txamt'],'时间':f'{year}年{df_max_txamt["month"]}月{df_max_txamt["day"]}日{df_max_txamt["hour"]}时{df_max_txamt["minute"]}分{df_max_txamt["second"]}秒','地点':df_max_txamt['mername']})

    # 记录单次交易金额最小值
    min_txamt = df['txamt'].min()
    df_min_txamt = df[df['txamt']==min_txamt]
    df_min_txamt = df_min_txamt.iloc[0]
    record.append({'事项':'单次交易金额最小值','金额':df_min_txamt['txamt'],'时间':f'{year}年{df_min_txamt["month"]}月{df_min_txamt["day"]}日{df_min_txamt["hour"]}时{df_min_txamt["minute"]}分{df_min_txamt["second"]}秒','地点':df_min_txamt['mername']})

    # 记录交易金额均值
    record.append({'事项':'交易金额均值','金额':df['txamt'].mean(),'时间':f'{year}年','地点':'无'})

    # 记录交易金额分月最大值和最小值，如果有月份没有交易记录，则补充其交易金额为0
    df_month = df.groupby('month')['txamt'].sum()
    df_month = df_month.sort_index()
    #df_month = df_month.reindex(index=['01','02','03','04','05','06','07','08','09','10','11','12'],fill_value=0)
    df_month = df_month.reindex(index=[1,2,3,4,5,6,7,8,9,10,11,12],fill_value=0)
    max_month = df_month.idxmax()
    record.append({'事项':'交易金额分月最大值','金额':df_month.max(),'时间':f'{year}年{max_month}月','地点':'无'})

    min_month = df_month.idxmin()
    record.append({'事项':'交易金额分月最小值','金额':df_month.min(),'时间':f'{year}年{min_month}月','地点':'无'})

    # 记录交易金额分地点最大值和最小值
    df_addr = df.groupby('meraddr')['txamt'].sum()
    max_addr = df_addr.idxmax()
    record.append({'事项':'交易金额分地点最大值','金额':df_addr.max(),'时间':f'{year}年','地点':max_addr})

    min_addr = df_addr.idxmin()
    record.append({'事项':'交易金额分地点最小值','金额':df_addr.min(),'时间':f'{year}年','地点':min_addr})

    # 记录交易金额分时间最大值和最小值
    df_hour = df.groupby('hour')['txamt'].sum()
    df_hour = df_hour.sort_index()
    max_hour = df_hour.idxmax()
    record.append({'事项':'交易金额分时间最大值','金额':df_hour.max(),'时间':f'{year}年{max_hour}时','地点':'无'})

    min_hour = df_hour.idxmin()
    record.append({'事项':'交易金额分时间最小值','金额':df_hour.min(),'时间':f'{year}年{min_hour}时','地点':'无'})

    # 记录分月与天交易金额最大值和最小值    
    max_month_day = df.groupby(['month','day'])['txamt'].sum().max()
    max_month_day_index = df.groupby(['month','day'])['txamt'].sum().idxmax()
    record.append({'事项':'分月与天交易金额最大值','金额':max_month_day,'时间':f'{year}年{max_month_day_index[0]}月{max_month_day_index[1]}日','地点':'无'})

    min_month_day = df.groupby(['month','day'])['txamt'].sum().min()
    min_month_day_index = df.groupby(['month','day'])['txamt'].sum().idxmin()
    record.append({'事项':'分月与天交易金额最小值','金额':min_month_day,'时间':f'{year}年{min_month_day_index[0]}月{min_month_day_index[1]}日','地点':'无'})

    # 记录最常去的地点及相对应的花费与次数，找到出现次数最多的mername，排除紫荆公寓6号楼、自助打印成绩单、学生卡成本
    df_addr = df[df['meraddr']!=apt]
    df_addr = df_addr[df_addr['meraddr']!='自助打印成绩单']
    df_addr = df_addr[df_addr['mername']!='学生卡成本']
    df_addr_count = df_addr['meraddr'].value_counts()
    max_addr = df_addr_count.idxmax()
    addr_count = df_addr_count.max()
    addr_monney = df_addr[df_addr['meraddr']==max_addr]['txamt'].sum()  
    record.append({'事项':'最常去的食堂','金额':addr_monney,'时间':f'{year}年共{addr_count}次','地点':max_addr})

    #记录去过的食堂
    addr_list = df_addr['meraddr'].unique()
    addr_list = addr_list.tolist()
    addr_number = len(addr_list)
    record.append({'事项':'去过的食堂','金额':None,'时间':f'{year}年共{addr_number}个','地点':addr_list})


    # 记录最常去的窗口及相对应的花费与次数，找到出现次数最多的mername，排除紫荆公寓6号楼、自助打印成绩单、学生卡成本
    df_name = df[df['meraddr']!=apt]
    df_name = df_name[df_name['mername']!='自助打印成绩单']
    df_name = df_name[df_name['mername']!='学生卡成本']
    df_name_count = df_name['mername'].value_counts()
    max_name = df_name_count.idxmax()
    name_count = df_name_count.max()
    name_monney = df_name[df_name['mername']==max_name]['txamt'].sum()
    record.append({'事项':'最常去的窗口','金额':name_monney,'时间':f'{year}年共{name_count}次','地点':max_name})

    #记录去过的窗口总数
    name_list = df_name['mername'].unique()
    name_list = name_list.tolist()
    name_number = len(name_list)
    record.append({'事项':'去过的窗口','金额':None,'时间':f'{year}年共{name_number}个','地点':name_list})

    # 记录累计消费最多的食堂及相对应的花费，找到总消费金额最大的meraddr，排除紫荆公寓6号楼、自助打印成绩单
    max_addr_cost = df_addr.groupby('meraddr')['txamt'].sum().idxmax()
    max_addr_cost_monney = df_addr.groupby('meraddr')['txamt'].sum().max()
    record.append({'事项':'累计消费最多的食堂','金额':max_addr_cost_monney,'时间':f'{year}年','地点':max_addr_cost})

    # 记录累计消费最多的窗口及相对应的花费，找到总消费金额最大的mername，排除紫荆公寓6号楼、自助打印成绩单
    max_name_cost = df_name.groupby('mername')['txamt'].sum().idxmax()
    max_name_cost_monney = df_name.groupby('mername')['txamt'].sum().max()
    record.append({'事项':'累计消费最多的窗口','金额':max_name_cost_monney,'时间':f'{year}年','地点':max_name_cost})


    # 早餐：筛选出hour在4——9点的数据，排除meraddr为紫荆公寓6号楼、自助打印成绩单、学生卡成本的数据
    df_breakfast = df[(df['hour']==4)|(df['hour']==5)|(df['hour']==6)|(df['hour']==7)|(df['hour']==8)|(df['hour']==9)|(df['hour']=='4')|(df['hour']=='5')|(df['hour']=='6')|(df['hour']=='7')|(df['hour']=='8')|(df['hour']=='9')|(df['hour']=='04')|(df['hour']=='05')|(df['hour']=='06')|(df['hour']=='07')|(df['hour']=='08')|(df['hour']=='09')]
    #print(df_breakfast)
    df_breakfast = df_breakfast[(df_breakfast['meraddr']!=apt)&(df_breakfast['mername']!='自助打印成绩单')&(df_breakfast['mername']!='学生卡成本')]

    # 记录吃早餐最早时间，找到最接近6的一条数据，按照minute、second依次检索得最小的一条数据
    df_breakfast_early = df_breakfast.sort_values(by=['hour','minute','second'])
    
    df_breakfast_earliest = df_breakfast_early.iloc[0]
    record.append({'事项':'吃早餐最早时间','金额':df_breakfast_earliest['txamt'],'时间':f'{year}年{df_breakfast_earliest["month"]}月{df_breakfast_earliest["day"]}日{df_breakfast_earliest["hour"]}时{df_breakfast_earliest["minute"]}分{df_breakfast_earliest["second"]}秒','地点':df_breakfast_earliest['mername']})

    # 记录吃早餐最晚时间，找到按照minute、second依次检索得最大的一条数据
    df_breakfast_late = df_breakfast.sort_values(by=['hour','minute','second'],ascending=False)
    df_breakfast_latest = df_breakfast_late.iloc[0]
    record.append({'事项':'吃早餐最晚时间','金额':df_breakfast_latest['txamt'],'时间':f'{year}年{df_breakfast_latest["month"]}月{df_breakfast_latest["day"]}日{df_breakfast_latest["hour"]}时{df_breakfast_latest["minute"]}分{df_breakfast_latest["second"]}秒','地点':df_breakfast_latest['mername']})

    # 记录吃早餐的总次数，并且同一天的数据只算一次
    breakfast_monney = df_breakfast['txamt'].sum()
    df_breakfast_count_a_day = df_breakfast.groupby(['month','day']).count()
    df_breakfast_count = df_breakfast_count_a_day.shape[0]
    record.append({'事项':'吃早餐总次数','金额':breakfast_monney,'时间':f'{year}年共{df_breakfast_count}次','地点':'无'})

    # 记录吃早餐最常去的地点及相对应的花费与次数，找到出现次数最多的meraddr，并且同一天的数据只算一次
    df_breakfast_by_day = df_breakfast.drop_duplicates(subset=['month','day'])
    df_breakfast_addr = df_breakfast_by_day['meraddr'].value_counts()
    max_breakfast_addr = df_breakfast_addr.idxmax()
    breakfast_addr_count = df_breakfast_addr.max()
    breakfast_addr_monney = df_breakfast[df_breakfast['meraddr']==max_breakfast_addr]['txamt'].sum()
    record.append({'事项':'吃早餐最常去的食堂','金额':breakfast_addr_monney,'时间':f'{year}年共{breakfast_addr_count}次','地点':max_breakfast_addr})

    # 记录吃早餐最常去的窗口及相对应的花费与次数，找到出现次数最多的mername
    df_breakfast_name = df_breakfast['mername'].value_counts()
    max_breakfast_name = df_breakfast_name.idxmax()
    breakfast_name_count = df_breakfast_name.max()
    breakfast_name_monney = df_breakfast[df_breakfast['mername']==max_breakfast_name]['txamt'].sum()
    record.append({'事项':'吃早餐最常去的窗口','金额':breakfast_name_monney,'时间':f'{year}年共{breakfast_name_count}次','地点':max_breakfast_name})


    # 午饭：筛选出hour在10——13点的数据，排除meraddr为紫荆公寓6号楼、自助打印成绩单的数据
    df_lunch = df[(df['hour']==10)|(df['hour']==11)|(df['hour']==12)|(df['hour']==13)|(df['hour']=='10')|(df['hour']=='11')|(df['hour']=='12')|(df['hour']=='13')]
    df_lunch = df_lunch[(df_lunch['meraddr']!=apt)&(df_lunch['mername']!='自助打印成绩单')&(df_lunch['mername']!='学生卡成本')]

    # 记录吃午饭最早的时间，按照minute、second依次检索得最小的一条数据
    df_lunch_early = df_lunch.sort_values(by=['hour','minute','second'])
    df_lunch_earliest = df_lunch_early.iloc[0]
    record.append({'事项':'吃午饭最早时间','金额':df_lunch_earliest['txamt'],'时间':f'{year}年{df_lunch_earliest["month"]}月{df_lunch_earliest["day"]}日{df_lunch_earliest["hour"]}时{df_lunch_earliest["minute"]}分{df_lunch_earliest["second"]}秒','地点':df_lunch_earliest['mername']})

    # 记录吃午饭最晚时间，找到按照minute、second依次检索得最大的一条数据
    df_lunch_late = df_lunch.sort_values(by=['hour','minute','second'],ascending=False)
    df_lunch_latest = df_lunch_late.iloc[0]
    record.append({'事项':'吃午饭最晚时间','金额':df_lunch_latest['txamt'],'时间':f'{year}年{df_lunch_latest["month"]}月{df_lunch_latest["day"]}日{df_lunch_latest["hour"]}时{df_lunch_latest["minute"]}分{df_lunch_latest["second"]}秒','地点':df_lunch_latest['mername']})

    # 记录吃午饭的总次数，并且同一天的数据只算一次
    lunch_monney = df_lunch['txamt'].sum()
    df_lunch_count_a_day = df_lunch.groupby(['month','day']).count()
    df_lunch_count = df_lunch_count_a_day.shape[0]
    record.append({'事项':'吃午饭总次数','金额':lunch_monney,'时间':f'{year}年共{df_lunch_count}次','地点':'无'})

    # 记录吃午饭最常去的地点及相对应的花费与次数，找到出现次数最多的meraddr，并且同一天的数据只算一次
    df_lunch_by_day = df_lunch.drop_duplicates(subset=['month','day'])
    df_lunch_addr = df_lunch_by_day['meraddr'].value_counts()
    max_lunch_addr = df_lunch_addr.idxmax()
    lunch_addr_count = df_lunch_addr.max()
    lunch_addr_monney = df_lunch[df_lunch['meraddr']==max_lunch_addr]['txamt'].sum()
    record.append({'事项':'吃午饭最常去的食堂','金额':lunch_addr_monney,'时间':f'{year}年共{lunch_addr_count}次','地点':max_lunch_addr})

    # 记录吃午饭最常去的窗口及相对应的花费与次数，找到出现次数最多的mername
    df_lunch_name = df_lunch['mername'].value_counts()
    max_lunch_name = df_lunch_name.idxmax()
    lunch_name_count = df_lunch_name.max()
    lunch_name_monney = df_lunch[df_lunch['mername']==max_lunch_name]['txamt'].sum()
    record.append({'事项':'吃午饭最常去的窗口','金额':lunch_name_monney,'时间':f'{year}年共{lunch_name_count}次','地点':max_lunch_name})


    # 晚饭：筛选出hour在16——19点的数据，排除meraddr为紫荆公寓6号楼、自助打印成绩单、学生卡成本的数据
    df_dinner = df[(df['hour']==16)|(df['hour']==17)|(df['hour']==18)|(df['hour']==19)|(df['hour']=='16')|(df['hour']=='17')|(df['hour']=='18')|(df['hour']=='19')]
    df_dinner = df_dinner[(df_dinner['meraddr']!=apt)&(df_dinner['mername']!='自助打印成绩单')&(df_dinner['mername']!='学生卡成本')]

    # 记录吃晚饭最早时间，找到最接近17的一条数据，按照minute、second依次检索得最小的一条数据
    df_dinner_early = df_dinner.sort_values(by=['hour','minute','second'])
    df_dinner_earliest = df_dinner_early.iloc[0]
    record.append({'事项':'吃晚饭最早时间','金额':df_dinner_earliest['txamt'],'时间':f'{year}年{df_dinner_earliest["month"]}月{df_dinner_earliest["day"]}日{df_dinner_earliest["hour"]}时{df_dinner_earliest["minute"]}分{df_dinner_earliest["second"]}秒','地点':df_dinner_earliest['mername']})

    # 记录吃晚饭最晚时间，，找到按照minute、second依次检索得最大的一条数据
    df_dinner_late = df_dinner.sort_values(by=['hour','minute','second'],ascending=False)
    df_dinner_latest = df_dinner_late.iloc[0]
    record.append({'事项':'吃晚饭最晚时间','金额':df_dinner_latest['txamt'],'时间':f'{year}年{df_dinner_latest["month"]}月{df_dinner_latest["day"]}日{df_dinner_latest["hour"]}时{df_dinner_latest["minute"]}分{df_dinner_latest["second"]}秒','地点':df_dinner_latest['mername']})

    # 记录吃晚饭的总次数，筛选出hour在16——18点的数据，并且同一天的数据只算一次，排除meraddr为紫荆公寓6号楼、自助打印成绩单的数据
    dinner_monney = df_dinner['txamt'].sum()
    df_dinner_count_a_day = df_dinner.groupby(['month','day']).count()
    df_dinner_count = df_dinner_count_a_day.shape[0]
    record.append({'事项':'吃晚饭总次数','金额':dinner_monney,'时间':f'{year}年共{df_dinner_count}次','地点':'无'})

    # 记录吃晚饭最常去的地点及相对应的花费与次数，找到出现次数最多的meraddr，并且同一天的数据只算一次
    df_dinner_by_day = df_dinner.drop_duplicates(subset=['month','day'])
    df_dinner_addr = df_dinner_by_day['meraddr'].value_counts()
    max_dinner_addr = df_dinner_addr.idxmax()
    dinner_addr_count = df_dinner_addr.max()
    dinner_addr_monney = df_dinner[df_dinner['meraddr']==max_dinner_addr]['txamt'].sum()
    record.append({'事项':'吃晚饭最常去的食堂','金额':dinner_addr_monney,'时间':f'{year}年共{dinner_addr_count}次','地点':max_dinner_addr})

    # 记录吃晚饭最常去的窗口及相对应的花费与次数，找到出现次数最多的mername
    df_dinner_name = df_dinner['mername'].value_counts()
    max_dinner_name = df_dinner_name.idxmax()
    dinner_name_count = df_dinner_name.max()
    dinner_name_monney = df_dinner[df_dinner['mername']==max_dinner_name]['txamt'].sum()
    record.append({'事项':'吃晚饭最常去的窗口','金额':dinner_name_monney,'时间':f'{year}年共{dinner_name_count}次','地点':max_dinner_name})


    # 吃宵夜：筛选出hour在20——23点的数据，排除meraddr为紫荆公寓6号楼、自助打印成绩单的数据
    df_midnight = df[(df['hour']==20)|(df['hour']==21)|(df['hour']==22)|(df['hour']==23)|(df['hour']=='20')|(df['hour']=='21')|(df['hour']=='22')|(df['hour']=='23')]
    df_midnight = df_midnight[(df_midnight['meraddr']!=apt)&(df_midnight['mername']!='自助打印成绩单')]

    # 记录吃宵夜最早时间，找到最接近20的一条数据
    df_midnight_early = df_midnight.sort_values(by=['hour','minute','second'])
    df_midnight_earliest = df_midnight_early.iloc[0]
    record.append({'事项':'吃宵夜最早时间','金额':df_midnight_earliest['txamt'],'时间':f'{year}年{df_midnight_earliest["month"]}月{df_midnight_earliest["day"]}日{df_midnight_earliest["hour"]}时{df_midnight_earliest["minute"]}分{df_midnight_earliest["second"]}秒','地点':df_midnight_earliest['mername']})

    # 记录吃宵夜最晚时间，找到按照minute、second依次检索得最大的一条数据
    df_midnight_late = df_midnight.sort_values(by=['hour','minute','second'],ascending=False)
    df_midnight_latest = df_midnight_late.iloc[0]
    record.append({'事项':'吃宵夜最晚时间','金额':df_midnight_latest['txamt'],'时间':f'{year}年{df_midnight_latest["month"]}月{df_midnight_latest["day"]}日{df_midnight_latest["hour"]}时{df_midnight_latest["minute"]}分{df_midnight_latest["second"]}秒','地点':df_midnight_latest['mername']})

    # 记录吃宵夜的总次数，并且同一天的数据只算一次
    midnight_monney = df_midnight['txamt'].sum()
    df_midnight_count_a_day = df_midnight.groupby(['month','day']).count()
    df_midnight_count = df_midnight_count_a_day.shape[0]
    record.append({'事项':'吃宵夜总次数','金额':midnight_monney,'时间':f'{year}年共{df_midnight_count}次','地点':'无'})

    # 记录吃宵夜最常去的地点及相对应的花费与次数，找到出现次数最多的meraddr，并且同一天的数据只算一次
    df_midnight_by_day = df_midnight.drop_duplicates(subset=['month','day'])
    df_midnight_addr = df_midnight_by_day['meraddr'].value_counts()
    max_midnight_addr = df_midnight_addr.idxmax()
    midnight_addr_count = df_midnight_addr.max()
    midnight_addr_monney = df_midnight[df_midnight['meraddr']==max_midnight_addr]['txamt'].sum()
    record.append({'事项':'吃宵夜最常去的食堂','金额':midnight_addr_monney,'时间':f'{year}年共{midnight_addr_count}次','地点':max_midnight_addr})

    # 记录吃宵夜最常去的窗口及相对应的花费与次数，找到出现次数最多的mername
    df_midnight_name = df_midnight['mername'].value_counts()
    max_midnight_name = df_midnight_name.idxmax()
    midnight_name_count = df_midnight_name.max()
    midnight_name_monney = df_midnight[df_midnight['mername']==max_midnight_name]['txamt'].sum()
    record.append({'事项':'吃宵夜最常去的窗口','金额':midnight_name_monney,'时间':f'{year}年共{midnight_name_count}次','地点':max_midnight_name})


    # 洗澡：筛选出meraddr为紫荆公寓6号楼的数据
    df_bath = df[df['meraddr']==apt]

    # 记录洗澡最晚时间，找到hour为0或者23及以前，按照minute、second依次检索得最大的一条数据
    df_bath_late = df_bath[(df_bath['hour']==0)|(df_bath['hour']=='00')|(df_bath['hour']=='0')(df_bath['hour']==1)|(df_bath['hour']=='01')|(df_bath['hour']=='1')]
    if df_bath_late.shape[0] == 0:
        df_bath_late = df_bath[(df_bath['hour']==23)|(df_bath['hour']=='23')|(df_bath['hour']==22)|(df_bath['hour']=='22')|(df_bath['hour']==21)|(df_bath['hour']=='21')|(df_bath['hour']==20)|(df_bath['hour']=='20')|(df_bath['hour']==19)|(df_bath['hour']=='19')|(df_bath['hour']==18)|(df_bath['hour']=='18')|(df_bath['hour']==17)|(df_bath['hour']=='17')|(df_bath['hour']==16)|(df_bath['hour']=='16')]
    
    df_bath_late = df_bath_late.sort_values(by=['minute','second'],ascending=False)
    df_bath_latest = df_bath_late.iloc[0]
    record.append({'事项':'洗澡最晚时间','金额':df_bath_latest['txamt'],'时间':f'{year}年{df_bath_latest["month"]}月{df_bath_latest["day"]}日{df_bath_latest["hour"]}时{df_bath_latest["minute"]}分{df_bath_latest["second"]}秒','地点':df_bath_latest['mername']})

    # 记录最常洗澡的时间，找到出现次数最多的hour
    df_bath_hour = df_bath['hour'].value_counts()
    max_bath = df_bath_hour.idxmax()

    if max_bath != 23:
        max_bath_end = int(max_bath) + 1
    else:
        max_bath_end = 0

    record.append({'事项':'最常洗澡时间','金额':df_bath_hour.max(),'时间':f'{year}年{max_bath}点到{max_bath_end}点','地点':df_bath_latest['mername']})

    # 记录洗澡的总次数
    bath_monney = df_bath['txamt'].sum()
    record.append({'事项':'洗澡总次数','金额':bath_monney,'时间':f'{year}年{df_bath.shape[0]}次','地点':df_bath_latest['mername']})


    # 整理记录为DataFrame
    df_record = pd.DataFrame(record)

    # 金额设置为两位小数
    df_record['金额'] = df_record['金额'].round(2)

    # 将记录保存为csv文件
    df_record.to_csv(result_path + f'{username}_{year}年校园卡交易总结记录.csv',index=False,encoding='utf-8-sig')

