from selenium import webdriver
import os
from urllib.request import urlopen
import matplotlib.pyplot as plt
import platform
import time

class Dec:
    """
    카드 클래스
    
    Args:
        card_name(str): 카드 이름
        image_path(str): 아이콘 위치(path)
        card_mana(int_or_float) : 카드 마나량, default 0
        card_damage(int_or_float) : default 0, 카드 데미지
        card_health(int_or_float) : 카드 힐량, default 0
        description(str): 카드 설명, default None
    """
    def __init__(self, card_name, image_path, 
                 card_mana=0, card_damage=0, card_health=0,
                 description=None):
        self._card_name = card_name
        self._description = description
        self._card_mana = card_mana
        self._card_damage = card_damage
        self._card_health = card_health
        
        self._artwork = self._card_generator(card_name, image_path, 
                 card_mana, card_damage, card_health,
                 description)
        
        
        
    @property
    def card_name(self):
        return self._card_name
    @property
    def description(self):
        return self._description
    @property
    def artwork(self):
        return self._artwork
    @property
    def card_mana(self):
        return self._card_mana
    @property
    def card_damage(self):
        return self._card_damage
    @property
    def card_health(self):
        return self._card_health
    
    def _card_generator(self, card_name, image_path, card_mana, card_damage, card_health, description):
        image_url = None
        try:
            if platform.system() == 'Darwin':
                DRIVER_PATH = os.path.join(os.getcwd(), '../driver/chromedriver')
            elif platform.system() == 'Windows':
                DRIVER_PATH = os.path.join(os.getcwd(), '../driver/chromedriver.exe')
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")

            driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
            # 일반적으로 다 로드 될때까지 3초정도 기다려줍니다
            driver.implicitly_wait(3)
            # url 접근
            driver.get('http://www.hearthcards.net')
            # 이름
            driver.find_element_by_xpath('//*[@id="panel_left_cardname_race"]/div/input[1]').send_keys(card_name)
            # 능력치
            driver.find_element_by_xpath('//*[@id="panel_left_mana"]/div/input[1]').send_keys(card_mana)
            driver.find_element_by_xpath('//*[@id="panel_left_mana"]/div/input[2]').send_keys(card_damage)
            driver.find_element_by_xpath('//*[@id="panel_left_mana"]/div/input[3]').send_keys(card_health)
            # 설명
            driver.find_element_by_xpath('//*[@id="input-area"]').send_keys(description)
            # 그림
            driver.find_element_by_xpath('//*[@id="file"]').send_keys(image_path)
            # submit
            driver.find_element_by_xpath('//*[@id="next"]').click()
            driver.implicitly_wait(3)
            time.sleep(1)
            image_url = driver.find_element_by_xpath('//*[@id="container"]/div[13]/p[2]/a').get_attribute('href')
        finally:
            driver.close()
        
        return image_url
    
    def display(self):
        """
        카드의 사진정보를 보여준다
        """
        f = urlopen(self.artwork)
        plt.figure(figsize=(5, 10))
        plt.axis('off')
        image = plt.imread(f)
        plt.imshow(image)
        plt.show()

