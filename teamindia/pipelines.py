# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import scrapy
import os

class TeamindiaPipeline:
    def process_item(self, item, spider):
        # os.chdir('/Users/Rahul/projects/teamindia/team_photo')
        # if item['images'][0]['path']:
        #     new_image_name = item['Name'][0] + '.png'
        #     new_image_path = 'full/' + new_image_name

        #     os.rename(item['images'][0]['path'], new_image_path)
        pass
        