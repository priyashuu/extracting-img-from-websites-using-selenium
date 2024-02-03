from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from selenium import webdriver
import os
import urllib.request
import time


app = Flask(__name__)

# CREATE FOLDER
def folder_create(folder_name):
    try:
        # folder creation
        os.mkdir(folder_name)
    except FileExistsError:
        print("Folder Exist with that name!")

# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):
    # initial count is zero
    count = 0
    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images are not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag, fetch image Source URL
            try:
                # Search for "src" in img tag
                image_link = image["src"]
            except KeyError:
                pass

            # After getting Image Source URL
            try:
                # Image Download start
                urllib.request.urlretrieve(image_link, f"{folder_name}/images{i+1}.jpg")
                # counting number of image downloaded
                count += 1
            except:
                pass

        # There might be a possibility that not all images are downloaded
        if count == len(images):
            print("All Images Downloaded!")
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")

# CAPTURE SCREENSHOT OF THE WEBSITE
def capture_screenshot(url, folder_name):
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for the page to load (adjust this time based on your website's loading time)
    time.sleep(5)

    # Capture screenshot
    screenshot_path = os.path.join(folder_name, 'screenshot.png')
    driver.save_screenshot(screenshot_path)

    print(f"Screenshot captured: {screenshot_path}")

    # Close the browser
    driver.quit()

# MAIN FUNCTION START
# ...

def main(url):
    # Create a folder with the given name
    folder_name = input("Enter Folder Name:- ")
    folder_create(folder_name)

    # Download the page content
    with urllib.request.urlopen(url) as response:
        html_content = response.read()

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all images in the HTML
    images = soup.findAll('img')

    # Check if there are any CAPTCHA images
    captcha_images = [img for img in images if 'captcha' in str(img).lower()]

    if captcha_images:
        # Call download_images function for CAPTCHA images only
        download_images(captcha_images, folder_name)

        # Display the CAPTCHA images to the user
        display_captcha_images(folder_name)
    else:
        print("No CAPTCHA images found on the website.")
        download_images(images, folder_name)

    # Capture screenshot of the webpage
    capture_screenshot(url, folder_name)

# ...


# Display CAPTCHA images to the user
def display_captcha_images(folder_name):
    image_files = [f for f in os.listdir(folder_name) if f.endswith(".jpg")]

    print("CAPTCHA images:")
    for i, image_file in enumerate(image_files):
        print(f"{i+1}. {image_file}")

    # Ask the user to solve the CAPTCHA manually
    user_input = input("Enter the number of the CAPTCHA you solved: ")
    captcha_path = os.path.join(folder_name, image_files[int(user_input) - 1])

    # Here, you can proceed with the user-inputted CAPTCHA path or implement further processing

if __name__ == '__main__':
    # Take URL
    url = "https://www.flipkart.com/"
    # CALL MAIN FUNCTION
    main(url)
from google.cloud import vision
from google.cloud.vision_v1 import types
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_service_account_json_file.json'

def detect_image_labels(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rt') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]

image_descriptions = detect_image_labels('path_to_your_image.jpg')
print(image_descriptions)
import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

image_text = extract_text_from_image('path_to_your_image.jpg')
print(image_text)
