from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import io
import requests
from PIL import Image
import pytesseract
import time

# required to have chromedriver.exe appropriate for you chrome version at "C:/chromedriver/"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # Set the tesseract path in the script

def solve_captcha():
    driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe')

    driver.get('https://www.amazon.com/errors/validateCaptcha')     # opens chrome browser with the given link
    
    images = driver.find_elements_by_tag_name('img')                # finds the image element
    src = images[0].get_attribute('src')                            # extracts image link from image element

    img_resp = requests.get(src)                                    
    img = Image.open(io.BytesIO(img_resp.content))                  # opens image in local memory

    solution = pytesseract.image_to_string(img)                     # Returns output as string from Tesseract OCR processing               
    captcha_box = driver.find_element_by_id("captchacharacters")    # finds element to type the captcha solution
    captcha_box.send_keys(solution)                                 # sends captcha solution to form
    driver.find_element_by_class_name("a-button-text").click()      # clicks submit button

    time.sleep(30)
    driver.close()

solve_captcha()