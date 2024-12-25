from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
from PIL import Image
from io import BytesIO

# 網頁分析
input_image = input("請輸入網址：")
response = requests.get(f"{input_image}")
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

# 開資料夾
img_dir = "img"
sticker_dir = "sticker"
os.makedirs(img_dir, exist_ok=True)
os.makedirs(sticker_dir, exist_ok=True)

download_urls = set()
img_count = 1
# 縮小圖片的目標寬度
target_width = 100

# 找到所有span ###這邊要看你網頁圖片的label跟class
spans = soup.find_all('span', class_='mdCMN09Image')

# 處理span
for index, span in enumerate(spans, start=1):
    if 'style' in span.attrs:
        style_content = span['style']
        # 抓URL
        start = style_content.find('url(') + len('url(')
        end = style_content.find(')', start)
        img_url = style_content[start:end]
        
        if img_url in download_urls:
            continue

        # 下載圖片
        response = requests.get(img_url)
        if response.status_code == 200:
            time = datetime.now().strftime("%m%d%H%M")
            img_path = os.path.join(img_dir, f"{time}_{img_count}.png")
            sticker_path = os.path.join(sticker_dir, f"{time}_{img_count}.png")
            with open(img_path, "wb") as file:
                file.write(response.content)

            # 圖片縮小
            image = Image.open(BytesIO(response.content))
            width, height = image.size
            new_height = int((target_width / width) * height)  # 等比例縮放
            resized_image = image.resize((target_width, new_height), Image.Resampling.LANCZOS)

            # 儲存縮小後的圖片
            resized_image.save(sticker_path)
            print(f"圖片已成功下載並儲存為 {img_path}")
            print(f"圖片已成功下載並縮小儲存為 {sticker_path}")
            download_urls.add(img_url)
            img_count += 1
        else:
            print("下載失敗")
    else:
        print("下載失敗")