import os
import csv
import time
import re
import requests
import json
import tqdm


# 宋浩高数156集
titles = []
cids = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}

def query_online_people(bvid, cid):
    """
    查询在线人数
    :param bvid: 视频av编号
    :param cid: 分p编号
    """
    url = f"https://api.bilibili.com/x/player/online/total?bvid={bvid}&cid={cid}"
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    online_people = data['data']['total']
    return online_people

def get_multiple_video_info(bvid):
    """
    获取多个分p的cid
    :param bvid: 视频bv号
    """
    global titles, cids
    url = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"查询失败，错误代码{response.status_code}")
        print(response.text)
        time.sleep(10)
        get_multiple_video_info(bvid)
        return
    data = json.loads(response.text)['data']
    cids = [p['cid'] for p in data]
    titles = [p['part'] for p in data]
    print(f"查询成功，共{len(cids)}个分p")


# get_multiple_video_info("BV1Eb411u7Fw")
def start(bvid, interval):
    """
    开始查询
    :param bvid: 视频bv号
    :param interval: 查询间隔，单位秒
    """
    # 表头存在则跳过
    with open(f"{bvid}_online_people.csv", "a", encoding="utf-8", newline="") as f:
        if os.path.getsize(f"{bvid}_online_people.csv") == 0:
            writer = csv.writer(f)
            writer.writerow([""] + titles)

    while True:
        online_people_list = []
        bar = tqdm.tqdm(total=len(cids))
        current_time = time.strftime("%Y-%m-%d %H:%M")
        for cid in cids:
            online_people = query_online_people(bvid, cid)
            online_people_list.append(online_people)
            # 写入新文件，文件名为bvid_online_people表头为每一p的标题，左侧一列为采样时间
            bar.update(1)
        with open(f"{bvid}_online_people.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([current_time] + online_people_list)
        print(f"{current_time} 采样完成")
        time.sleep(interval)

get_multiple_video_info("BV1Eb411u7Fw")
start("BV1Eb411u7Fw", 10*60)
