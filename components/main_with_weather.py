# ... main.py class version
# ---------------------------
# insert this code
def weatherSetting (self, width):
        base_url = 'http://www.weather.go.kr/weather/forecast/timeseries.jsp'
        #base_url = 'https://pjt3591oo.github.io/' 테스트용 url

        self.driver.get(base_url)
        self.driver.implicitly_wait(15)
        time.sleep(3)
        html = self.driver.page_source
        self.driver.implicitly_wait(15)

        soup = BeautifulSoup(html, 'html.parser')

        while True :
            selected_selector = self.driver.find_element_by_css_selector('body div.body-wrapper div div.width2 div div.distibution_search6 dl dd span.text')
            if width in selected_selector.text.strip() :
                self.source1.config(text = selected_selector.text.strip())
                print("동작")
                break

        state = True
        while state :
            try :
                ss = self.driver.find_elements_by_css_selector('body div.body-wrapper div div.width2 div div div.local_forecast_inn div.now_weather1 dd.now_weather1_center')
                state = False
                print("{0}, {1}, {2}", ss[0].text, ss[1].text, ss[2].text)
                self.weather_frame1.config(text = ss[0].text.strip())
                self.weather_frame2.config(text = ss[1].text.strip())
                self.weather_frame3.config(text = ss[2].text.strip())
            except :
                print("state8 error")

        while state :
            try :
                ss = driver.find_elements_by_css_selector('body div.body-wrapper div div.width2 div div div.local_forecast_inn div.time_weather1 img.png24')
                src = ss[0].get_attribute('alt')
                self.weather_frame4.config(text = src)
                state = False
            except :
                print("state8 error")

        self.driver.quit()
# ----------------------------------
# ...

# way to defind this code in MainThread
    def MainThread (self):
        while True:
            # ...
            self.weatherSetting('대구광역시')
            # ...
