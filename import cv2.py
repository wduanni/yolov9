import cv2
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor

def load_image(image_path):
    return cv2.imread(image_path)

def create_video_from_images(image_folder, output_video_path, frame_repeat=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")][10:]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width,height))

    with ThreadPoolExecutor(max_workers=4) as executor:
        for image in tqdm(images):
            img_path = os.path.join(image_folder, image)
            img_future = executor.submit(load_image, img_path)
            video.write(img_future.result())

    cv2.destroyAllWindows()
    video.release()

# 使用示例
image_folder = r'C:\Users\WDN\Desktop\file\code\PY\yolov5\data\industry\val\images'
output_video_path = r'C:\Users\WDN\Desktop\file\code\PY\yolov5\data\industry\val\video.mp4'
create_video_from_images(image_folder, output_video_path, frame_repeat=30)