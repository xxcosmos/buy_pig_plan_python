from selenium import webdriver


target = {
    "phone": "13012345678",
    "name": "小明",
    "email": "xx@xx.xx",
    "address": "这个男人来自地球",
    "comment": "谢谢！不会～"
}

settings = {
    "times": 100,
    "timeout": 5,
    "driver":webdriver.Firefox(),
}