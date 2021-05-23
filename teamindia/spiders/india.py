from scrapy import Spider
from scrapy.http import Request
import os
from scrapy.loader import ItemLoader
from teamindia.items import TeamindiaItem
import csv
import glob
import mysql.connector

class IndiaSpider(Spider):
    name = 'india'
    allowed_domains = ['bcci.tv']
    start_urls = ['https://www.bcci.tv/players/men']

    def parse(self, response):
        player_url = response.xpath('//*[@class = "player-item"]/@href').extract()
        for players in player_url:
            player_url = response.urljoin(players)
            yield Request(player_url, callback = self.parse_data)

    def parse_data(self, response):
        l = ItemLoader(item = TeamindiaItem(), response=response)
        try:
            first_name = response.xpath('//*[@class = "player-bio__first-name"]/text()').extract_first()
            last_name = response.xpath('//*[@class = "player-bio__last-name"]/text()').extract_first()
            Name = first_name + last_name
        except:
            print("No first and last name found")
        else:
            first_name = response.xpath('//*[@class = "player-bio__first-name"]/text()').extract_first()
            last_name = response.xpath('//*[@class = "player-bio__last-name"]/text()').extract_first()
            Name = first_name + last_name
        
            Role = response.xpath('//*[@class = "player-bio__info"]/div[1]/dl/dd/text()').extract_first()
            Dob = response.xpath('//*[@class = "player-bio__info"]/div[2]/dl[2]/dd/text()').extract_first()
            img_id =  response.url.split('/')[4]
            image_urls= 'https://playerimages.platform.bcci.tv/generic/500x640/'+img_id+'.png'
        
            yield{
                 'Name':Name,
                 'Role':Role,
                 'Dob':Dob,
                 'image_urls':image_urls}
            
        #     l.add_value('Name',Name)
        #     l.add_value('Role',Role)
        #     l.add_value('Dob',Dob)
        #     l.add_value('image_urls',image_urls)

        # return l.load_item()
    
    def close(self, reason):

        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        mydb = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '1234@', db= 'team_inida')
        cursor = mydb.cursor()
        with open(csv_file, 'r') as file:
            csv_data = csv.reader(file)
            row_count = 0
            for row in csv_data:
                if row_count != 0:
                   cursor.execute('INSERT IGNORE INTO indian_player(Name, Role, Dob, image_urls) VALUES(%s,%s,%s,%s)', row)
                row_count += 1
        mydb.commit()
        mydb.commit() 


