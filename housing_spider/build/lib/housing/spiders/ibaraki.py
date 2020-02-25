# -*- coding: utf-8 -*-
import scrapy


target = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=08&sc=08201&sc=08202&sc=08203&sc=08204&sc=08205&sc=08207&sc=08208&sc=08210&sc=08211&sc=08212&sc=08214&sc=08215&sc=08216&sc=08217&sc=08219&sc=08220&sc=08221&sc=08222&sc=08223&sc=08224&sc=08225&sc=08226&sc=08227&sc=08228&sc=08229&sc=08230&sc=08231&sc=08232&sc=08233&sc=08234&sc=08235&sc=08236&sc=08300&sc=08340&sc=08360&sc=08440&sc=08520&sc=08540&sc=08560&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=']

zone = "Ibaraki"

class IbarakiSpider(scrapy.Spider):
    name = 'ibaraki'
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
                rooms = str(raw_rooms[var_iter])
                # rooms_str = ""
                
                studio = ["ワンルーム"]
                one_room = ["1K","1DK", "1LDK", "1LK", "1SDK", "1SK", "1SLDK", "1SLK"]
                two_rooms = ["2K","2DK", "2LDK", "2LK", "2SDK", "2SK", "2SLDK", "2SLK"]
                three_rooms = ["3K","3DK", "3LDK", "3LK", "3SDK", "3SK", "3SLDK", "3SLK"]
                four_rooms = ["4K","4DK", "4LDK", "4LK", "4SDK", "4SK", "4SLDK", "4SLK"]
                five_rooms = ["5K","5DK", "5LDK", "5LK", "5SDK", "5SK", "5SLDK", "5SLK"]
                six_rooms = ["6K","6DK", "6LDK", "6LK", "6SDK", "6SK", "6SLDK", "6SLK"]
                seven_rooms = ["7K","7DK", "7LDK", "7LK", "7SDK", "7SK", "7SLDK", "7SLK"]
                eight_rooms = ["8K","8DK", "8LDK", "8LK", "8SDK", "8SK", "8SLDK", "8SLK"]
                nine_rooms = ["9K","9DK", "9LDK", "9LK", "9SDK", "9SK", "9SLDK", "9SLK"]

                if rooms in studio:
                    rooms = 0
                elif rooms in one_room:
                    rooms = 1
                elif rooms in two_rooms:
                    rooms = 2
                elif rooms in three_rooms:
                    rooms = 3
                elif rooms in four_rooms:
                    rooms = 4
                elif rooms in five_rooms:
                    rooms = 5
                elif rooms in six_rooms:
                    rooms = 6
                elif rooms in seven_rooms:
                    rooms = 7
                elif rooms in eight_rooms:
                    rooms = 8
                elif rooms in nine_rooms:
                    rooms = 9
                else:
                    rooms = None

                try:
                    rooms = float(rooms)
                except:
                    rooms = rooms

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
                       'zone': zone,
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

        if str(finished_page) == 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=11&sc=11101&sc=11102&sc=11103&sc=11104&sc=11105&sc=11106&sc=11107&sc=11108&sc=11109&sc=11110&sc=11201&sc=11202&sc=11203&sc=11206&sc=11207&sc=11208&sc=11209&sc=11210&sc=11211&sc=11212&sc=11214&sc=11215&sc=11216&sc=11217&sc=11218&sc=11219&sc=11221&sc=11222&sc=11223&sc=11224&sc=11225&sc=11227&sc=11228&sc=11229&sc=11230&sc=11231&sc=11232&sc=11233&sc=11234&sc=11235&sc=11237&sc=11238&sc=11239&sc=11240&sc=11241&sc=11242&sc=11243&sc=11245&sc=11246&sc=11300&sc=11320&sc=11340&sc=11360&sc=11380&sc=11400&sc=11440&sc=11460&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=':
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p/a/@href').extract_first()
            print('ran first')

        else:
            next_page_url = response.xpath('//*[@id="js-leftColumnForm"]/div[11]/div/p[2]/a/@href').extract_first()
            print('ran second')   
        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)

        print(next_page_url)

        print("beginning to scrape: "+absolute_next_page_url)
