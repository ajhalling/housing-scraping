# -*- coding: utf-8 -*-
import scrapy


class JRSpider(scrapy.Spider):
    name = 'JR'
    allowed_domains = ['suumo.jp']
    start_urls = [
        'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04']
    
    def parse(self, response):
        listings = response.xpath('//*[@class="cassetteitem"]')
        for listing in listings:

            # initial block
            title = listing.xpath(
                './/*[@class="cassetteitem_content-title"]/text()').extract_first()
            area = listing.xpath(
                './/*[@class="cassetteitem_detail-col1"]/text()').extract_first()
            distances = listing.xpath(
                './/*[@class="cassetteitem_detail-col2"]/div/text()').extract()
            building_age = listing.xpath(
                './/*[@class="cassetteitem_detail-col3"]/div[1]/text()').extract_first()
            stories_tall = listing.xpath(
                './/*[@class="cassetteitem_detail-col3"]/div[2]/text()').extract_first()

            # int for number of listings
            number_of_listings = len(listing.xpath(
                './/*[@class="js-cassette_link"]'))

            # listing information
            for i in range(0, number_of_listings):
                raw_floor = listing.xpath(
                    './/*[@class="js-cassette_link"]/td[3]/text()').extract()
                floor = (raw_floor[0]).strip()

                raw_price = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--rent"]/span/text()').extract()
                price = raw_price[i]

                raw_administrative_cost = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--administration"]/text()').extract()
                administrative_cost = raw_administrative_cost[i]

                raw_deposit = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--deposit"]/text()').extract()
                deposit = raw_deposit[i]

                raw_gratuity = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--gratuity"]/text()').extract()
                gratuity = raw_gratuity[i]

                raw_rooms = listing.xpath(
                    './/span[@class="cassetteitem_madori"]/text()').extract()
                rooms = raw_rooms[i]

                raw_sqmeters = listing.xpath(
                    './/span[@class="cassetteitem_menseki"]/text()').extract()
                sqmeters = raw_sqmeters[i]

                links = listing.xpath(
                    './/*[@class="ui-text--midium ui-text--bold"]/a/@href').extract()

                raw_absolutelinks = []

                for link in links:
                    raw_absolutelinks.append(response.urljoin(link))
                absolutelink = raw_absolutelinks[i]

                yield {'Listing Title': title,
                       'Area': area,
                       'Distances to Railway Stations': distances,
                       'Building Age': building_age,
                       'Stories Tall': stories_tall,
                       'Floor': floor,
                       'Price': price,
                       'Administrative Costs': administrative_cost,
                       'Deposit': deposit,
                       'Gratuity': gratuity,
                       'Rooms': rooms,
                       'Square Meters': sqmeters,
                       'Links to Listing': absolutelink}
              
        print("Finished Page: "+response.request.url)
        finished_page = response.request.url
        
        if str(finished_page) == 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13112&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=04':
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p/a/@href').extract_first()
            print('ran first')

        else:
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p[2]/a/@href').extract_first()
            print('ran second')   

        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)

       
            

        print(next_page_url)

        print("beginning to scrape: "+absolute_next_page_url)
