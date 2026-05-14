!pip install selenium beautifulsoup4 pandas chromedriver-autoinstaller -q

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import pandas as pd
import time

chromedriver_autoinstaller.install()

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

url = "https://www.inmotionhosting.com/shared-hosting"

driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

plans = soup.find_all("div", class_="plan-card")

data = []

for plan in plans:
    
    try:
        name = plan.find("h3").get_text(strip=True)
    except:
        name = "N/A"

    try:
        price = plan.find(class_="price").get_text(strip=True)
    except:
        price = "N/A"

    features = []

    try:
        feature_list = plan.find_all("li")

        for feature in feature_list:
            features.append(feature.get_text(strip=True))
    except:
        pass

    data.append({
        "Plan Name": name,
        "Price": price,
        "Features": ", ".join(features)
    })

df = pd.DataFrame(data)

print(df)

df.to_csv("hosting_plans.csv", index=False)

print("CSV saved successfully!")

driver.quit()


