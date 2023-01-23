# scrapy_crawler
A crawler to scrape news details. Advertisement news have been ignored intentionally.

## Installation Guide for Linux:

1. Install chromium if you don't have chromium already.  
   `sudo apt install chromium-browser`

2. Install the python packages. You may use a virtual environment to install the packages.
    `pip install -r requirements.txt`  

## Installation Guide for Windows.
1. Make sure Chrome is installed in your system. If not download and install it.  
2. Get your Chrome version by placing the below url in the browser url section.  
    `chrome://settings/help`  
 For me the version shows `Version 109.0.5414.75 (Official Build) (64-bit)`
3. Find your chrome driver from `https://chromedriver.chromium.org/downloads`. As my Chrome version is `109`, so I downloaded the 
ChromeDriver which version startswith `109`. 
4. Unzip the downloaded file and put the `chromedriver.exe` in the `scrapy_crawler/drivers` directory. Overwrite with new `chromedriver.exe` if needed.
5. Install the python packages. You may use a virtual environment to install the packages. 
    `pip install -r requirements.txt` 

