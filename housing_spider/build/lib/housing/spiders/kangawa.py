# -*- coding: utf-8 -*-
import scrapy


class SuumoHousingSpider(scrapy.Spider):
    name = 'kangawa'
    allowed_domains = ['suumo.jp']
    start_urls = [
        'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14101&sc=14102&sc=14103&sc=14104&sc=14105&sc=14106&sc=14107&sc=14108&sc=14109&sc=14110&sc=14111&sc=14112&sc=14113&sc=14114&sc=14115&sc=14116&sc=14117&sc=14118&sc=14131&sc=14132&sc=14133&sc=14134&sc=14135&sc=14136&sc=14137&sc=14151&sc=14152&sc=14153&sc=14201&sc=14203&sc=14204&sc=14205&sc=14206&sc=14207&sc=14208&sc=14210&sc=14211&sc=14212&sc=14213&sc=14214&sc=14215&sc=14216&sc=14217&sc=14218&sc=14300&sc=14320&sc=14340&sc=14360&sc=14400&sc=14380&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=']

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
        
        if str(finished_page) == 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14101&sc=14102&sc=14103&sc=14104&sc=14105&sc=14106&sc=14107&sc=14108&sc=14109&sc=14110&sc=14111&sc=14112&sc=14113&sc=14114&sc=14115&sc=14116&sc=14117&sc=14118&sc=14131&sc=14132&sc=14133&sc=14134&sc=14135&sc=14136&sc=14137&sc=14151&sc=14152&sc=14153&sc=14201&sc=14203&sc=14204&sc=14205&sc=14206&sc=14207&sc=14208&sc=14210&sc=14211&sc=14212&sc=14213&sc=14214&sc=14215&sc=14216&sc=14217&sc=14218&sc=14300&sc=14320&sc=14340&sc=14360&sc=14400&sc=14380&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=':
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p/a/@href').extract_first()
            print('ran first')

        else:
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p[2]/a/@href').extract_first()
            print('ran second')   

        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)

       
            

        print(next_page_url)

        print("beginning to scrape: "+absolute_next_page_url)
