import web
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import pandas as pd
import numpy
from pandas import DataFrame
from scipy import stats 
from pandas.io.json import json_normalize
import json
import requests


urls = (
  '/', 'hello')

app = web.application(urls, globals(), True)

render = web.template.render('templates/')

class hello:
    def GET(self):
	co=0
	co=0
	nh3=0
	no2=0
	dp=0
	so2=0
	# feed1=requests.get('https://api.thingspeak.com/channels/31959/feeds.json')
	# feed=feed1.json()
	data_file=open('feeds.json')   
	feeds= json.load(data_file)
	# feeds=feed['feeds']
	df=json_normalize(feeds)

	df1=df.tail(582)
	df1.created_at = dt.date2num(pd.to_datetime(df1.created_at))
	df1.field1=df1.field1.astype(float)
	df1.field2=df1.field2.astype(float)
	df1.field3=df1.field3.astype(float)
	df1.field4=df1.field4.astype(float)
	df1.field5=df1.field5.astype(float)

	df1.field1=df1.field1.replace('-1',df1.field1.mean())
	df1.field2=df1.field2.replace('-1',df1.field2.mean())
	df1.field3=df1.field3.replace('-1',df1.field3.mean())
	df1.field4=df1.field4.replace('-1',df1.field4.mean())
	df1.field5=df1.field5.replace('-1',df1.field5.mean())

	a=df1["created_at"].count()
	treatment1=df1[["field1","field2","field3","field4","field5"]].tail(48)
	treatment2=df[["field1","field2","field3","field4","field5"]].ix[a-96:a-48]
	plt.figure(figsize=(12, 14)) 
	ax = plt.subplot(111)  
	
	ax.spines["top"].set_visible(False)  
	ax.spines["right"].set_visible(False)  


	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()  

	plt.ylabel('Parts Per Million',fontsize=16)
	plt.xlabel('Previous 2 Days',fontsize=16)
	plt.plot_date(df1.created_at.tail(96),df1.field1.tail(96),'b-', label="Carbon Monoxide")
	plt.plot_date(df1.created_at.tail(96),df1.field2.tail(96),'r-',label="Ammonia")
	plt.plot_date(df1.created_at.tail(96),df1.field3.tail(96),'g-',label="Nitrogen Oxide")
	plt.plot_date(df1.created_at.tail(96),df1.field4.tail(96),'y-',label="Coarse Dust Particle")
	plt.plot_date(df1.created_at.tail(96),df1.field5.tail(96),'m-',label="Sulphur di-oxide")
	plt.legend(bbox_to_anchor=(.5, 1), loc=2, borderaxespad=0.)
	plt.draw()


	# disp=plt.savefig('disp.jpeg')
	# fout=open(plt.savefig('disp.png'),'w')
	#filedir = '/path/where/you/want/to/save'

	z_stat, p_val_field1 = stats.ranksums(treatment1["field1"], treatment1["field1"]) 
	if (p_val_field1>0.05):
		co=1
	z_stat_field2, p_val_field2 = stats.ranksums(treatment1["field2"], treatment2["field2"]) 
	if (p_val_field2>0.05):
		nh3=1
	z_stat_field3, p_val_field3 = stats.ranksums(treatment1["field3"], treatment2["field3"])
	if (p_val_field3>0.05):
		no2=1
	z_stat_field4, p_val_field4 = stats.ranksums(treatment1["field4"], treatment2["field4"]) 
	if (p_val_field4>0.05):
		dp=1
	z_stat_field5, p_val_field5 = stats.ranksums(treatment1["field5"], treatment2["field5"]) 
	if (p_val_field5>0.05):
		so2=1

	plt.show()

        return render.Display(df1.field1.min(),df1.field1.mean(),df1.field1.max(),
				df1.field2.min(),df1.field2.mean(),df1.field2.max(),
				df1.field3.min(),df1.field3.mean(),df1.field3.max(),
				df1.field4.min(),df1.field4.mean(),df1.field4.max(),
				df1.field5.min(),df1.field5.mean(),df1.field5.max(),
				co,nh3,no2,dp,so2)

	


if __name__ == "__main__":
    app.run()
