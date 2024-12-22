from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import json
import matplotlib.pyplot as plt
import requests
import platform

from matplotlib.ticker import MultipleLocator

def decrypt_aes_ecb(encrypted_data: str) -> str:
    
    key = encrypted_data[:16].encode('utf-8')
    encrypted_data = encrypted_data[16:]
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    
    cipher = AES.new(key, AES.MODE_ECB)
    
    decrypted_data = unpad(cipher.decrypt(encrypted_data_bytes), AES.block_size)

    return decrypted_data.decode('utf-8')

idserial = ""
servicehall = ""
all_data = dict()

if __name__ == "__main__":
    print("请输入年份：")
    year = input()
    year = str(year)
    print(type(year))

    # 读入账户信息
    try:
        with open("config.json", "r", encoding='utf-8') as f:
            account = json.load(f)
            idserial = account["idserial"]
            servicehall = account["servicehall"]
    except Exception as e:
        print("账户信息读取失败，请重新输入")
        idserial = input("请输入学号: ")
        servicehall = input("请输入服务代码: ")
        with open("config.json", "w", encoding='utf-8') as f:
            json.dump({"idserial": idserial, "servicehall": servicehall}, f, indent=4)
    
    # 发送请求，得到加密后的字符串
    url = f"https://card.tsinghua.edu.cn/business/querySelfTradeList?pageNumber=0&pageSize=5000&starttime={year}-01-01&endtime={year}-12-31&idserial={idserial}&tradetype=-1"
    cookie = {
        "servicehall": servicehall,
    }
    response = requests.post(url, cookies=cookie)

    # 解密字符串
    encrypted_string = json.loads(response.text)["data"]
    decrypted_string = decrypt_aes_ecb(encrypted_string)

    # 整理数据
    data = json.loads(decrypted_string)
    
    # 保存数据
    with open(f"data_{year}.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    for item in data["resultData"]["rows"]:
        try:
            if item["mername"] in all_data:
                all_data[item["mername"]] += item["txamt"]
            else:
                all_data[item["mername"]] = item["txamt"]
        except Exception as e:
            pass
    all_data = {k: round(v / 100, 2) for k, v in all_data.items()} # 将分转换为元，并保留两位小数
    print(type(all_data))

    # 保存数据
    with open(f"all_data_{year}.json", "w", encoding='utf-8') as f:
        json.dump(all_data, f, indent=4)


    print(len(all_data))
    # 输出结果
    all_data = dict(sorted(all_data.items(), key=lambda x: x[1], reverse=False))
    if platform.system() == "Darwin":
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    elif platform.system() == "Linux":
        plt.rcParams['font.family'] = ['Droid Sans Fallback', 'DejaVu Sans']
    else:
        plt.rcParams['font.sans-serif'] = ['SimHei']
    
    
    # plt.figure(figsize=(12, len(all_data) / 66 * 18))
    # plt.barh(list(all_data.keys()), list(all_data.values()))
    # for index, value in enumerate(list(all_data.values())):
    #     plt.text(value + 0.01 * max(all_data.values()),
    #             index,
    #             str(value),
    #             va='center')
        
    # # plt.tight_layout()
    # plt.xlim(0, 1.2 * max(all_data.values()))

    # # 设置 y 轴刻度，间隔为 5 或其他合适的值
    # plt.yticks(range(0, len(all_data), 5))
    
    # plt.title("华清大学食堂消费情况")
    # plt.xlabel("消费金额（元）")
    # plt.savefig("result.png")
    # plt.show()

    fig,ax = plt.subplots(figsize=(12, len(all_data) / 66 * 18))
    ax.barh(list(all_data.keys()), list(all_data.values()))

    total = sum(all_data.values())

    for index, value in enumerate(list(all_data.values())):
        ax.text(value + 0.01 * max(all_data.values()),
                index,
                str(value),
                va='center',fontsize=16)
    # 设置 y 轴刻度间距为 1
    ax.yaxis.set_major_locator(MultipleLocator(1))  # 设置刻度间隔为 1   
    # plt.tight_layout()
    plt.xlim(0, 1.2 * max(all_data.values()))
    plt.tick_params(axis='y', labelsize=10)  # 'both' 表示设置 x 和 y 轴的刻度字体大小为 5

    plt.text(0.5, 0.5, f"总消费金额：{total}元", fontsize=20, ha='center', va='center', transform=ax.transAxes)
    
    ax.set_title(f"华清大学食堂{year}年消费情况", fontsize=24)
    ax.set_xlabel("消费金额（元）")
    plt.savefig(f"result_{year}.png")
    plt.show()
