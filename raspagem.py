from parsel import Selector
import requests


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


def get_tech_news(amount):
    url = "https://blog.betrybe.com/"
    response = fetch(url)
    list_news = []
    list_news_url = scrape_novidades(response)
    while len(list_news_url) <= amount:
        print('adicionando novos links no array urls')
        url = scrape_next_page_link(fetch(url))
        list_news_url = increment_urls(list_news_url, url)
    for new_url in list_news_url:
        if len(list_news) < amount:
            new = scrape_noticia(fetch(new_url))
            list_news.append(new)
        else:
            break
    create_news(list_news)
    for i in list_news:
        print(f'---{i["title"]}---')
    print(len(list_news))
    return list_news



if __name__ == "__main__":
    test = fetch(
        "https://discografia.discosdobrasil.com.br/discos/"
        "e-a-gente-nem-deu-nome"
    )
    test2 = scrape_cards(test)
    test3 = scrape_next_page_link(test)
    test4 = scrape_disco(test)
    print(test4)
