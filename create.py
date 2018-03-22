from installer import*

dependencies = 'requests,selenium'.split(',')
i  = Installer(dependencies=dependencies)
i.load()

import requests
import json
import os
from utils import *
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime


def openSelenium(session,url,driver):
	driver.get(url)
	for c in session.cookies:
		driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})
	driver.get(url)

def debug(filename,text):
	newName = 'debugging/{} | {}.{}'.format(filename.split('.')[0],datetime.now().ctime(),filename.split('.')[-1])
	with open(newName, 'w+') as test:
		test.write(text)
	test.close()

def selenium2Req(driver,session):
	for cookie in driver.get_cookies():
		session.cookies.set(cookie['name'], cookie['value'])

def main():
	log('Starting...')
	loggedin = False
	s = requests.session()

	headers = {
		'Accept':'application/json, text/plain, */*',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.9',
		'Connection':'keep-alive',
		'Content-Type':'application/json;charset=UTF-8',
		'Host':'privacy.com',
		'Origin':'https://privacy.com',
		'Referer':'https://privacy.com/login',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
	}
	log('Getting Session ID')
	b = s.post("https://privacy.com/login", headers=headers)
	cookies = s.cookies.get_dict()
	sessionid = cookies["sessionID"]
	headers["Cookie"] = 'sessionID={}; abtests=%5B%7B%22name%22%3A%22extension-install-test%22%2C%22value%22%3A%22signup-step%22%7D%5D; landing_page=main'.format(sessionid)

	# log('Session ID: ' + sessionid)
	log('Logging in')
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-gpu")
	driver = webdriver.Chrome(chrome_options=chrome_options)
	openSelenium(s,'https://privacy.com/login',driver)
	driver.find_element_by_name("email").send_keys(email)
	driver.find_element_by_name("password").send_keys(passw)
	driver.find_element_by_name("submit").click()

	#check for 60s to see if login succeeded
	for i in range(0,20):
		token = driver.get_cookie('token')
		if token != None:
			loggedin = True
			break
		else:
			log('Logging in.. This may take a while.')
			time.sleep(3)

	if loggedin == False:
		log('Failed to login')
		exit()
	else:
		log('Succesfully Logged in')

	selenium2Req(driver,s)
	token = s.cookies.get_dict()['token']
	headers["Authorization"] = 'Bearer ' + token
	headers["Cookie"] = 'sessionID={}; abtests=%5B%7B%22name%22%3A%22extension-install-test%22%2C%22value%22%3A%22signup-step%22%7D%5D; landing_page=main; ETag="ps26i5unssI="; token={}'.format(sessionid, token)
	driver.close()

	for i in range(int(num)):
		log('Creating card #' + str(i))
		url = "https://privacy.com/api/v1/card"

		payload1 = {
			"reloadable":'true',
			"spendLimitDuration":"MONTHLY",
			"memo": 'CardGen ' + str(i),
			"meta":{"hostname":""},
			"style":'null'}

		r = s.post(url, data=json.dumps(payload1), headers=headers)

		if r.status_code == 200:
			card = r.json()
			number = card["card"]["pan"]
			expdate = card["card"]["expMonth"] + "/" + card["card"]["expYear"]
			cvv = card["card"]["cvv"]
			f = open("cards.txt", "a+")
			f.write("{} | {} | {}\n".format(number, expdate, cvv))
			f.close()
			cLog("Created Card: {} | {} | {}".format(number,expdate,cvv), "green")

		else:
			cLog("ERROR CREATING CARD", "red")
			print(r.status_code,r.text)

	log('Cards written to cards.txt')

def init():
	global num
	global email
	global passw

	num = int(input('Number of cards to create: '))
	email = input("Privacy account email ")
	passw = input("Privacy account password: ")

	os.remove("cards.txt")
	f = open("cards.txt", "w+")
	f.close()

if __name__ == '__main__':
	print("\n---------------------------")
	print('Privacy Card Generator')
	print("Made by Anton Lin")
	print("www.github.com/antonjlin")
	print("---------------------------\n")
	init()
	main()
