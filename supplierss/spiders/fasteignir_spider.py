import scrapy
from scrapy import Request
import random
from furl import furl

class SuppliersSpider(scrapy.Spider):
    name = "fasteignir"

    custom_settings = {
        'FEEDS': {
            'fasteignir.csv': {
                'format': 'csv',
                'encoding': 'utf-8-sig',
                'overwrite': True,
            },
        },
    }
   
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://fasteignir.visir.is/search/results/?stype=sale',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    start_urls = ['https://fasteignir.visir.is/search/results/?stype=sale#/?zip=101,102,103,104,105,107,108,109,110,111,112,113,116,161,162,200,201,202,203,206,210,212,225,220,221,222,270,271,276,170,230,232,233,262,240,241,245,246,250,251,260,190,191,500,510,511,512,520,522,523,524,530,531,540,541,545,546,550,551,560,561,565,566,570,580,581,600,601,602,603,604,605,606,607,610,616,611,620,621,625,626,630,640,641,645,650,660,670,671,675,680,681,400,401,410,415,416,420,421,425,426,430,431,450,451,460,461,465,466,470,471,300,301,302,310,311,320,340,341,342,345,350,351,355,356,360,370,371,380,381,685,690,691,700,701,710,711,711,715,720,721,730,731,735,736,740,741,750,751,755,756,760,761,765,780,781,785,800,801,802,803,804,805,806,810,815,816,820,825,840,845,846,850,851,860,861,870,871,880,881,900,901&price=1000000,100000000%22&category=2,1,4,7,17,3,6,35,8,36&stype=sale&searchid=116598637&page=3']

    def parse(self, response):
        
        links=[
            
            #'https://fasteignir.visir.is/ajaxsearch/getresults?zip=101,102,103,104,105,107,108,109,110,111,112,113,116,161,162,200,201,202,203,206,210,212,225,220,221,222,270,271,276,170,230,232,233,262,240,241,245,246,250,251,260,190,191,500,510,511,512,520,522,523,524,530,531,540,541,545,546,550,551,560,561,565,566,570,580,581,600,601,602,603,604,605,606,607,610,616,611,620,621,625,626,630,640,641,645,650,660,670,671,675,680,681,400,401,410,415,416,420,421,425,426,430,431,450,451,460,461,465,466,470,471,300,301,302,310,311,320,340,341,342,345,350,351,355,356,360,370,371,380,381,685,690,691,700,701,710,711,711,715,720,721,730,731,735,736,740,741,750,751,755,756,760,761,765,780,781,785,800,801,802,803,804,805,806,810,815,816,820,825,840,845,846,850,851,860,861,870,871,880,881,900,901&price=1000000,100000000%22&category=2,1,4,7,17,3,6,35,8,36&stype=sale&searchid=116598637&page=1',
            #'https://fasteignir.visir.is/ajaxsearch/getresults?stype=rent&searchid=5597134&page=1',
            #'https://fasteignir.visir.is/ajaxsearch/getresults?zip=101,102,103,104,105,107,108,109,110,111,112,113,116,161,162,200,201,202,203,206,210,212,225,220,221,222,270,271,276,170,230,232,233,262,240,241,245,246,250,251,260,190,191,500,510,511,512,520,522,523,524,530,531,540,541,545,546,550,551,560,561,565,566,570,580,581,600,601,602,603,604,605,606,607,610,616,611,620,621,625,626,630,640,641,645,650,660,670,671,675,680,681,400,401,410,415,416,420,421,425,426,430,431,450,451,460,461,465,466,470,471,300,301,302,310,311,320,340,341,342,345,350,351,355,356,360,370,371,380,381,685,690,691,700,701,710,711,711,715,720,721,730,731,735,736,740,741,750,751,755,756,760,761,765,780,781,785,800,801,802,803,804,805,806,810,815,816,820,825,840,845,846,850,851,860,861,870,871,880,881,900,901&category=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&stype=companies&searchid=242054&page=1'
            'https://fasteignir.visir.is/ajaxsearch/getresults?zip=%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20Select%20an%20area%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20&stype=rent&searchid=5597144&page=1'
        
        ]
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.category_parse,headers=self.headers)

    def category_parse(self, response):
        
        links=response.xpath('//a[@class="js-property-link"]/@href').extract()
        for link in links:
            link='https://fasteignir.visir.is'+str(link)
            yield scrapy.Request(url=link, callback=self.scrape_page,headers=self.headers)
            
        
        next_page_text = response.xpath('//a[@class="current"]/following-sibling::a/text()').get()
        if next_page_text:
            next_page_number = int(next_page_text)
            next_page_url = self.construct_next_page_url(response.url, next_page_number)
            print(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.category_parse)
            
    def construct_next_page_url(self, current_url, next_page_number):
        parsed_url = furl(current_url)
        parsed_url.args['page'] = next_page_number
        return str(parsed_url)
  
    def scrape_page(self, response):
        
        item = {}
        title = response.xpath('//h3[@class="property__center-title"]/text()').get()
        item['title']=title
       
        item['property_number'] = response.xpath('//div[@class="property__bottom-item"]/div[@class="property__bottom-text"][contains(text(), "Fasteignanúmer")]/following-sibling::h4[@class="property__bottom-title"]/text()').get()
        item['property_price'] = response.xpath('//div[@class="property__bottom-item"]/div[@class="property__bottom-text"][contains(text(), "Fasteignamat")]/following-sibling::h4[@class="property__bottom-title"]/text()').get()
        item['additional_cost'] = response.xpath('//div[@class="property__bottom-item"]/div[@class="property__bottom-text"][contains(text(), "Brunabótamat")]/following-sibling::h4[@class="property__bottom-title"]/text()').get()
        item['debt'] = response.xpath('//div[@class="property__bottom-item"]/div[@class="property__bottom-text"][contains(text(), "Áhvílandi")]/following-sibling::h4[@class="property__bottom-title"]/text()').get()

        item['built_year'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "Byggt")]/text()').get()
        item['size'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "m²")]/text()').get()
        item['rooms'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "herb.")]/text()').get()
        item['bathrooms'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "baðherb.")]/text()').get()
        item['bedrooms'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "svefnh.")]/text()').get()
        item['shared_entrance'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "Sameiginl. inngangur")]/text()').get()
        item['parking'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "Bílastæði")]/text()').get()
        item['elevator'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "Lyfta")]/text()').get()
        item['laus_strax'] = response.xpath('//div[@class="description__head-item"]/div[@class="description__head-text"][contains(text(), "Laus strax")]/text()').get()

        
        item['price'] = response.xpath('//h3[@class="property__center-price"]/text()').get()
        item['price_per_sqm'] = response.xpath('//div[@class="property__center-text property__center-text-right"]/text()').get()


        item['property_type'] = response.xpath('//div[@class="property__center-class"]/text()').get()
      
        address = response.xpath('//div[@class="property__center-text"]/text()').get()
        if  address:
            item['property_address'] = f"{address.strip()}"
        else:
            item['property_address'] = None

        item['latitude']=''
        item['longitude']=''
        self.log(f'Extracted Item: {item}')
        map_link = response.xpath('//div[@class="property__head-item"]/a[contains(@href, "google.com/maps?q=")]/@href').get()
        if map_link:
            coordinates = self.extract_coordinates_from_map_link(map_link)
            if coordinates:
                item['latitude'], item['longitude'] = coordinates
                
        description_text = response.xpath('//div[@class="description__bottom-text"]/descendant-or-self::*/text()').getall()
        
        item['description'] = ' '.join(description_text).strip()
        item['url'] = response.url
        for key in item:
            if isinstance(item[key], str):
                item[key] = item[key].strip() if item[key] else None

       
        
        
        yield item
        
    def extract_coordinates_from_map_link(self, map_link):
        try:
           
            coordinates = map_link.split('q=')[1].split(',')
            latitude = float(coordinates[0])
            longitude = float(coordinates[1])
            return latitude, longitude
        except Exception as e:
            self.logger.error(f"Error extracting coordinates from map link: {e}")
            return None 