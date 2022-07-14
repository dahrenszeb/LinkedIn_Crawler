import urllib.request as req
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import login_details


username = login_details.username
password = login_details.password


options = Options()
#options.add_argument('-headless')
driver = webdriver.Chrome(options=options)

driver.get("https://www.linkedin.com/uas/login?")
driver.maximize_window()

driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.XPATH,"//*[@id=\"organic-div\"]/form/div[3]/button").click()

driver.get("https://www.linkedin.com/in/michaelclijdesdale/")

page_soup = soup(driver.page_source, "html.parser")


work_exp = page_soup.find("div", {"class": "pvs-list__outer-container"}).findAll("li", {"class": "artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column"})

#del work_exp[0]  # does not contain working experience

# name the output file to write to local disk
out_filename = "work_exp.csv"
# header of csv file to be written
headers = "company, position \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

i = 1
for station in work_exp:
    company = station.find("span", {"class": "t-14 t-normal"}).find("span", {"class": "visually-hidden"}).text

    print("Company" + str(i) + ":" + company)
    position = station.find("span", {"class": "mr1 t-bold"}).find("span", {"class": "visually-hidden"}).text
    print("Position" + str(i) + ":" + position)
    i = i + 1

    # writes the dataset to file
    f.write(company.replace(",", "|") + ", " + position.replace(",", "|") + "\n")

f.close()
driver.quit()

