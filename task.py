import time

from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import target


def single_task(driver, url, wait):
    """
    传入URL，处理单个页面
    :param driver: driver
    :param url: 要处理的url
    :param wait: driver 等待
    :return: 结果 success or error
    """
    result = pre_handle(driver, url)
    if result['status'] == 'error':
        return result

    result1 = comment_for_later_call(wait)
    result2 = comment_for_immediate_call(wait)
    if result1['status'] == 'success' or result2['status'] == 'success':
        result = {'status': 'success'}
        return result

    return result2


def comment_for_immediate_call(wait):
    """
    电话回拨系统（实时攻击）
    :param wait: driver 等待
    :return: 结果 success or error
    """
    result = {'status': 'success'}
    try:
        phone_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "lxb-cb-input")))
        phone_input.send_keys(target['phone'])
        button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "lxb-cb-input-btn")))
        time.sleep(1)
        button.click()

    except Exception as e:
        result['message'] = e
        result['status'] = 'error'
    return result


def comment_for_later_call(wait):
    """
    留言系统实现（非实时攻击）
    :param wait: driver 等待
    :return:  结果 success or error
    """
    result = {'status': 'success'}
    try:
        textarea = wait.until(EC.visibility_of_element_located((By.ID, "nb-nodeboard-set-content-js")))
        textarea.send_keys(target['comment'])
        input_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'nb-nodeboard-input')))
        for text in input_list:
            placeholder = str(text.get_attribute('placeholder'))
            if '电话' in placeholder:
                text.send_keys(target['phone'])
            elif '姓' in placeholder:
                text.send_keys(target['name'])
            elif '邮' in placeholder:
                text.send_keys(target['email'])
            elif '地址' in placeholder:
                text.send_keys(target['address'])
            elif '必填' in placeholder:
                text.send_keys(target['phone'])
            time.sleep(0.5)
        button = wait.until(EC.presence_of_element_located((By.ID, 'nb_nodeboard_send')))
        button.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'nb_nodeboard_success')))

    except Exception as e:
        result['message'] = e
        result['status'] = 'error'

    return result


def pre_handle(driver, url):
    """
    预处理 404、502、页面不存在 等问题
    :param driver: driver
    :param url: url
    :return:  结果 success or error
    """
    result = {'status': 'success'}
    try:
        driver.get(url)
    except WebDriverException as e:
        if 'NotFound' in e.msg:
            result['message'] = Exception("404 Not Found")
            result['status'] = 'error'
            return result
        else:
            driver.execute_script("window.stop()")
    except Exception as e:
        result['message'] = e
        result['status'] = 'error'
        return result

    try:
        if driver.find_element_by_xpath("//*[contains(text(),'502')]") is not None:
            raise Exception("502 Bad GatWay")
    except NoSuchElementException as e:
        pass
    except Exception as e:
        result['message'] = e
        result['status'] = 'error'
        return result

    try:
        if driver.find_element_by_xpath("//*[contains(text(),'无法进行访问')]") is not None:
            raise Exception("502 Bad GatWay")
    except NoSuchElementException as e:
        pass
    except Exception as e:
        result['message'] = e
        result['status'] = 'error'
        return result

    try:
        if driver.find_element_by_xpath("//*[contains(text(),'无法访问')]") is not None:
            raise Exception("502 Bad GatWay")
    except NoSuchElementException as e:
        pass
    except Exception as e:
        result['message'] = e
        result['status'] = 'error'
        return result

    try:
        if driver.find_element_by_xpath("//*[contains(text(),'404 Not Found')]") is not None:
            raise Exception("404 Not Found")
    except NoSuchElementException as e:
        pass
    except Exception as e:
        result['message'] = e
        result['status'] = 'error'
        return result
    return result
