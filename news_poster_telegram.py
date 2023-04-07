import requests
from bs4 import BeautifulSoup
import openai
import schedule
import time
import os

# TODO: Completează credențialele pentru Telegram și OpenAI
telegram_bot_token = "6058301449:AAHEYAYf4HE6dqHxv_OwVFuQfRi7vRaLGgQ"
telegram_chat_id = "@blockchainimpulse"
openai_api_key = "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"

def extract_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_elements = soup.find_all("div", class_="main-post__container")
    
    news_list = []
    for news in news_elements:
        news_title = news.find("h2", class_="main-post__title").text.strip()
        news_url = news.find("a")["href"]
        news_list.append({"title": news_title, "url": news_url})
        
    return news_list

def send_telegram_message(bot_token, chat_id, text):
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}"
    response = requests.get(send_text)
    return response.json()

def generate_text(api_key, prompt, model="text-davinci-002", max_tokens=50):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    generated_text = response.choices[0].text.strip()
    return generated_text

def post_news_telegram():
    url = "https://cointelegraph.com/"
    news_list = extract_news(url)

    for news in news_list:
        news_title = news["title"]
        news_url = news["url"]

        prompt = f"Prezintă în mod original știrea: {news_title} {news_url}"
        original_text = generate_text(openai_api_key, prompt)

        send_telegram_message(telegram_bot_token, telegram_chat_id, original_text)

if __name__ == "__main__":
    schedule.every(30).minutes.do(post_news_telegram)

    while True:
        schedule.run_pending()
        time.sleep(1)
