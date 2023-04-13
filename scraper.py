from requests import get, codes
from bs4 import BeautifulSoup

# product_code = input("Please enter product code: ")
product_code = "36991221"
# product_code = "150607722"
# url = "https://www.ceneo.pl/" + product_code + "#tab=reviews"
# url = "https://www.ceneo.pl/{}#tab=reviews".format(product_code)
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = get(url)
if response.status_code == codes['ok']:
    page_dom = BeautifulSoup(response.text, "html.parser")
    try:
        opinions_count = int(page_dom.select_one("a.product-review__link > span").text.strip())
    except AttributeError:
        opinions_count = 0
    if opinions_count > 0:
        all_opinions = []
        opinions = page_dom.select("div.js_product-review")
        for opinion in opinions:
            id = opinion["data-entry-id"]
            author = opinion.select_one("span.user-post__author-name").text.strip()
            try:
                recommendation = opinion.select_one("span.user-post__author-recommendation > em").text.strip()
            except AttributeError:
                recommendation = None
            stars = opinion.select_one("span.user-post__score-count").text.strip()
            content = opinion.select_one("div.user-post__text").text.strip()
            pros = opinion.select("div.review-feature__title--positives ~ div.review-feature__item")
            pros = [p.text.strip() for p in pros]
            cons = opinion.select("div.review-feature__title--negatives ~ div.review-feature__item")
            cons = [c.text.strip() for c in cons]
            upvote = opinion.select_one("button.vote-yes")["data-total-vote"].strip()
            downvote = opinion.select_one("button.vote-no")["data-total-vote"].strip()
            posted = opinion.select_one("span.user-post__published > time:nth-child(1)")["datetime"].strip()
            try:
                purchased = opinion.select_one("span.user-post__published > time:nth-child(2)")["datetime"].strip()
            except TypeError:
                purchased = None

            single_opinion = {
                "id": id,
                "author": author,
                "recommendation": recommendation,
                "stars": stars,
                "content": content,
                "pros": pros,
                "cons": cons,
                "upvote": upvote,
                "downvote": downvote,
                "posted": posted,
                "purchased": purchased
            }
            all_opinions.append(single_opinion)
        print(all_opinions)

    