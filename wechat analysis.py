# -*- coding: utf-8 -*-

import numpy as np
import itchat
import matplotlib.pyplot as plt

itchat.login()

friends = itchat.get_friends(update=True)[0:]



male = female = other = 0
for i in friends[1:]:
	sex = i['Sex']
	if sex == 1:
		male += 1
	elif sex == 2:
		female += 1
	else:
		other += 1
total = len(friends[1:])
print(
	"male friend: %.2f%%" % (float(male)/total * 100) + "\n" +
	"female friend: %.2f%%" % (float(female)/total * 100) + "\n" +
	"unidentified gender friend: %.2f%%" % (float(other)/total * 100)
	)

label_name = ["Boy", "Girl", "Unknown"]
gender_list = [male, female, other]
plt.figure()
plt.bar(range(len(gender_list)), gender_list, tick_label=label_name)

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

plt.xlabel(u'gender')
plt.ylabel(u'number of people')
plt.title(u'Friends Gender Ratio')


x=np.arange(3)
y=np.array(gender_list)
for a,b in zip(x,y):
	plt.text(a, b+0.1, '%.2f' % b, ha='center', va= 'bottom',fontsize=12)



def get_var(var):
	variable = []
	for i in friends[1:]:
		value = i[var]
		variable.append(value)
	return variable
NickName = get_var("NickName")
Sex = get_var("Sex")
Province = get_var("Province")
City = get_var("City")
Signature = get_var("Signature")

from pandas import DataFrame
data = {"NickName": NickName, "Sex": Sex, "Province": Province,
	"City": City, "Signature": Signature}
frame = DataFrame(data)
frame.to_csv('data.csv', encoding='utf_8_sig', index=True)


city_dict = {}
x_city = []
y_city = []
for city_name in City:
	if city_name in city_dict:
		city_dict[city_name] += 1
	else:
		city_dict[city_name] = 1
city_list = sorted(city_dict.items(), key=lambda item:item[1], reverse=True)
# print city_list
for i in city_list[1:15]:
	x_city.append(i[0])
	y_city.append(i[1])


plt.figure()
plt.bar(range(len(x_city)), y_city, tick_label=x_city)
plt.xlabel(u'city')
plt.ylabel(u'number of people')
plt.title(u'City distribution of friends')

x=np.arange(len(x_city))
y=np.array(y_city)
for a,b in zip(x,y):
	plt.text(a, b+0.06, '%.2f' % b, ha='center', va='bottom', fontsize=9)



import re 
Signature_list = []
for i in friends:
	signature = i["Signature"].strip().replace("span", "").replace("class", "").replace("emoji", "")
	rep = re.compile("lf\d+\w*|[<>/=]")
	signature = rep.sub("", signature)
	Signature_list.append(signature)
text = "".join(Signature_list)

import jieba 
wordlist = jieba.cut(text, cut_all=False)
word_space_split = " ".join(wordlist)


from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image

coloring = np.array(Image.open("weixin_sj520_33.jpg"))
my_wordcloud = WordCloud(background_color="white", max_words=200,
	mask=coloring, max_font_size=70, random_state=42, scale=2,
	font_path="C:\Windows\Fonts\SimHei.ttf").generate(word_space_split)
image_colors = ImageColorGenerator(coloring)
plt.figure()
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
