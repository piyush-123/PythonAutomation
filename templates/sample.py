from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from selenium import webdriver

app = Flask(__name__)


@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/analyse',methods=['POST','GET'])
@cross_origin()
def analyse_link():
    if request.method == 'POST':
        try:
            searchUrl = request.form['youtubelink'].replace(" ","")
            Driver = 'chromedriver.exe'
            image_urls = []
            title_names = []
            title_url = []
            likes_result = []
            comments_count = []
            commenter=[]
            commenter_desc=[]
            final_comments_name = []
            final_comments_desc = []


            wd = webdriver.Chrome(executable_path=Driver)
            wd.get(searchUrl)
            time.sleep(1)
            thumbnail_results = wd.find_elements("xpath", "//*[@id='items']/ytd-grid-video-renderer/div[1]/ytd-thumbnail/a/yt-img-shadow/img")



            for img in thumbnail_results:
                   image_urls.append(img.get_attribute('src'))


            title_results = wd.find_elements("xpath", "//*[@id='video-title']")

            for img in title_results:
                   title_names.append(img.get_attribute('title'))
                   title_url.append(img.get_attribute('href'))
            wait = WebDriverWait(wd, 15)
            for i in title_url:
                wd.get(i)
                wd.maximize_window()
                wd.execute_script("window.focus();")
                likes_result.append(wait.until(EC.presence_of_element_located((By.XPATH,
                                           "//*[@id='top-level-buttons-computed']/ytd-toggle-button-renderer/a/yt-formatted-string"))).text)

                wd.execute_script("window.scrollBy(0, 500)"," ")
                #wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(1)
                comments_count.append(wait.until(EC.presence_of_element_located((By.XPATH,
                                            "//*[@id='count']/yt-formatted-string/span[1]"))).text)
                comments_name = wd.find_elements("xpath", "//*[@id='author-text']/span")
                for k in comments_name:
                    commenter.append(k.text)
                comments_desc = wd.find_elements("xpath", "//*[@id='content-text']/span")
                for k in comments_desc:
                    commenter_desc.append(k.text)
                final_comments_name.append(commenter)
                final_comments_desc.append(commenter_desc)
                commenter = []
                commenter_desc = []







            return str(image_urls)
        except Exception as e:
            print(e)
            return "error"


if __name__ == '__main__':
    app.run()

