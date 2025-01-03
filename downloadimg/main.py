from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
from PIL import Image
#from resize import resize

def resize():
    f_path = './img'
    sticker_dir = "sticker"
    os.makedirs(sticker_dir, exist_ok=True)

    # 目標大小
    target_width = 130  

    # 遍歷資料夾中的所有圖片
    for fname in os.listdir(f_path):
        if fname.endswith(('.png')):  # 判斷檔案是否是圖片
            img_path = os.path.join(f_path, fname)
            sticker_path = os.path.join(sticker_dir, fname)
            
            # 開啟圖片
            with Image.open(img_path) as img:
                # 縮小圖片
                width, height = img.size
                new_height = int((target_width / width) * height)  # 等比例縮放
                resized_image = img.resize((target_width, new_height), Image.Resampling.LANCZOS)

                # 儲存縮小後的圖片
                resized_image.save(sticker_path)
    print("已縮小所有圖片並儲存")

def downloadimg():
    # 網頁分析
    input_image = input("請輸入網址：")
    response = requests.get(f"{input_image}")
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # 開資料夾
    output_dir = "img"
    os.makedirs(output_dir, exist_ok=True)

    download_urls = set()
    img_count = 1

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
                img_path = os.path.join(output_dir, f"{time}_{img_count}.png")
                with open(img_path, "wb") as file:
                    file.write(response.content)
                print(f"圖片已成功下載並儲存為 {img_path}")
                download_urls.add(img_url)
                img_count += 1
            else:
                print("下載失敗")
        else:
            print("下載失敗")

downloadimg()
resize()