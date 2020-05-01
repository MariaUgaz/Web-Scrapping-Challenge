from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    html = browser.html
    news_bsoup = BeautifulSoup(html, 'html.parser')
    news_tit = news_bsoup.find_all('div', class_='content_title')[0].text
    news_pa = news_bsoup.find_all('div', class_='article_teaser_body')[0].text


    jplnasa_url = 'https://www.jpl.nasa.gov'
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    img_html = browser.html
    img_bsoup = BeautifulSoup(html, 'html.parser')
    relative_img_path = img_bsoup.find_all('img')[3]["src"]
    featured_img_url = jplnasa_url + relative_img_path

    wthr_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(wthr_url)
    wthr_html = browser.html
    wthr_bsoup = BeautifulSoup(wthr_html, 'html.parser')
    mars_wthr = wthr_bsoup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    fts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fts_url)
    fts_df = tables[2]
    fts_df.columns = ["Description", "Value"]
    marshtml_table = fts_df.to_html()
    marshtml_table.replace('\n', '')
    
    astro_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    astro_html = browser.html
    astro_bsoup = BeautifulSoup(hemispheres_html, 'html.parser')
    ahemispheres = astro_bsoup.find('div', class_='collapsible results')
    marshemi = ahemispheres.find_all('div', class_='item')
    hemi_img_urls = []

    for i in marshemi:
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text        
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(astro_url + hemisphere_link)        
        img_html = browser.html
        img_bsoup = BeautifulSoup(image_html, 'html.parser')        
        img_link = img_bsoup.find('div', class_='downloads')
        img_url = img_link.find('li').a['href']
        img_dict = {}
        img_dict['title'] = title
        img_dict['img_url'] = img_url        
        hemi_img_urls.append(img_dict)

    mars_dict = {
        "news_title": news_tit,
        "news_p": news_pa,
        "featured_image_url": featured_img_url,
        "mars_weather": mars_wthr,
        "fact_table": str(marshtml_table),
        "hemisphere_images": hemi_img_urls
    }

    return mars_dict