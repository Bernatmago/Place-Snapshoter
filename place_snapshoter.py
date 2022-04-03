import time
from datetime import datetime

import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

place_url = "https://www.reddit.com/r/place/"
canvas_tag = "mona-lisa-canvas"

place_size_px = 2000

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(options=chrome_options)
driver.get(place_url)
driver.maximize_window()

try:
    place_frame = WebDriverWait(driver, 5) \
        .until(EC.presence_of_element_located((By.XPATH, "//iframe[@src='https://hot-potato.reddit.com/embed']")))
    driver.switch_to.frame(place_frame)
    # time.sleep(5)

    canvas = driver.find_element(By.TAG_NAME, "mona-lisa-embed").shadow_root.\
        find_element(By.TAG_NAME, "mona-lisa-canvas").shadow_root.find_element(By.TAG_NAME, "canvas")

    button = driver.find_element(By.TAG_NAME, "mona-lisa-embed").shadow_root.\
        find_element(By.TAG_NAME, "mona-lisa-status-pill")

    ActionChains(driver).move_to_element(button).click().perform()
    time.sleep(2)  # Don't judge me thanks
    ActionChains(driver).move_by_offset(200, 200).click().perform()

    script = f"""
        const canvas = document.querySelector('mona-lisa-embed').shadowRoot
                                .querySelector('mona-lisa-canvas').shadowRoot
                                .querySelector('canvas')
        const context = canvas.getContext('2d')
        return context.getImageData(0, 0, {place_size_px}, {place_size_px})
        """

    for n in range(3):
        img_data = driver.execute_script(script)

        img = np.array(img_data["data"])
        img = img.reshape(place_size_px, place_size_px, 4).astype(np.uint8)

        filename = f"place_snapshot_{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.png"
        Image.fromarray(img).save(filename)
        print(f"saved {filename}")
        time.sleep(20)

except (TimeoutException, NoSuchElementException) as e:
    print(e)
finally:
    driver.close()
