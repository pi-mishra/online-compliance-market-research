import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


def extract_reviews(page_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    review_articles = soup.find_all(
        "article", attrs={"data-service-review-card-paper": True}
    )

    reviews_data = []

    for article in review_articles:
        review_text = None
        review_date = None
        rating = None

        text_tag = article.find(
            "p", attrs={"data-service-review-text-typography": True}
        )
        if text_tag:
            review_text = text_tag.get_text(strip=True)

        time_tag = article.find("time")
        if time_tag:
            review_date = time_tag.get_text(strip=True)

        rating_div = article.find(
            "div", attrs={"data-service-review-rating": True}
        )
        if rating_div:
            rating = rating_div.get("data-service-review-rating")

        reviews_data.append(
            {
                "review_text": review_text,
                "review_date": review_date,
                "rating": rating,
            }
        )

    return reviews_data


def extract_all_reviews(base_url, from_page=1, to_page=5, sleep_time=1):
    all_reviews = []

    for page in range(from_page, to_page + 1):
        page_url = f"{base_url}?page={page}"
        print(f"Scraping: {page_url}")
        all_reviews.extend(extract_reviews(page_url))
        sleep(sleep_time)

    return pd.DataFrame(all_reviews)
