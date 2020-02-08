from scrapy import Spider
import json
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from unsplash.items import UnsplashItem
from scrapy.loader import ItemLoader



class WallsSpider(Spider):
    item = 0
    name = 'walls'
    allowed_domains = ['unsplash.com']
    # start_urls = ['https://unsplash.com']
    def __init__(self,q):
        self.q = q
        self.start_urls = ['https://unsplash.com/napi/search/photos?query='+self.q+r'&xp=search-no-idf%3Aexcluded&per_page=20&page=1']

    def parse(self, response):

        js = json.loads(response.body)
        pages = js['total_pages']
        print('=========================')
        print(pages)
        js = js['results']
        l = ItemLoader(item=UnsplashItem(), response=response)
        self.item+=1
        print('===============\n'+f'Current Page is {self.item}' +'\n'+ '==============\n')
        for i in js:
            image_urls = i.get('urls').get('raw')
            l.add_value('image_urls', image_urls)
            yield {
            'URL':image_urls,
            'image_urls' :[image_urls],
            }
        try:
            assert self.item <= pages
        except AssertionError:
            raise CloseSpider('Maximum pages crawled!')


        url = r'https://unsplash.com/napi/search/photos?query='+self.q+r'&xp=search-no-idf%3Aexcluded&per_page=20&page=' + str(self.item)
        yield Request(url)
        return l.load_item()
