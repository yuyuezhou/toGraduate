import requests
import re
import time




# #设定爬虫目标网址
# #url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=630501735136&spuId=1880913130&sellerId=2891951486&order=3&currentPage=1&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvJQvUvbpvUpCkvvvvvjiWR2dpzjDnRLcwQjrCPmPUQj1nPLc90jDWPLMygjE8R29Cvvpvvvvv29hvCvvvMMGvvpvVvvpvvhCvKvhv8vvvvvCvpvvvvvmCC6Cvmh%2BvvvWvphvW9pvvvQCvpvs9vvv2vhCv2RmUvpvVmvvC9jDvuvhvmvvv9bGXNrN4mvhvLv3EdvvjXUcnDOvXVjIUDajxALwpEcqOaNLU5itYVVzwafm65kx%2F0jcG6Ek4ahqhAW2veBO0747B9Wma%2BoHoDO2U1C6tExjxAfev%2Bu0evpvhvvmv99%3D%3D&needFold=0&_ksTS=1646472461529_1260&callback=jsonp1261'
# #伪装
headers = {
    #从哪个页面发出的数据申请，每个网站可能略有不同
    'referer':'https://detail.tmall.com/item.htm?spm=a230r.1.14.11.749157e1xrtFbX&id=630501735136&ns=1&abbucket=10&sku_properties=5919063:6536025',
    #用的哪个浏览器
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    #哪个用户想看数据，是游客还是注册用户，建议使用登陆后的cookie
    'cookie':'hng=CN%7Czh-CN%7CCNY%7C156; lid=theuniqueyyz; cna=UNRZGgpIuwkCAXWEB+RHGJxe; enc=EK%2BcBvCH0idz0yHLxAonDY1ounS5m2UeMtDA%2Fc6kmR61P88IybRbPxWKbyQy%2BZaZuNYbFffluWQPyazsihkQ1g%3D%3D; dnk=theuniqueyyz; uc1=cookie21=UIHiLt3xThH8t7YQoFNq&existShop=false&cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie14=UoewBj6ekpMngw%3D%3D&pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D; uc3=lg2=VFC%2FuZ9ayeYq2g%3D%3D&nk2=F55vgTi3VDr5AV4b&id2=VyyX56UFD4kH6w%3D%3D&vt3=F8dCvUFhtmcG0pdAxFQ%3D; tracknick=theuniqueyyz; uc4=nk4=0%40FYREPL3vyQd5c82y%2F1yYHufhrq9wA5I%3D&id4=0%40VXtYi81shZoWMtCKMYi6Q8vJ8l4u; _l_g_=Ug%3D%3D; unb=4061607594; lgc=theuniqueyyz; cookie1=AVIm2cGT134PJZHx0daAhvTaw%2F7YfwLji12bdGINnQg%3D; login=true; cookie17=VyyX56UFD4kH6w%3D%3D; cookie2=18e80d27e9542e2f96fd07347574bd66; _nk_=theuniqueyyz; sgcookie=E100qxuBGF4CGiPGwbArIYNEjGN9bfjdlW8Ezrngt0wYOJL0k42VTOcmyY63rdNo%2FhPX6OYDQ%2BHhUZ80EfzUQsTxP89Ggyj61GlRTGJGiEjN6GEotqPDmsJzLk7Lh9FCAwD%2B; cancelledSubSites=empty; t=bb9e435455b538343ec0be98128b1481; sg=z4e; csg=736d0983; _tb_token_=5e7485eb34358; xlly_s=1; x5sec=7b22617365727665723b32223a226361333630323739346235386334613964366666366361356665343135333233434b44546a4a4547454c485371656d6b7a2b365470414561444451774e6a45324d4463314f5451374d5443756f66474e41673d3d227d; tfstk=co2RBpN_YZbluNoYb7C0Rt46jb2dZ8---3gppic_iEyRF2pdii2gBrCGNDuZyiC..; l=eBg1suAggVyqwEGwBOfanurza77OSIRYSuPzaNbMiOCPO2f654FAW6mmTsLBC3GVh6JvR3lrOrBaBeYBqnV0x6aNa6Fy_Ckmn; isg=BIeH7JTMqT2InS5PDNhhJg6XFjtRjFtuzmuAm1l0o5Y6yKeKYVzrvsWOaoiWJTPm',
}
# data = requests.get(url,headers = headers).text
#
# #通过正则提取评论
#     #发现规律-套路-->搞一个匹配规则出来：
#     #即 "rateContent":"想要的评论内容","fromMall"
# data=re.findall('"rateContent":"(.*?)","fromMall"',data)

#临时保存
texts = []
#获取更多页的评论 ==>通过改变评论url中的页码数 currentPage代表当前页数
for n in range(90,100):
    #url2 = 'https://rate.tmall.com/list_detail_rate.htm?itemId=520695230261&spuId=344103112&sellerId=201749140&order=3&currentPage='+str(n)+'&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvepvPvBvvUvCkvvvvvjiWR2z9tj3nR2sh6jYHPmPy6j38n25hljiERsMOQjiW9vhv2HifnNMSzHi47eIgzTQCvvyvmCmmXeOvnm%2F%2BvpvBUvFi99hCv2Ly84%2F9nh2ExLV%2BvpvEvvQ995B6vm1VRvhvCvvvvvvRvpvhvv2MMT9Cvv9vvUvMmjPh1U9CvvOUvvVvJZ%2FgvpvIvvvvvhCvvvvvvUhSphvUoQvvvQCvpvACvvv2vhCv2RvvvvWvphvWgv9CvhQv5j9vCAKDYWsWeX1%2BVd0DyOvO5onmsX7v1CyaWDNBlwethbUf8KBld8Q7rjlH0WFh%2B2Kz8Z0vQRAn%2BbyDCwLWTWeARFxjKOmxfBkKvvhvC9vhvvCvp8OCvvpvvUmm39hvCvvhvvm%2BvpvEvvLOvIeEv2FoRvhvCvvvvvv%3D&needFold=0&_ksTS=1641893544641_535&callback=jsonp536'
    #不能爬太快 容易暴露 -->增加延时
    url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=630501735136&spuId=1880913130&sellerId=2891951486&order=3&currentPage='+str(n)+'&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvJQvUvbpvUpCkvvvvvjiWR2dpzjDnRLcwQjrCPmPUQj1nPLc90jDWPLMygjE8R29Cvvpvvvvv29hvCvvvMMGvvpvVvvpvvhCvKvhv8vvvvvCvpvvvvvmCC6Cvmh%2BvvvWvphvW9pvvvQCvpvs9vvv2vhCv2RmUvpvVmvvC9jDvuvhvmvvv9bGXNrN4mvhvLv3EdvvjXUcnDOvXVjIUDajxALwpEcqOaNLU5itYVVzwafm65kx%2F0jcG6Ek4ahqhAW2veBO0747B9Wma%2BoHoDO2U1C6tExjxAfev%2Bu0evpvhvvmv99%3D%3D&needFold=0&_ksTS=1646472461529_1260&callback=jsonp1261'
    time.sleep(3)
    data = requests.get(url, headers=headers).text
    data = re.findall('"rateContent":"(.*?)","fromMall"', data)
    texts.extend(data)
    print('爬完了第'+str(n)+'页')
print(texts)

#本地文件保存
import xlwt
import pandas as pd
#创建一个空的数据表
df = pd.DataFrame();
#创建一个列 此列的每行都是texts列表中的一个元素
df['评论'] = texts
print(df)
#存为excel
df.to_excel('F:\ToGraduate\毕设\Data\淘宝笔记本电脑评论数据\淘宝笔记本电脑评论数据90-100页.xls')
#存为csv
#df.to_csv('F:\ToGraduate\Data\淘宝微波炉评论数据\淘宝微波炉评论数据final.csv',encoding='utf-8')

print("爬取完成")