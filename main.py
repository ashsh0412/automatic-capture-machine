import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def create_download_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def download_images(keyword, num_images=6):
    options = Options()
    options.add_argument(
        "--headless"
    )  # Uncomment this line to run Chrome in headless mode (without a visible browser window)
    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Searching the given keyword
        driver.get("https://www.google.com/imghp")
        search_box = driver.find_element(By.XPATH, "//input[@name='q']")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # Step 2: Go to the image and download 6 pics
        image_links = driver.find_elements(
            By.XPATH, "//a[@class='wXeWr islib nfEiy mM5pbd']"
        )
        for i, image_link in enumerate(image_links[:num_images]):
            image_link.click()
            time.sleep(1)

            # Step 3: Make a folder and save the downloaded pics
            create_download_folder("downloaded_images")
            image_url = driver.find_element(By.XPATH, "//img[@class='n3VNCb']")
            src_url = image_url.get_attribute("src")
            image_name = f"downloaded_images/{keyword}_image_{i + 1}.jpg"

            with open(image_name, "wb") as f:
                f.write(requests.get(src_url).content)

            print(f"Image {i + 1} downloaded and saved.")

        print("Download process completed!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    keyword_to_search = (
        "your_keyword_here"  # Replace with the keyword you want to search for
    )
    download_images(keyword_to_search, num_images=6)
