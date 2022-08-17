import argparse
import json
from pickle import FALSE
import requests
import signal
import sys
import time
from colorama import Fore, init

init()
def menu(): 
 print(Fore.LIGHTBLUE_EX + """

       ____  _        _    ____ _  __  ____  _____ _____ _  _______ ____       
      | __ )| |      / \  / ___| |/ / / ___|| ____| ____| |/ / ____|  _ \     
      |  _ \| |     / _ \| |   | ' /  \___ \|  _| |  _| | ' /|  _| | |_) |     
      | |_) | |___ / ___ \ |___| . \   ___) | |___| |___| . \| |___|  _ <    
      |____/|_____/_/   \_\____|_|\_\ |____/|_____|_____|_|\_\_____|_| \_\     
                                                                       
   BLACK SEEKER is an OSINT tool based on url requests created by: @Clideus. Enjoy!                                         		                                                             
                                                                    """)

parser = argparse.ArgumentParser()
add_help=True
parser.add_argument("-u", "--username", type=str, metavar='USERNAME', help="Search a username on all sites list.")
parser.add_argument("-ip", type=str, metavar='IP', help="Locate an IP adress.")
parser.add_argument("-o", "--onlyok", action='store_true', default=FALSE, help="Show the OK responses only. This will hide NOT FOUND responses.")
parser.add_argument("-sn", "--socialnetworks", type=str, metavar='USERNAME', help="Search for social networks only. DO NOT USE: -sn -u [username]." )


menu()
socialnetworks_list = [
"https://www.twitter.com/",
"https://vsco.co/",
"https://www.instagram.com/",
"https://www.onlyfans.com/",
"https://www.tiktok.com/",
"https://www.snapchat.com/",
"https://www.facebook.com/",
"https://pinterest.com/",
"https://reddit.com/",
"https://vk.com/",
"https://twitch.tv/",
"https://discord.com/",
"https://soundcloud.com/",
"https://linkedin.com/"]

notfound = Fore.RED+ "[-] NOT FOUND: %s" 
found = Fore.LIGHTGREEN_EX + "[*] GOAL!: %s"
possible = Fore.YELLOW + "[?] POSSIBLE CONNECTION: %s"
iperror = Fore.LIGHTRED_EX + "[-] ERROR: COULD NOT CONNECT TO IP TRACKER API."

def search():
 with open("sites.md","r") as sites:
   lines = sites.readlines()
   for site in lines:
          userurl = "%s%s" % (site.rstrip(),target_user)
          session = requests.Session() 
          response = session.get(userurl, allow_redirects=True, verify=None)
          if response.status_code == 200:
             print (possible % userurl)
          else:
            if (response.status_code == 404 or 504) and (args.onlyok == FALSE):
             print (notfound % userurl) 
   sites.close()

def social():
   if (args.socialnetworks) :
      for social in socialnetworks_list:
          userurl = "%s%s" % (social,target_user)
          response = requests.get(userurl,allow_redirects=True) 
          if response.status_code == 200 :
             print (possible % userurl)
          elif (args.onlyok == FALSE):
             print (notfound % userurl)  
             
def ipsearch():
   url = ("http://ip-api.com/json/")
   stat = requests.get(url,allow_redirects=False)
   if (stat.status_code == 200):
       input_ip = requests.get(url + target_ip)
       data = input_ip.text
       api = json.loads(data)

       #results variables:
       ip = "IP: "+(target_ip)
       isp = "ISP: "+(api["isp"])
       country = "COUNTRY: "+(api["country"])
       timezone = "TIMEZONE: "+(api["timezone"]) 
       region = "REGION: "+(api["regionName"])+" - "+(api["zip"])
       city = "CITY: "+(api["city"])

       resultlist = [
         ip + "\n", 
         isp + "\n \r", 
         country + "\n", 
         timezone + "\n \r", 
         region + "\n", 
         city+ "\n \r"]

       def ipresults():
         print(Fore.LIGHTGREEN_EX + "[*] GOAL!:")
         print()
         print(Fore.LIGHTCYAN_EX + ip)
         print(Fore.LIGHTCYAN_EX + isp)
         print() 
         print(Fore.LIGHTCYAN_EX + country)
         print(Fore.LIGHTCYAN_EX + timezone)
         print()
         print(Fore.LIGHTCYAN_EX + region)
         print(Fore.LIGHTCYAN_EX + city)
         print()
       ipresults()

       saveip=input("Do you want to create a log file? (y/n)...")
       if saveip=="y":
          logfile=open(target_ip + " log.txt","w")
          logfile.write("LOCATION IP LOG: \n \r")
          for lines in resultlist:
             logfile.writelines(lines) 
          logfile.close()          
   else:
       print(iperror)

def handler(signum,frame):
    exit = input("Do you really want to exit? y/n ")
    if exit == 'y':
       print(Fore.LIGHTCYAN_EX + "Thanks for using BLACK SEEKER!")
       time.sleep(1)
       sys.exit(1)
signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    args = parser.parse_args()
    onlyok_bool = FALSE
target_user = args.username or args.socialnetworks
target_ip = args.ip

if args.username:
    search()
if args.ip:
	 ipsearch()
if args.socialnetworks:
   social()
if len(sys.argv) == 1:
     parser.print_help()
