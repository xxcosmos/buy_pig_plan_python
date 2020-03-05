import json
import random
import time
import os

from selenium.webdriver.support.wait import WebDriverWait
from config import settings
from task import single_task


def main():
    """
    程序主函数
    :return: None
    """
    driver = setup_driver()
    wait = WebDriverWait(driver, settings['timeout'])

    url_list = get_url_list()
    count_result = {'success': 0, 'error': 0, 'sum': settings['times']}

    for i in range(settings['times']):
        url = url_list[random.randint(0, len(url_list) - 1)]

        print(f'--------------TASK {i + 1}: {url["name"]} {url["url"]} --------------')
        result = single_task(driver, url['url'], wait)
        print(result)

        count_result[result['status']] += 1
        if result['status'] == 'success':
            time.sleep(2)

    print(f'\n{count_result}')
    driver.close()


def setup_driver():
    """
    初始化 driver
    :return: driver
    """
    driver = settings['driver']
    driver.set_page_load_timeout(settings['timeout'])
    driver.set_script_timeout(settings['timeout'])
    driver.set_window_rect(0, 0, 1024, 768)
    return driver


def get_url_list():
    """
    随机选择一个 json 文件读入
    :return: dict 数组，URL 列表
    """
    file_list = os.listdir('assets')
    filepath = os.path.join('assets', file_list[random.randint(0, len(file_list) - 1)])
    with open(filepath) as f:
        url_list = json.load(f)
    return url_list


if __name__ == '__main__':
    main()
