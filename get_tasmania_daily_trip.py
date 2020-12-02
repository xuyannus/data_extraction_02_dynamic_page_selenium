import time
import lxml.html
import pandas as pd
from selenium import webdriver

WEB_DRIVER_PATH = "/Users/yanxu/opt/chromium-browser/chromedriver"


def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36")
    options.add_argument('--headless')   # comment it for debug UI
    return options


def remove_special_chars(something):
    return "".join(something.split())


def close_ads(driver):
    # close the ad if existing
    try:
        time.sleep(3)   # wait for the ad to show up
        driver.switch_to.frame(frame_reference=driver.find_element_by_xpath("//iframe[@title='Modal Message']"))
        ad_element = driver.find_element_by_xpath("//span[@class='ab-close-button ab-html-close-button']")
        ad_element.click()
        time.sleep(2)    # wait for the click to happen
    except Exception:
        print("did not find the ad close button.")


def click_more_activities(driver):
    click_max = 100
    for index in range(click_max):
        try:
            button = driver.find_element_by_xpath("//button[@class='load-more__button gtm-trigger__search-results-show-more-btn btn btn-cta']")
            driver.execute_script('arguments[0].scrollIntoView();', button)
            time.sleep(3)   # wait for the window to scroll to button
            print(f"CONTINUE: click button for more activities: {index}")
            button.click()
            time.sleep(3)   # wait for the click to happen
        except Exception:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            print("STOP: no more activities")
            time.sleep(3)    # wait for the window to scroll to the bottom
            break


def extract_daily_trip(url, default_wait_sec=5):
    try:
        driver = webdriver.Chrome(WEB_DRIVER_PATH, chrome_options=get_chrome_options())
        driver.maximize_window()
        driver.get(url)
        time.sleep(default_wait_sec) # need to wait a while for the JS to run

        close_ads(driver)
        click_more_activities(driver)
        time.sleep(default_wait_sec)

        root = lxml.html.fromstring(driver.page_source)
        activities = root.xpath("//div[@class='activity-card__details']")
        print("len(activities):", len(activities))

        activity_list = []
        for activity in activities:
            title = activity.xpath(".//h2[@class='activity-card__title']/text()")
            title = "unspecified" if title is None or len(title) == 0 else title[0].strip()
            price = activity.xpath(".//p[@class='baseline-pricing__value']/text()")
            price = "unspecified" if price is None or len(price) == 0 else remove_special_chars(price[0])
            rate = activity.xpath(".//span[@class='rating-overall__rating-number']/text()")
            rate = "unspecified" if rate is None or len(rate) == 0 else remove_special_chars(rate[0])
            duration = activity.xpath(".//span[contains(text(), 'Duration')]/text()")
            duration = "unspecified" if duration is None or len(duration) == 0 else remove_special_chars(duration[0])

            activity_list.append({
                "title": title.replace(",", ""),
                "price": price.replace(",", ""),
                "rate": rate.replace(",", ""),
                "duration": duration.replace(",", ""),
            })

        activity_df = pd.DataFrame(activity_list)
        activity_df.to_csv("./tasmania_daily_trips.csv", index=False)
    except Exception as e:
        print(e)
    finally:
        if driver:
            driver.close()


if __name__ == "__main__":
    extract_daily_trip(url="https://www.getyourguide.co.uk/discovery/s?q=Tasmania&lc=l209&ct=172&searchSource=4&utm_force=0")