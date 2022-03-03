import requests
import time
import random
import json
import datetime

headers={
'content-type':'application/json;charset=UTF-8',
'User-Agent':'Mozilla/5.0 (Linux; Android 11; PCGM00 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120 MQQBrowser/6.2 TBS/045714 Mobile Safari/537.36 SuperApp',
}

class Report:
	def __init__(self,name,password,headers):
		self.name = name
		self.password = password
		self.headers = headers

	#登录获取token
	def login(self):
		url = 'https://token.haust.edu.cn/password/passwordLogin?username={}&password={}&appId=com.lantu.MobileCampus.haust&geo=&deviceId=YROsZ3RJzqcDAMlBISGiNHXZ&osType=android&clientId=1443ac9e0c3c529e08274c7fdf7faeb0'.format(self.name,self.password)
		ur = requests.post(url=url,headers=self.headers).json()
		id_token = ur['data']['idToken']
		headers['X-Id-Token'] = id_token
		self.headers = headers

	#获取历史记录id
	def id_get(self):
		end_time=datetime.datetime.now()
		enddate=(end_time+datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
		url='https://yqfkfw.haust.edu.cn/smart-boot/api/healthReport/queryUserHealthReport?date=%s'%(enddate)
		us=requests.get(url=url,headers=self.headers)
		code=us.status_code
		us=us.json()
		name_id=us['result']['reports'][0]['id']
		self.history_id = name_id


	#获取历史记录详情
	def grxx(self):
		inparam = {}
		nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		tw=random.uniform(35.5,36.0)
		tw=round(tw,1)
		url='https://yqfkfw.haust.edu.cn/smart-boot/api/healthReport/getReport?id=%s'%(self.history_id)
		us=requests.get(url=url,headers=self.headers)
		code=us.status_code
		us=us.json()
		result=us['result']
		inparam['address']=result['address']
		inparam['age']=str(result['age'])
		inparam['bodyTemperature']=float(tw)
		inparam['createTime'] = nowtime
		inparam['phone']=result['phone']
		inparam['isStayLocal']=result['isStayLocal']
		if result['latitude']:
			inparam['latitude']=result['latitude']
			inparam['longitude']=result['longitude']
		if 'firstVaccineDate' in result.keys():
			if result['lastVaccineDate']:
				inparam['firstVaccineDate']=result['firstVaccineDate']
				inparam['lastVaccineDate']=result['lastVaccineDate']
			elif result['firstVaccineDate']:
				inparam['firstVaccineDate']=result['firstVaccineDate']
			else:
				pass
		newparam={"vaccineType":1,"unusualSymptomList":[],"needUpdate":0}
		inparam.update(newparam)
		self.param = json.dumps(inparam)

	#报平安
	def bpa(self):
		while True:
			try:
				url = 'https://yqfkfw.haust.edu.cn/smart-boot/api/healthReport/saveHealthReport'
				us=requests.post(url=url,headers=self.headers,data=self.param)
				us=us.json()
				print(us)
				if(us['success']):
					self.text= "账号:********"+ str(self.name[8:]) +"今天上报情况："+ str(us['result'])+"\n"
				else:
					self.text= "账号:********"+ str(self.name[8:]) +"今天上报情况："+ str(us['success'])+"\n"
				break
			except:
				time.sleep(60*30)
		return self.text

		

def start(name,password):
	app = Report(name,password,headers)
	app.login()
	app.id_get()
	app.grxx()
	app.bpa()

def run():
	name=""
	password=""
	start(name,password)

run()