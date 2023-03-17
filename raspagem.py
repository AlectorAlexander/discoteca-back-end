from parsel import Selector
import requests
import time


def fetch(url):
    try:
        page = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=3
        )
        if page.status_code == 200:
            return page.text
        else:
            return None
    except requests.ReadTimeout:
        print("muita demora em responder. A leitura foi cancelada")
        return None


def scrape_cards(html_content):
    selector = Selector(text=html_content)
    response = selector.css("tbody tr::attr(onclick)").getall()
    cards = []
    for card in response:
        cards.append(
            card.replace("window.location=", "")
            .replace(";", "")
            .replace("'", "")
        )
    print("retornando cards")
    return cards


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    nexter = selector.css("[rel='next']::attr(href)").get()
    print("retornando link da próxima página")
    return nexter


def scrape_details(tags):
    details = {}
    for tag in tags:
        selector = Selector(text=tag)
        attribute = selector.css('strong::text').get()
        value = ''.join(selector.css('p::text').getall())
        if value == '  ' or value == '   ':
            value = ''.join(selector.css('p a::text').getall())
        details[attribute] = value
    return details


def scrape_musics(tags):
    musics = []
    for tag in tags:
        selector = Selector(text=tag)
        value = ''.join(selector.css('::text').getall())
        musics.append(value)
    return musics


def scrape_disco(html_content):
    selector = Selector(text=html_content)
    title = selector.css("h1::text").get()
    artist = selector.css("h2 a::text").get()
    url_img = selector.css("img::attr(src)").get()
    details = scrape_details(selector.css(".mt-4 .m-0").getall())
    musics = scrape_musics(selector.css(".btn-link").getall())

    response = {}
    response["title"] = title
    response["details"] = details
    response["artist"] = artist
    response["musics"] = musics
    response["url_img"] = f"https://discografia.discosdobrasil.com.br{url_img}"
    return response


def increment_urls(list_news_url, new_url):
    new_list = scrape_cards(fetch(new_url))
    for new in new_list:
        list_news_url.append(new)
    return list_news_url


def get_discos(amount):
    url = "https://discografia.discosdobrasil.com.br/discos"
    response = fetch(url)
    let = 0
    list_discs = []
    list_news_url = scrape_cards(response)
    while len(list_news_url) <= amount:
        print('adicionando novos links no array urls')
        url = scrape_next_page_link(fetch(url))
        list_news_url = increment_urls(list_news_url, url)
    for new_url in list_news_url:
        print(f'ajustando {let}')
        let += 1
        if len(list_discs) < amount:
            new = scrape_disco(fetch(new_url))
            list_discs.append(new)
        else:
            break
    for i in list_discs:
        print(f'---{i["title"]}---')
    print(list_discs)
    time.sleep(5)
    return list_discs
