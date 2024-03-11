import scrapy
from hyperreal.items import HyperrealItem


class HyperDrugSpider(scrapy.Spider):
    name = "Hyper_Drug"
    allowed_domains = ["hyperreal.info"]
    start_urls = [
        "https://hyperreal.info/talk/zdrowie-knajpa.html"]

    def parse(self, response, **kwargs):
        # 本来应该是解析数据的
        # print(response)ß
        # 拿到页面源代码
        # 用 print(response.text)提取数据
        # response.json()
        # response.xpath()  # 用xpath进行数据解析
        # response.css()   # 用css选择器进行解析
        # 获取到页面中所有的游戏名字
        # txt = response.xpath("//ul[@class='n-game cf']/li/a/b/text()").extract()  # 提取内容
        # print(txt)
        # 分块提取数据
        li_list = response.xpath(
            "//div[starts-with(@class,'container-fluid row-item position-relative')]")
        for li in li_list:
            title = li.xpath(
                './/a[@class="topic-title fs-5"]/text()').extract_first()
            link = li.xpath(
                './/a[@class="topic-title fs-5"]/@href').extract_first()
            Hyper = HyperrealItem()
            Hyper['title'] = title
            Hyper['link'] = link
            yield scrapy.Request(
                url=link,
                method="GET",
                callback=self.parse_detail,
                # Pass HyperrealItem object to parse_detail method
                meta={'item': Hyper}
            )

            # Check if there is a next page
            next_page = response.xpath(
                "(//i[@class='fa fa-step-forward fa-fw'])[2]/parent::a")
            # 这个按钮的父类标签藏有下一页的链接，所以要用parent::a，方便下面提取@href
            if next_page:
                next_url = next_page.xpath("@href").extract_first()
                yield scrapy.Request(
                    url=next_url,
                    method="GET",
                    callback=self.parse,
                )

    def parse_detail(self, response):
        elements = response.xpath(
            "//div[@class='timeline-post position-relative clearfix']")  # Get all elements
        # Extract the text from each element and join them together
        separator = "\n·······························································\n"
        file = separator.join(
            [e.xpath("string()").get().strip() for e in elements])
        # Remove consecutive empty lines
        lines = file.splitlines()
        file = "\n".join([lines[i] for i in range(len(lines))
                         if lines[i].strip() or (i > 0 and lines[i-1].strip())])
        # Get HyperrealItem object from meta and store file
        Hyper = response.meta['item']
        Hyper['file'] = file

        # Append file to previous page's file
        prev_file = Hyper['file']
        if 'prev_file' in response.meta:
            prev_file = response.meta['prev_file'] + separator + prev_file

        # Check if there is a next page
        next_page = response.xpath(
            "(//i[@class='fa fa-step-forward fa-fw'])[2]/parent::a")
        if next_page:
            next_url = next_page.xpath("@href").extract_first()
            yield scrapy.Request(
                url=next_url,
                method="GET",
                callback=self.parse_detail,
                # Pass HyperrealItem object and previous file to parse_detail method
                meta={'item': Hyper, 'prev_file': prev_file}
            )
        else:
            # Set the final file by appending the previous file
            Hyper['file'] = prev_file
            yield Hyper
