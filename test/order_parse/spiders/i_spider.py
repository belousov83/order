import pandas as pd
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

items = []

class ISpider(CrawlSpider):
    name = "i_spider"
    allowed_domains = ["order-nn.ru"]
    start_urls = [
        "https://order-nn.ru/kmo/catalog/5974/",
        "https://order-nn.ru/kmo/catalog/9460/",
        "https://order-nn.ru/kmo/catalog/5999/",
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="horizontal-product-item-block_3_2"]/a'), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="ul-pagination"]/li/a')),
    )

    def parse_item(self, response):
        ink_name = response.xpath('//h1/text()').get()

        price = response.xpath('//span[@class="element-current-price-number"]/text()').get()
        if price is not None:
            price = price.replace(" ", "")

        ink_description = (" ".join(
            response.xpath('//*[@id="block-description"]//text()').getall()
        )).strip()

        char = {}
        table = response.xpath('//*[@id="block-character"]/div[2]/table')
        for row in table.xpath('//tr'):
            info = row.xpath('.//td//text()').getall()
            char[info[0]] = info[1]

        new_item = {
            'Name': ink_name,
            'Price': price,
            'Description': ink_description,
            'Specifications': char
        }
        items.append(new_item)
        x = pd.DataFrame(items, columns=['Name', 'Price', 'Description', 'Specifications'])

        yield x.to_csv("ink_pd.csv", sep=",")