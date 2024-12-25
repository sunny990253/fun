from PIL import Image
import os

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
