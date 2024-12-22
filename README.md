# THU-Annual-Summary

本项目在[Ze-en Xiong](https://github.com/leverimmy)的THU-Annual-Eat的基础上，对数据进行进一步处理与分析，可以获得THU校园卡年度消费报告。

另外，应该只能获取到2023年7月以后的数据，因此获取的2023年数据只有后半年。

## 0.申明

> 项目数据获取主体框架来源于[Ze-en Xiong](https://github.com/leverimmy)。

> 项目的 idea 来源于 [Rose-max111](https://github.com/Rose-max111)。

> 项目的数据分析与展示制作由本人[Zang Lee](https://github.com/MrZang27)完成。

## 1.获取数据

> 项目数据获取方式请见[数据获取](https://github.com/leverimmy/THU-Annual-Eat)。

ps:需要保证[校园卡网页](https://card.tsinghua.edu.cn/userselftrade)处于登录状态，如果重新登录，则需要在 `config.json`文件中更新servicehall再运行。

注意，请使用本仓库的 `main.py`文件。

如果直接使用[数据获取](https://github.com/leverimmy/THU-Annual-Eat)中的 `main.py`文件，并且在适当位置增加如下代码以实现获取不同年份数据，并存储数据：

```
    print("请输入年份：")
    year = input()
    year = str(year)
```

存储数据：

```
    with open(f"data_{year}.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)
```

另外，如果自行修改，请把[数据获取](https://github.com/leverimmy/THU-Annual-Eat)中的 `main.py`代码中的 `url`改为如下内容：

```
    # 发送请求，得到加密后的字符串
    url = f"https://card.tsinghua.edu.cn/business/querySelfTradeList?pageNumber=0&pageSize=5000&starttime={year}-01-01&endtime={year}-12-31&idserial={idserial}&tradetype=-1"
    cookie = {
        "servicehall": servicehall,
    }
```

以上操作进行完成后，运行 `main.py`文件，输入所获取数据的年份（4位纯数字，如：2024）。

**如果直接用本仓库 `main.py`文件，可忽略以上内容。**

最终可获得记录了原始数据的 `data_{year}.json`文件。

请勿删除该文件，后续数据处理需要使用。

## 2.数据展示

### 2.1安装依赖

本项目依赖于 `requests`、`matplotlib` 、`pandas`、`numpy`、`platform`和 `pycryptodome`，请确保你的 Python 环境中已经安装了这些库。

```bash
pip install requests matplotlib pycryptodome pandas numpy platform
```

> 你可能需要在 `Python\Python312\Lib\site-packages` 目录下将 `crypto` 文件夹改名为 `Crypto`。

### 2.2数据处理

当获取到 `data_{year}.json`文件后，**运行 `convert_data.py`文件**，输入对应的年份（4位纯数字如：2024），

可以得到记录了有效数据的 `data_{year}_{username}.csv`表格与记录了当前用户名的 `username.txt`文件，会自动存储于结果文件夹 `./results/`中，请勿删除，后续数据分析需要使用。

### 2.3数据分析

当获得 `data_{year}_{username}.csv`表格后，**运行 `record_data.py`文件**，输入对应的年份（4位纯数字如：2024），以及你的消费所涉及的宿舍楼（请保持与表格中meraddr列所记录的一致，如：紫荆公寓6号楼）

可以得到一个记录有 “事项”、“金额”、“时间/次数”、“地点” 的表格 `{username}_{year}年校园卡交易总结记录.csv`，存储于结果文件夹 `./results/`中，具体记录事项可自行于 `record_data.py`文件中增删。

请勿删除该文件，后续年度总结需要使用。


注意：请将所有涉及到宿舍楼的内容（如"紫荆公寓6号楼")更替为你自己所在的宿舍楼或你去洗过澡的宿舍楼

### 2.4数据可视化

当获得 `data_{year}_{username}.csv`表格后，**运行 `show_data.py`文件**，输入对应的年份（4位纯数字如：2024），

另外，部分图像可能需要自行调整参数，可以通过 `ctrl+F`查找关键字 `TODO`，包括 `show_data.py`第236—237行的：

```
#TODO: 为了避免互相重叠，这里的坐标需要调整，请自行调整调整下行0.2和0.13的值
plt.text(b-(0.2-a*0.13),int(df_addr_count.iloc[b,a]),int(df_addr_count.iloc[b,a]),ha='center',va='bottom',fontsize=8)
```

和 `show_data.py`第280—281行的：

```
#TODO: 为了避免互相重叠，这里的坐标需要调整，请自行调整调整下行0.21和0.07的值
plt.text(a - (0.21 - b*0.07),int(df_name_count.iloc[a,b]),int(df_name_count.iloc[a,b]),ha='center',va='bottom',fontsize=8)
```

可以得到部分数据的可视化图像（包含柱状图、饼图），存储于结果文件夹 `./results/`中，具体绘图内容可自行增删。

请勿删除该文件，后续年度总结需要使用。

## 3.年度总结

当获得 `{username}_{year}年校园卡交易总结记录.csv`表格与部分数据的可视化图像后，**运行 `make_report.py`文件**，输入对应的年份（4位纯数字如：2024），

即可获得你的华清大学校园卡年度总结报告 `Annual_Summary_{year}.md`。

值得注意的是，2023年数据应该只有7月及以后的数据，因此2023年的总结实际为半年总结。

最后，可以自行将所获得的.md文件转化为pdf文件方便阅读。

以下是以本人2024年年度报告为示例：

![图片](Example_Annual_Summary_2024.png)
