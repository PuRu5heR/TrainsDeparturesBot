from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
from threading import Thread


class Parser:
    def __init__(self, departure_country, departure_city, arrival_country, date_from,
                 date_to, nights_count_from, nights_count_to, adults, children, stars):
        self.departure_country = departure_country
        self.departure_city = departure_city  # город вылета
        self.arrival_county = arrival_country  # страна
        self.date_from = date_from  # дата
        self.date_to = date_to  # вылета
        self.nights_count_from = nights_count_from  # количество
        self.nights_count_to = nights_count_to  # ночей
        self.adults = adults  # количество взрослых
        self.children = children.split(", ")  # дети [возраст, возраст...]
        self.stars = stars
        self.url = "https://tourvisor.ru/"  # ссылка на сайт

    def choosing_departure(self, driver):
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "TVMainSelect.TVAxisDirection-Column.TVStyleTheme2.TVTextAlign-Left").click()
        countries = driver.find_elements(By.CLASS_NAME, "TVNationContainer")
        for country in countries:
            if country.text == self.departure_country:
                country.click()
                break

        time.sleep(1)
        cities = driver.find_elements(By.CLASS_NAME, "TVCheckBox")
        for city in cities:
            if city.text == self.departure_city:
                city.click()
                break

    def choosing_arrival(self, driver):
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/div/div/div/div/div[2]/div/div").click()
        for i in driver.find_elements(By.CLASS_NAME, "TVTabListItem"):
            if i.text == "Все":
                i.click()
        countries = driver.find_elements(By.CLASS_NAME, "TVComplexListItemContent")
        time.sleep(1)
        for country in countries:
            if country.text == self.arrival_county:
                country.click()
                break

    def choosing_datefrom(self, driver):
        global month_now
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/div/div/div/div/div[3]/div/div").click()
        time.sleep(1)
        months = ["ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ", "МАЙ", "ИЮНЬ", "ИЮЛЬ", "АВГУСТ", "СЕНТЯБРЬ", "ОКТЯБРЬ",
                  "НОЯБРЬ", "ДЕКАБРЬ"]
        date_from = self.date_from.split(".")
        month_now_text = driver.find_element(By.CLASS_NAME, "TVCalendarTitleControlMonth").text
        for i in range(0, 12):
            if month_now_text == months[i]:
                month_now = i + 1
                break
        year_now = driver.find_element(By.CLASS_NAME, "TVCalendarTitleControlYear").text
        if int(year_now) < int(date_from[2]):
            diff = abs(int(date_from[2]) - int(year_now))
            for i in range(0, diff):
                for j in range(0, 12):
                    driver.find_element(By.CLASS_NAME, "TVCalendarSliderViewRightButton").click()
            for i in range(0, month_now - 1):
                driver.find_element(By.CLASS_NAME, "TVCalendarSliderViewLeftButton").click()
            month_now = 1
        for i in range(0, int(date_from[1]) - month_now):
            driver.find_element(By.CLASS_NAME, "TVCalendarSliderViewRightButton").click()

        time.sleep(1)
        stop = False
        for i in range(1, 7):
            if stop:
                break
            for j in range(1, 8):
                try:
                    day = driver.find_element(By.XPATH,
                                              "/html/body/div[11]/div[1]/div/div/div[3]/div[1]/div[2]/div/t-table/t-tbody/t-tr[" +
                                              str(i) + "]/t-td[" + str(j) + "]")
                    if day.get_attribute('data-value') == date_from[0]:
                        day.click()
                        stop = True
                        break
                except StaleElementReferenceException:
                    pass

    def choosing_dateto(self, driver):
        date_to = self.date_to.split(".")
        date_from = self.date_from.split(".")
        year_now = driver.find_element(By.CLASS_NAME, "TVCalendarTitleControlYear").text
        if int(year_now) < int(date_to[2]):
            month_current = int(date_from[1])
            diff = abs(int(date_to[2]) - int(year_now))
            for i in range(0, diff):
                for j in range(0, 12):
                    driver.find_element(By.CLASS_NAME, "TVCalendarSliderViewRightButton").click()
            for i in range(0, month_current - 1):
                driver.find_element(By.CLASS_NAME, "TVCalendarSliderViewLeftButton").click()
        else:
            for i in range(0, int(date_to[1]) - int(date_from[1])):
                driver.find_element(By.CLASS_NAME, "TVCalendarSliderViewRightButton").click()
        time.sleep(1)
        stop = False
        for i in range(1, 7):
            if stop:
                break
            for j in range(1, 8):
                try:
                    day = driver.find_element(By.XPATH,
                                              "/html/body/div[11]/div[1]/div/div/div[3]/div[1]/div[2]/div/t-table/t-tbody/t-tr[" + str(
                                                  i) + "]/t-td[" + str(j) + "]")
                    if day.get_attribute('data-value') == date_to[0]:
                        ActionChains(driver).move_to_element(day).perform()
                        day.click()
                        stop = True
                        break
                except StaleElementReferenceException:
                    pass

    def choosing_nights_count_from(self, driver):
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/div/div/div/div/div[4]/div/div").click()
        nights = driver.find_elements(By.CLASS_NAME, "TVRangeTableCell")
        for night in nights:
            if night.find_element(By.CLASS_NAME, "TVRangeCellLabel").text == self.nights_count_from:
                night.click()
                break

    def choosing_nights_count_to(self, driver):
        time.sleep(1)
        nights = driver.find_elements(By.CLASS_NAME, "TVRangeTableCell")
        for night in nights:
            if night.find_element(By.CLASS_NAME, "TVRangeCellLabel").text == self.nights_count_to:
                ActionChains(driver).move_to_element(night).perform()
                night.click()
                break

    def choosing_adults_count(self, driver):
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/div/div/div/div/div[5]/div/div").click()
        adults_now = driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/div[2]/div[1]/div/div[2]").text.strip()
        if self.adults == "1":
            driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/div[2]/div[1]/div/div[1]").click()
        elif int(self.adults) > int(adults_now):
            diff = int(self.adults) - int(adults_now)
            for i in range(0, diff):
                driver.find_element(By.XPATH, "/html/body/div[11]/div[1]/div[2]/div[1]/div/div[3]").click()

    def choosing_children(self, driver):
        time.sleep(1)
        for i in range(0, len(self.children)):
            driver.find_element(By.CLASS_NAME, "TVTouristElement.TVTouristButton").click()
            ages = driver.find_elements(By.CLASS_NAME, "TVSelectChildAgeItem.TVButtonHover")
            if int(self.children[i]) < 2:
                driver.find_element(By.CLASS_NAME,
                                    "TVSelectChildAgeItem.TVButtonHover").click()
                continue
            for age in ages:
                if age.find_element(By.CLASS_NAME, "TVSelectChildAgeValue").text == self.children[i]:
                    age.click()

    def pick_stars(self, driver):
        picking = driver.find_elements(By.CLASS_NAME, "TVStarsSelectItem.TVSize-S")
        for i in range(len(picking)):
            if i == int(self.stars) - 1:
                ActionChains(driver).move_to_element(picking[i]).perform()
                picking[i].click()
                break

    def parsing(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        if not self.departure_country == "" and not self.departure_city == "":
            self.choosing_departure(driver)
        if not self.arrival_county == "":
            self.choosing_arrival(driver)
        if not self.date_from == "":
            self.choosing_datefrom(driver)
        if not self.date_to == "":
            self.choosing_dateto(driver)
        if not self.nights_count_from == "":
            self.choosing_nights_count_from(driver)
        if not self.nights_count_to == "":
            self.choosing_nights_count_to(driver)
        if not self.adults == "":
            self.choosing_adults_count(driver)
        if not self.children == [""]:
            self.choosing_children(driver)
        driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/div/div/div/div/div[6]").click()
        time.sleep(2)
        if not self.stars == "":
            self.pick_stars(driver)
            driver.find_element(By.CLASS_NAME, "TVSearchButton.TVButtonColor.TVButtonHover").click()

        time.sleep(5)
        hotels = driver.find_elements(By.CLASS_NAME, "blpricesort")
        hotel_texts = []
        for hotel in hotels:
            try:
                href = hotel.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = hotel.find_element(By.CLASS_NAME, "TVResultItemDescription.TVLineClampEnabled.TVLineClamp-M").text
                name = hotel.find_element(By.TAG_NAME, "a").text
                location = hotel.find_element(By.CLASS_NAME, "TVResultItemSubTitle").text
                hotel_text = name + "\n\n" + location + "\n\n" + description + "\n\n" + href
                hotel_texts.append(hotel_text)
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass

        driver.close()
        return hotel_texts


if __name__ == "__main__":
    thread_list = []

    parser = Parser("Беларусь", "Минск", "Турция", "10.07.2022", "30.07.2022", "7", "14", "2", "8", "5")
    thread1 = Thread(target=parser.parsing())
    thread2 = Thread(target=parser.parsing())
    thread_list[0].start()
    thread_list[1].start()
