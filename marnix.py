import requests
import string
import random
import json
import time
import multiprocessing


with open("http_proxies.txt", "r") as readr:

	all_proxies = readr.readlines()

class myAccGen:

	def __init__(self, userId, proxies):

		self.s = requests.Session()
		self.bot_userId = userId
		self.proxy = {'http': random.choice(all_proxies)}
		

	def main(self):

		n_letters = random.randint(6, 9)
		usrname = "".join([random.choice(string.ascii_letters) for x in range(n_letters)])
		pwd = 'Wollah123'

		payload = {"deviceName":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61",
		"deviceLocale":"nl",
		"country":"nl",
		"timezone":"-2",
		"deviceUuid":"18b766ff-4aa0-4a8d-bcc1-86b5ecd561b4",
		"deviceType":3,"email":f"{usrname}@gmail.com",
		"userName":f"{usrname}","password":f"{pwd}"}

		payloadauth = {"password":pwd, "userName":usrname,
		"deviceName":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61",
		"deviceLocale":"nl","country":"nl","timezone":"-2","deviceUuid":"18b766ff-4aa0-4a8d-bcc1-86b5ecd561b4","deviceType":3}

		url = 'https://api-v2.medal.tv/users'
		re = self.s.options(url, allow_redirects = True )
		re = self.s.post(url, allow_redirects = True, data=json.dumps(payload) )
		jsonid = json.loads(re.text)

		try:
			self.userid = jsonid['userId']
		except KeyError:

			print(jsonid)
		re = self.s.post('https://api-v2.medal.tv/authentication', allow_redirects = True, data=json.dumps(payloadauth), proxies=self.proxy )
		re = self.s.post('https://api-v2.medal.tv/authentication', allow_redirects = True, data=json.dumps(payloadauth), proxies=self.proxy )

		jsonkey = json.loads(re.text)
		key = jsonkey["key"]


		re = self.s.options('https://api-v2.medal.tv/ref/complete', allow_redirects = True, proxies=self.proxy )

		re = self.s.post(f'https://firestore-auth.medal.tv/http/authenticate', allow_redirects = True, data =json.dumps({"id":self.userid,"key":key}), proxies=self.proxy)
		tokenjson = json.loads(re.text)
		token = tokenjson["token"]
		tokenpayload = {"token":token,"returnSecureToken":True}






		re = self.s.post(f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key=AIzaSyDiNjNw-pqWw0nNhRaE5lQnmeeym_1s-Fk', allow_redirects = True, data = json.dumps(tokenpayload), proxies=self.proxy)


		jsonnewtoken = json.loads(re.text)
		newtoken = jsonnewtoken['idToken']
		re = self.s.post(f'https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key=AIzaSyDiNjNw-pqWw0nNhRaE5lQnmeeym_1s-Fk', allow_redirects = True, data = json.dumps({"idToken": newtoken}), proxies=self.proxy)

		#print(re.status_code)
		self.header = {

		'x-authentication': f"{self.userid},{key}"}
		re = self.s.get(f'https://api-v2.medal.tv/content?userId={self.userid}&limit=5&offset=10')
		re = self.s.get(f'https://www.google-analytics.com/collect?v=1&_v=j83&a=140313294&t=event&_s=3&dl=https%3A%2F%2Fmedal.tv%2Fusers%2F8256421&ul=nl&de=UTF-8&dt=Evil%20Dodo%27s%20Latest%20Clips%20%26%20Gameplay%20Videos%20%7C%20Medal.tv&sd=24-bit&sr=1536x864&vp=1522x754&je=0&ec=video&ea=started&el=web-desktop&_u=SACAAUAB~&jid=&gjid=&cid=287247206.1594994279&uid=8256220&tid=UA-101634769-1&_gid=154559052.1594994279&z=1716219762', allow_redirects=True, proxies=self.proxy)
		re = self.s.get(f'https://www.google-analytics.com/collect?v=1&_v=j83&a=140313294&t=event&_s=4&dl=https%3A%2F%2Fmedal.tv%2Fusers%2F8256421&ul=nl&de=UTF-8&dt=Evil%20Dodo%27s%20Latest%20Clips%20%26%20Gameplay%20Videos%20%7C%20Medal.tv&sd=24-bit&sr=1536x864&vp=1522x754&je=0&ec=video&ea=viewcount&el=web-desktop&_u=SACAAUAB~&jid=&gjid=&cid=287247206.1594994279&uid=8256220&tid=UA-101634769-1&_gid=154559052.1594994279&z=1186892192', allow_redirects=True, proxies=self.proxy)
		re = self.s.post(f'https://api-js.mixpanel.com/track/?ip=1&_=1595003635993', allow_redirects=True, data ='eyJldmVudCI6ICJmb2xsb3dVc2VyIiwicHJvcGVydGllcyI6IHsiJG9zIjogIldpbmRvd3MiLCIkYnJvd3NlciI6ICJNaWNyb3NvZnQgRWRnZSIsIiRjdXJyZW50X3VybCI6ICJodHRwczovL21lZGFsLnR2L3VzZXJzLzgwNTQ0NjYiLCIkYnJvd3Nlcl92ZXJzaW9uIjogODMsIiRzY3JlZW5faGVpZ2h0IjogODY0LCIkc2NyZWVuX3dpZHRoIjogMTUzNiwibXBfbGliIjogIndlYiIsIiRsaWJfdmVyc2lvbiI6ICIyLjM4LjAiLCIkaW5zZXJ0X2lkIjogImRxZzk1eGxyd2E1eXp5ZjgiLCJ0aW1lIjogMTU5NTAwMzYzNS45OTIsImRpc3RpbmN0X2lkIjogODI1NjIyMCwiJGRldmljZV9pZCI6ICIxNzM1ZDExMzA2MTJlNy0wOGUzYzkxM2ZjZWEwMS03OTY1N2E2MC0xNDQwMDAtMTczNWQxMTMwNjIyMmIiLCIkc2VhcmNoX2VuZ2luZSI6ICJnb29nbGUiLCIkaW5pdGlhbF9yZWZlcnJlciI6ICJodHRwczovL3d3dy5nb29nbGUuY29tLyIsIiRpbml0aWFsX3JlZmVycmluZ19kb21haW4iOiAid3d3Lmdvb2dsZS5jb20iLCIkdXNlcl9pZCI6IDgyNTYyMjAsInBsYXRmb3JtIjogIndlYi1kZXNrdG9wIiwiZnJvbSI6ICJ3ZWItcHJvZmlsZS1wYWdlIiwiY2F0ZWdvcnlOYW1lIjogImNzOmdvIiwidG9rZW4iOiAiMDY3YjUxZDljMWNkODcyNzYzMDU3OGFjMDYzNDlhOTQifX0=',proxies=self.proxy )

	def follow(self):

		
		followPayload = {"followingId":self.bot_userId,"action":"follow","from":f"/users/self.bot_userId","categoryName":"CS:GO"}
		re = self.s.options(f'https://api-v2.medal.tv/users/{self.userid}/following', allow_redirects=True, proxies=self.proxy)
		re = self.s.post(re.url, allow_redirects=True, data = json.dumps(followPayload), headers=self.header, proxies=self.proxy)
		#print(re.status_code)

	def like(self, videos):

		likePayload = {"action":"like","userId":self.bot_userId}
		

		for video in videos:

			likeurl = f"https://api-v2.medal.tv/content/{video}/likes"

			re = self.s.post(likeurl, allow_redirects=True, data = json.dumps(likePayload), headers=self.header, proxies=self.proxy)
		
		

	def view(self, videos):

		for video in videos:
			url = f"https://api-v2.medal.tv/content/{video}/views"
			re = self.s.post(url, headers=self.header, proxies=self.proxy)

		print(re.status_code)




def accProcess(userId, videos, proxies):
	
	try:
		firsttime = time.time()
		tempuser = myAccGen(userId, proxies) 
		tempuser.main()
		tempuser.follow()
		tempuser.like(videos)
		tempuser.view(videos)

	except (ConnectionError, requests.exceptions.ConnectionError) as e:

		print("Exception handled: ", e)



def main(userId, videos, proxies, maxProcess=20):

	i = 0

	while True:

		
		print(i)
		
		processes = []

		for _ in range(maxProcess):

			p = (multiprocessing.Process(target=accProcess, daemon=True, args=[userId, videos, proxies]))
			p.start()
			processes.append(p)

		for process in processes:

			process.join()
		
		i+=1



if __name__ == '__main__':

	videos = ['30978511', '30978598']
	userid = 8797500 #ID of the user you want to bot
	main( userid, videos,maxProcess = 10)
	'''
	while True:
		accProcess(userid, videos, all_proxies)
	'''