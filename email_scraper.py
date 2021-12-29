#!/usr/bin/env python3
# coding=utf-8
# ******************************************************************
# Email Scraper - a small Python base tool to grab some emails from a URL.
# Author:
# Yesspider (Y3$_$pider)
# 
# ******************************************************************




from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# logo , auther_name and tool discription

print ()

print (f"{Fore.CYAN}******************************************************************")
print ("Email Scraper - a small Python base tool to grab some emails from a URL.")
print ('\033[31m' + "Author:")
print (" **//** Yesspider **//** ")
print ('''
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
░░░████▌█████▌█░████████▐▀██▀             
░▄█████░█████▌░█░▀██████▌█▄▄▀▄       
░▌███▌█░▐███▌▌░░▄▄░▌█▌███▐███░▀      *  Email Scraper By Y3$_$pider *
▐░▐██░░▄▄▐▀█░░░▐▄█▀▌█▐███▐█
░░███░▌▄█▌░░▀░░▀██░░▀██████▌
░░░▀█▌▀██▀░▄░░░░░░░░░███▐███
░░░░██▌░░░░░░░░░░░░░▐███████▌
░░░░███░░░░░▀█▀░░░░░▐██▐███▀▌
░░░░▌█▌█▄░░░░░░░░░▄▄████▀░▀
░░░░░░█▀██▄▄▄░▄▄▀▀▒█▀█░
	''')

print (f"{Fore.CYAN}******************************************************************")
print ("")



# Getting URL and s

user_url=str(input(f'{Fore.CYAN}[+]Enter Target URL to Scan [https://example.com] : '))
urls = deque([user_url])

scrapped_urls= set()
emails = set()

count = 0
try:
	while len(urls):
		count += 1
		if count == 10:

			break
		url = urls.popleft()
		scrapped_urls.add(url)

		parts=urllib.parse.urlsplit(url)
		base_url = '{0.scheme}://{0.netloc}' . format(parts)

		path=url[:url.rfind('/')+1] if '/' in parts.path else url
		print('[%d] Processing %s' % (count, url))
		
		try:
			response = requests.get(url)	

		except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
			continue

		new_emails = set(re.findall(r'[a-z0-9\. \-+_]+@[a-z0-9\. \-+_]+\.[a-z]+', response.text,re.I))
		emails.update(new_emails)

		soup = BeautifulSoup(response.text, features="lxml")

		for anchor in soup.find_all("a"):
			link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
			if link.startswith('/'):
				link = base_url+ link
			elif not link.startswith('http'):
				link = path + link
			if not link in urls and not link in scrapped_urls:
				urls.append(link)

except KeyboardInterrupt:
	print('[-] Closing!')

print("")
print(f"{Fore.RED}##################" + f"{Fore.CYAN} Emails :" + f"{Fore.RED}###################### ")
print("")

for mail in emails:
	print(mail)

print('')

