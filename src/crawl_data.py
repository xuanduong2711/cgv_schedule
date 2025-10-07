from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service


import os
import json
import time

#  Cấu hình Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu") 

# Chỉ định đường dẫn binary của Chrome for Testing (như đã cài trong Dockerfile.airflow)
options.binary_location = "/opt/chrome-for-testing/chrome-linux64/chrome"

# ----------------- THAY ĐỔI TẠI ĐÂY -----------------
# Chỉ định đường dẫn đến chromedriver đã cài đặt thủ công
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver" 

# Tạo Service bằng đường dẫn đã chỉ định
service = Service(CHROMEDRIVER_PATH)

# Khởi tạo driver với Service và Options đã cấu hình
# KHÔNG CÒN GỌI ChromeDriverManager().install() NỮA
driver = webdriver.Chrome(service=service, options=options)
# ----------------- KẾT THÚC THAY ĐỔI -----------------

# Truy cập web

link = 'https://www.cgv.vn/en/cinox/site/cgv-vivo-city'
driver.get(link)
wait = WebDriverWait(driver, 20)

def get_info_cinema(list_phim: list, date_list: list) -> list:
    for i in range(len(date_list)):
        try:
            date = date_list[i]
            
            driver.execute_script("arguments[0].scrollIntoView(true);", date)
            clickable_date = wait.until(EC.element_to_be_clickable((By.ID, date.get_attribute("id"))))
            clickable_date.click()
            time.sleep(2)
            phim_elements = driver.find_elements(By.XPATH, "//*[@class='film-list']")
            if len(phim_elements) == 0:
                break
            for sub_list in phim_elements:
                name = sub_list.find_element(By.XPATH, ".//*[@class='film-label']").text
                times = [t.text for t in sub_list.find_elements(By.XPATH, ".//*[@class='film-showtimes']")]
                
                title_cinema = sub_list.find_element(By.XPATH, "//*[@class='page-title theater-title']")
                list_phim.append({ "theater": title_cinema.text,  "name_movie": name, "date": date.text, "times": times})

        except:
            print('ERROR \n ')
    return list_phim



data_list = []
cinemas_list = []
urls = []  # chỉ lưu URL

cinemas_list= driver.find_elements(By.XPATH, "//*[contains(@id,'cgv_site_0')]")


for i in range(len(cinemas_list)):
    page = cinemas_list[i].get_attribute("onclick")
    urls.append(page.split("'")[1])



# Duyệt từng URL
for url in urls:
    driver.get(url)
    time.sleep(1.5)
    date_list = driver.find_elements(By.XPATH, "//*[contains(@id,'cgv20')]")
    data = get_info_cinema(list_phim=[], date_list=date_list)
    data_list.extend(data)

output_path = "/opt/airflow/data/cgv_movies.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

print(f"✅ Đang lưu dữ liệu vào {output_path}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=4) 
print(f"Dữ liệu data_list đã lưu thành công vào {output_path}")

driver.quit()