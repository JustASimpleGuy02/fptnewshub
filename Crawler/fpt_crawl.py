import scrapy
import justext

class FptCrawlSpider(scrapy.Spider):
    name = "fpt_crawl"
    allowed_domains = ["hanoi.fpt.edu.vn"]
    start_urls = ["https://hanoi.fpt.edu.vn/360-do-hoa-lac"]

    def parse(self, response):
        result = []
        paragraphs = justext.justext(response.content, justext.get_stoplist("Vietnamese"))
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                result.append(paragraph.text)
        result = '\n'.join(result)
        yield {
            
        }

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)
