from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import pandas as pd

company = []
job = []
salary = []
loc = []
desc = []
size = []
type = []
sector = []
industry = []
founded = []
revenue = []

def scrape_job_details(driver):
    try:
        star = driver.find_element(By.XPATH, "//span[@class='css-1m5m32b e1tk4kwz2']").text
        comp_name = driver.find_element(By.XPATH, "//div[@class='css-87uc0g e1tk4kwz1']").text
        company.append(comp_name.replace(star, ""))
    except:
        company.append("#N/A")

    try:
        # scrapping title name
        job.append(driver.find_element(By.XPATH, "//div[@class='css-1vg6q84 e1tk4kwz4']").text)
    except:
        job.append("#N/A")

    try:
        # scrapping location
        loc.append(driver.find_element(By.XPATH, "//div[@class='css-56kyx5 e1tk4kwz5']").text)
    except:
        loc.append("#N/A")

    try:
        # scrapping job description
        desc.append(driver.find_element(By.XPATH, "//div[@id='JobDescriptionContainer']").text)
    except:
        desc.append("#N/A")

    try:
        # scrapping salary estimate
        salary.append(driver.find_element(By.XPATH, "//div[@class='css-1bluz6i e2u4hf13']").text)
    except:
        salary.append("#N/A")

    try:
        # scrapping company_size
        size_elem = driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*")
        size.append(size_elem.text)
    except:
        size.append("#N/A")

    try:
        # scrapping company_type
        type_elem = driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*")
        type.append(type_elem.text)
    except:
        type.append("#N/A")

    try:
        # scrapping company sector
        sector_elem = driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*")
        sector.append(sector_elem.text)
    except:
        sector.append("#N/A")

    try:
        # scrapping company's industry 
        industry_elem = driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*")
        industry.append(industry_elem.text)
    except:
        industry.append("#N/A")

    try:
        # scrapping when company is founded
        founded_elem = driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*")
        founded.append(founded_elem.text)
    except:
        founded.append("#N/A")

    try:
        # scrapping company revenue
        revenue_elem = driver.find_element(By.XPATH, "//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*")
        revenue.append(revenue_elem.text)
    except:
        revenue.append("#N/A")

def scrape(driver, num_pages):
    current_page = 1
    time.sleep(3)

    while current_page <= num_pages:
        job_cards = driver.find_elements(By.XPATH, "//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")

        for card in job_cards:
            print(f"Page {current_page}")
            card.click()
            time.sleep(3)
            card.location_once_scrolled_into_view

            # Ignore the sign-in screen
            try:
                driver.find_element(By.XPATH, ".//button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']").click()
                time.sleep(2)
            except NoSuchElementException:
                time.sleep(2)
                pass

            time.sleep(3)

            # Expand job card and scroll down
            try:
                show_more = driver.find_element(By.XPATH, "//div[@class='p-std css-1k5huso e856ufb0']")
                show_more.location_once_scrolled_into_view
            except:
                continue

            time.sleep(2)

            # Click "Show more" button
            driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb4']").click()
            time.sleep(2)

            # Scrape job details
            scrape_job_details(driver)

        print(f"Page {current_page} done")

        # Go to the next page
        try:
            next_button = driver.find_element(By.XPATH, "//span[@alt='next-icon']")
            next_button.click()
            current_page += 1
            time.sleep(4)
        except NoSuchElementException:
            break

    driver.close()

    # Create a DataFrame from the scraped data
    df = pd.DataFrame({
        'company': company,
        'job title': job,
        'location': loc,
        'job description': desc,
        'salary estimate': salary,
        'company size': size,
        'company type': type,
        'company sector': sector,
        'company industry': industry,
        'company founded': founded,
        'company revenue': revenue
    })

    # Print the DataFrame
    print(df)

    return df

if __name__ == "__main__":
    keyword = 'machine learning engineer'  # Title of the job to scrape

    # Set up Chrome options and driver
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver_path = 'C:/Users/salmanoglu.LAPTOP-H6N6LQ5C/Desktop/tt_project/chromedriver.exe'
    driver = webdriver.Chrome(options=options, executable_path=driver_path)

    # URL of the website to scrape
    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'

    driver.get(url)
    time.sleep(2)

    num_pages = 5  # Total number of pages to scrape

    df = scrape(driver, num_pages)

    # Save the DataFrame as a CSV file
    df.to_csv(keyword + '.csv')