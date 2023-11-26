from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import re
from bs4 import BeautifulSoup
import openai
import os
from openai import OpenAI
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/asin', methods=['POST'])
def post_example():
    product_title = ''
    product_price = ''
    product_description = ''
    image_url = ''
    critical_reviews_url = ''
    reviews = []
    data = request.get_json()

    asin = data.get('ASIN', '')
    base_url = 'https://www.amazon.com/dp/'
    base_url = base_url + asin + '?th=1'
    # return base_url
    # Set headers for your request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'aws-ubid-main=944-7538757-0673725; regStatus=registering; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19626%7CMCMID%7C42471595777138831613683393735419461672%7CMCAAMLH-1696240843%7C6%7CMCAAMB-1696240843%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1695643244s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19633%7CvVersion%7C4.4.0; session-id=142-0658299-9275014; i18n-prefs=USD; ubid-main=133-5478043-4681045; lc-main=en_US; x-main="X8?wJ1Rd6sm94iCocUWTZXLXqKqSzPDpR1eRyPmlIAyB6Rrm8Ya@I44yK7r8DN5s"; at-main=Atza|IwEBIGvQhE1v2hYu9lZmNX5ygtunXyVHauEWEahAFn2ls1qkbBG4VAbQ8htg4Mlcp_pNkF4T3oz5He9xwfDQL_mb7yw9WuU6GiW-2zCH1Z4tfBuV_p3Hki07IHdSZanejiSF8_Vcxi77_y8QRk4ISDWf8vIQwaczVUPDppu428EaF9O-8uvw9gflvpzta905VwLSdSYhGRjTT3xBv0KSOJoXASjhkB9SE7ikkhAYwRafhhgLsA; sess-at-main="+4gbKK0bETh+osIoNpRFfpb3BEopGUxPZU0D2feh8G8="; sst-main=Sst1|PQGUm2aFPWx_Sd18P99HCA41CQL8Bne8CPuroR67uQTsFfLDpH8Icb1iUGcvIFeqXhlgBgqHSlUA5l9ImEtEWM4JbE0YGl5yWJ_3TnlhqWzoXgP97MNSIHdNquEBtPgAfINYnEA6zgGiM3Nt1ZjRAWN0uoGry_Zbb6BJBhbnS5YaaXrOLin5WAx4xpmQUxjekppwGyPoWyYo7oNDf8l5sCD_gV1eJ3DloClPda47YKJZ8e9XUdIdGmU8QLwFrw4UnbKMxDZ76IznV-f8J8qMy4SrcQNLJvRXD5IFyNihfN3lTGw; _rails-root_session=ZWlFYVlicG1NMTRhUUlYaW9qZHU4RkpkdFRwS0V1bGhLT0pQSVVSUW4zcmZCOWFvU3pJT1lHU2s4ZjBPR0w4c3FRT3VjV2xaSGsxM3FPRzNCY3ErMFhPdWZtVTc2ZUY4OVNJc2d3Y2VNZEVpUUt1VlQ3Y0xBejA4OGoreUUyVVdWMjRKNWVMNkM4dFloQVMrZ2o2UER1OGMyZmFDZnhRbkZVVkZDZXNZMUxxRDd6dkhvZEFPN2pPb3FNTnl3Q0dYLS1yZW9XdlNVYmwva1hQU0ZydjVLc0tnPT0%3D--4e140b7c83aa3f69cdb9295fe1259144ea52c47b; s_fid=2F5A41B14783D560-2D06C7FDD66E8913; s_cc=true; session-id-time=2082787201l; JSESSIONID=53DAC393871A3B2784DAFB72E3A9D216; session-token=UjuBLWXa1OWXa6o3Do6KFofDHszIpATOA+nv+JOozAe43gTdw0FSn66jjUC/XYysIzSdXEX2SE+XV7wJq1QqSC9tAqKXE1ijf43bmE4MLKRsA93d8I1l54EmVfr8nqK6aQvFioR7eIUxUDHr5dyOSbBxov+JiscKBE4pnjUv/bmbGwROQy7R5fk6gYvSE4DFKjaDZC4BVe06A4Xf3RLnw5a6R+uqjGN4S+UOI2I/jzJ24G+ZhJcA+gctTh3uXI90m3vJlDZ5OFGlz8KU6IW2h2QPgngx2w8tqQoJdl0PWO56MGsg7FD/7Yl+rSEmmsROyIpiSe0+fUac/tanOLua1kDUtYrkS3jdlgYtJXaEh4z5KUHgJwWERlIZAmzBBJQb; csm-hit=tb:CHG6Z7BRVMCG06D50QXJ+s-CHG6Z7BRVMCG06D50QXJ|1700782346161&t:1700782346161&adb:adblk_yes'
    }

    # Make the request
    response = requests.get(base_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # ------------------Extract the product title----------------------
        product_title_element = soup.find('span', {'id': 'productTitle', 'class': 'a-size-large product-title-word-break'})
        if product_title_element is not None:
            product_title = product_title_element.text.strip()
            print("Product Title:", product_title)
        else:
            print("Product title not found in the HTML response.")
        
        # ------------------Extract the price------------------------------
        price_element = soup.find('span', {'class': 'a-offscreen'})
        product_price = price_element.get_text(strip=True)
        print("Product Price:", product_price)

        # -------------------Extract the product description---------------
        description_div = soup.find('div', {'id': 'productDescription'})
        product_description = description_div.get_text(strip=True)
        print("Product Description:", product_description)

        # -------------------Extract the src image url---------------------
        img_tag = soup.find('li', {'class': 'image'}).find('img')
        image_url = img_tag['src']
        print("Image URL:", image_url)

        # -------------------Find the critical reviews URL-----------------
        # Find the 'See more reviews' link
        see_more_reviews_link = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})
        # Extract the href attribute
        reviews_url = "https://www.amazon.com" + see_more_reviews_link['href']
        print("See more reviews URL:", reviews_url)

        # convert 'see more reviews' link to 'critical reviews' link
        tp_url = reviews_url + "&filterByStar=critical&pageNumber=1"
        pattern_to_find = r'cm_cr_dp_d_show_all_btm'
        replacement_pattern = 'cm_cr_arp_d_viewopt_sr'
        critical_reviews_url = re.sub(pattern_to_find, replacement_pattern, tp_url)
        print("Critical Reviews URL:", critical_reviews_url)

        # --------------------Extract the critical reviews-------------------
        def scrape_critical_page(soup, reviews):
            review_elements = soup.find_all('div', class_='a-section review aok-relative')

            for element in review_elements:
                reviewer_name = element.find('span', class_='a-profile-name').text
                star_num = element.find('span', class_='a-icon-alt').text
                review_date = element.find('span', class_='a-size-base a-color-secondary review-date').text
                review_content = element.find('div', class_='a-row a-spacing-small review-data').text

                reviews.append(
                    {
                        'name of reviewer': reviewer_name,
                        'number of stars': star_num,
                        'date of review': review_date,
                        'content of review': review_content
                    }
                )   
        
        critical_reviews_response = requests.get(critical_reviews_url, headers=headers)
        critical_reviews_soup = BeautifulSoup(critical_reviews_response.text, 'html.parser')

        # scraping the critical reviews page
        scrape_critical_page(critical_reviews_soup, reviews)

        next_li_element = critical_reviews_soup.find('li', {'class': 'a-last'}).find('a')
        while next_li_element is not None:
            next_page_relative_url = next_li_element['href']
            page = requests.get("https://www.amazon.com" + next_page_relative_url, headers=headers)
            soup = BeautifulSoup(page.text, 'html.parser')
            scrape_critical_page(soup, reviews)
            next_li_element = soup.find('li', {'class': 'a-last'}).find('a')


        print("#####################################")
        print(len(reviews))
        
        all_reviews = ""
        for review in reviews:
            content_of_review = review.get('content of review', '')
            all_reviews += content_of_review
            
        # analysis the negative review using openAI API
        messages = [
            {"role": "user", "content": all_reviews},
            {"role": "assistant", "content": "These are the packet of many customers' feedback of the product on Amazon. Please analyze the negative aspect of this review for the product sellers. Summarize the answer that good to see.'"}
        ]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )

        analysis_result = completion.choices[0].message.content

    else:
        print(f"Error: {response.status_code}")

    result = {
        'product_title': product_title,
        'product_price': product_price,
        'product_description': product_description,
        'image_url': image_url,
        'critical_reviews_url': critical_reviews_url,
        'reviews': reviews,
        'analysis_result': analysis_result
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)