import cloudscraper
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from datetime import datetime

# 创建爬虫对象（绕开反爬）
scraper = cloudscraper.create_scraper()
# 要爬取的网站（广东政府+学习强国，公开数据）
urls = [
    "https://www.gd.gov.cn/gkmlpt/zczc/index",  # 广东政府政策（名言素材）
    "https://www.xuexi.cn/lgpage/detail/index.html?id=xxx"  # 学习强国广东频道
]

# 存储题库和名言数据
questions = []  # 行测/申论题库
quotes = []     # 申论名言库

# 爬取名言（先做简单的，后续再补题库）
for url in urls:
    try:
        # 发送请求（模拟浏览器）
        response = scraper.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"})
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 提取名言（根据网页结构，这里用示例选择器，能爬多少算多少）
        quote_elements = soup.select("p")  # 暂时提取所有段落，后续可优化
        for elem in quote_elements:
            content = elem.get_text().strip()
            if content and len(content) > 15:  # 只保留长于15字的内容（避免垃圾数据）
                quotes.append({
                    "id": len(quotes) + 1,
                    "content": content,
                    "source": url,
                    "timestamp": datetime.now().strftime("%Y-%m-%d")
                })
    except Exception as e:
        print(f"爬取{url}出错：{e}")

# 生成题库示例数据（先手动加10道行测题，避免爬虫没爬到数据）
sample_questions = [
    {
        "id": 1,
        "questionType": "言语理解",
        "difficulty": "易",
        "content": "下列词语中，没有错别字的一项是？",
        "options": ["A. 迫不急待", "B. 川流不息", "C. 悬梁刺骨", "D. 滥芋充数"],
        "answer": "B",
        "analysis": "A选项应为“迫不及待”，C选项应为“悬梁刺股”，D选项应为“滥竽充数”。"
    },
    # 这里可以再复制9道类似题（换内容就行，id从2到10）
]
questions.extend(sample_questions)

# 保存数据到本地文件（后续同步到Firebase）
# 建data文件夹
import os
if not os.path.exists("./data"):
    os.makedirs("./data")

# 保存题库
with open("./data/questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

# 保存名言
with open("./data/quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, ensure_ascii=False, indent=2)

print("爬取完成！共获取题库：", len(questions), "道，名言：", len(quotes), "条")
