# -*- coding: utf-8 -*-
import scrapy


target = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&sc=13300&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=']


class SuumoHousingSpider(scrapy.Spider):
    name = 'suumo_housing'
    allowed_domains = ['suumo.jp']
    start_urls = target

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

            # split each distance to the station into
            try:
                distance1 = distances[0]
            except:
                distance1 = None
            else:
                distance1 = distances[0]

            try:
                distance2 = distances[1]
            except:
                distance2 = None
            else:
                distance2 = distances[1]

            try:
                distance3 = distances[2]
            except:
                distance3 = None
            else:
                distance3 = distances[2]

            # building age
            building_age_raw = listing.xpath(
                './/*[@class="cassetteitem_detail-col3"]/div[1]/text()').extract_first()
            building_age_str = ""
            for i in list(building_age_raw):
                if i == "築":
                    continue
                elif i == "年":
                    continue
                elif i ==  "新":
                    building_age_str += "0"
                else:
                    building_age_str += i
            try:
                building_age = float(building_age_str)
            except:
                building_age = building_age_str
            

            # stories tall
            stories_tall_raw = listing.xpath(
                './/*[@class="cassetteitem_detail-col3"]/div[2]/text()').extract_first()
            stories_tall_str = ""
            for i in list(stories_tall_raw):
                if i == "建":
                    continue
                elif i == "階":
                    continue
                else:
                    stories_tall_str += i
            try:
                stories_tall = float(stories_tall_str)
            except:
                stories_tall = stories_tall_str

            # int for number of listings
            number_of_listings = len(listing.xpath(
                './/*[@class="js-cassette_link"]'))

            # listing information
            var_iter = 0
            for i in range(0, number_of_listings):
                links = listing.xpath(
                    './/*[@class="ui-text--midium ui-text--bold"]/a/@href').extract()
                raw_absolutelinks = []

                for link in links:
                    raw_absolutelinks.append(response.urljoin(link))
                absolutelink = raw_absolutelinks[var_iter]

                # price
                raw_price = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--rent"]/span/text()').extract()
                price = raw_price[var_iter]
                pricestring = ""
                for i in list(price):
                    if i == "円":
                        continue
                    elif i == "万":
                        continue
                    else:
                        pricestring += i
                try:
                    price = (float(pricestring)*1000)
                except:
                    price = pricestring

                # floor
                raw_floor = listing.xpath(
                    './/*[@class="js-cassette_link"]/td[3]/text()').extract()
                floor = (raw_floor[0]).strip()
                floor_str = ""
                for i in list(floor):
                    if i == "階":
                        continue
                    elif i == "-":
                        break
                    else:
                        floor_str += i
                try:
                    floor = float(floor_str)
                except:
                    floor = floor_str

                # administrative cost
                raw_administrative_cost = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--administration"]/text()').extract()
                administrative_cost = raw_administrative_cost[var_iter]
                administrative_str = ""
                for i in list(administrative_cost):
                    if i == "円":
                        continue
                    elif i == "万":
                        continue
                    elif i == "-":
                        administrative_str += "0"
                    else:
                        administrative_str += i
                try:
                    administrative_cost = float(administrative_str)
                except:
                    administrative_cost = administrative_str

                #rooms
                raw_rooms = listing.xpath(
                    './/span[@class="cassetteitem_madori"]/text()').extract()
                rooms = raw_rooms[var_iter]
                rooms_str = ""
                for i in list(rooms):
                    try:
                        float(i)
                    except:
                        continue
                    else:
                        rooms_str += i
                try:
                    rooms = float(rooms_str)
                except:
                    rooms = rooms_str
                
                #deposit
                raw_deposit = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--deposit"]/text()').extract()
                deposit = raw_deposit[var_iter]
                deposit_str = ""
                for i in list(deposit):
                    if i == "万":
                        continue
                    elif i == "円":
                        continue
                    elif i == "-" or i == '':
                        deposit_str += "0"
                    else:
                        deposit_str += i
                try:
                    deposit = (float(deposit_str)*1000)
                except:
                    deposit = deposit_str

                #gratuity
                raw_gratuity = listing.xpath(
                    './/span[@class="cassetteitem_price cassetteitem_price--gratuity"]/text()').extract()
                gratuity = raw_gratuity[var_iter]
                gratuity_str = ""
                for i in list(gratuity):
                    if i == "万":
                        continue
                    elif i == "円":
                        continue
                    elif i == "-" or i == '':
                        gratuity_str += "0"
                    else:
                        gratuity_str += i
                try:
                    gratuity = (float(gratuity_str)*1000)
                except:
                    gratuity = gratuity_str
                
                #sqmeters
                raw_sqmeters = listing.xpath(
                    './/span[@class="cassetteitem_menseki"]/text()').extract()
                sqmeters = raw_sqmeters[var_iter]
                sqmeters_str = ""
                for i in list(sqmeters):
                    if i == "m" or i == "M":
                        continue
                    else:
                        sqmeters_str += i
                try:
                    sqmeters = float(sqmeters_str)
                except:
                    sqmeters = sqmeters_str


                yield {'title': title,
                       'area': area,
                       'station1': distance1,
                       'station2': distance2,
                       'station3': distance3,
                       'building_age': building_age,
                       'stories_tall': stories_tall,
                       'floor': floor,
                       'price': price,
                       'administrative_cost': administrative_cost,
                       'deposit': deposit,
                       'gratuity': gratuity,
                       'rooms': rooms,
                       'sq_meters': sqmeters,
                       'link': absolutelink}
                var_iter +=  1


        print("Finished Page: "+response.request.url)
        finished_page = response.request.url

        if str(finished_page) == 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13119&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&sc=13300&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=':
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p/a/@href').extract_first()
            print('ran first')

        else:
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p[2]/a/@href').extract_first()
            print('ran second')   
        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)

        print(next_page_url)

        print("beginning to scrape: "+absolute_next_page_url)
