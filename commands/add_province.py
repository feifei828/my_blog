# coding=utf-8

from django.core.management import BaseCommand
from article.models import Province


class Command(BaseCommand):

    def handle(self, *args, **options):
        provinces = ['安徽', '澳门', '北京市', '重庆省', '福建', '甘肃', '广东', '广西', '贵州', '海南省', '河北',
                     '黑龙江', '河南', '湖北', '湖南', '江苏', '江西', '吉林省', '辽宁', '内蒙古', '宁夏', '青海',
                     '山东', '上海市', '山西', '陕西', '首尔市', '四川', '台湾', '天津市', '香港', '新疆', '西藏',
                     '云南', '浙江',
                     ]
        for province in provinces:
            p = Province.objects.create(province_name=province)
            p.save()
            print(province)
