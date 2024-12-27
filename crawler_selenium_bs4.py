from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup

"""
    python2 executable
    导出 荷兰 的电价
    地区可以手动，时间自动就可以啦
"""


# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 运行时无界面

# 设置ChromeDriver路径
service = Service('E:\chromedriver-win64\chromedriver.exe')  # 替换为您的chromedriver路径

# 初始化WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 打开目标网页
    driver.get('https://newtransparency.entsoe.eu/market/energyPrices?appState=%7B%22sa%22%3A%5B%22BZN%7C10YNL----------L%22%5D%2C%22st%22%3A%22BZN%22%2C%22mm%22%3Atrue%2C%22ma%22%3Afalse%2C%22sp%22%3A%22HALF%22%2C%22dt%22%3A%22TABLE%22%2C%22df%22%3A%222024-12-25%22%2C%22tz%22%3A%22CET%22%7D')

    # 等待页面加载完成（这里简单地等待几秒）
    time.sleep(60)
    # 获取页面源代码
    page_source = driver.page_source

    # 使用BeautifulSoup解析页面源代码
    soup = BeautifulSoup(page_source, 'html.parser')
    print(soup.prettify(), type(soup.prettify()))

    # 创建一个空列表用于存储结果
    data = []

    # 查找所有的<tr>标签
    rows = soup.find_all('tr', class_='uutileselements-1obf64m')

    # 如果没有<tr>标签，则可能是顶层数据，直接查找
    if not rows:
        print("没有行数据", rows)
        time_range_element = soup.find('span', class_='usytpelementsg-1xekhk3')
        price_element = soup.find('span', class_='usytpelementsg-1wowaen')

        if time_range_element and price_element:
            data.append({
                'time_range': time_range_element.text.strip(),
                'price': price_element.text.strip()
            })
    else:
        # 遍历每一个<tr>标签
        for row in rows:
            # 提取时间范围
            time_range_element = row.find('span', class_='usytpelementsg-1xekhk3')
            time_range = time_range_element.text.strip() if time_range_element else None

            # 提取电价
            price_element = row.find('span', class_='usytpelementsg-1wowaen')
            price = price_element.text.strip() if price_element else None

            # 将提取的数据添加到列表中
            if time_range and price:
                data.append({
                    'time_range': time_range,
                    'price': price
                })

    # 输出结果
    for item in data:
        print(f"时间范围: {item['time_range']}, 电价: {item['price']} 欧元/MWh")

finally:
    # 关闭浏览器
    driver.quit()