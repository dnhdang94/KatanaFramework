#
# Katana framework 
# @Katana Ping functions
#

import readline, rlcompleter
from scapy.all import *
import xml.etree.ElementTree as ET
from xml.dom import minidom
import StringIO
import fcntl, socket, struct
import logging
import urllib
import re
import colors
import socket
import time 
import commands   
import subprocess
import Setting
import sys                   


ap_list = []
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

### PING ###
def live(defaulthost, defaultport):
	red=socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
	red.connect((defaulthost, int(defaultport))) 
	red.close()

### LOG's ###
def save(module, target, port, dat1, dat2):
	log=open('core/logs/logsBruteForce.log','a')
	log.write('\n ===================================== ')
	log.write('\n Module  : '+module)
	log.write('\n Data    : '+time.strftime('%c'))
	log.write('\n target  : '+target)
	log.write('\n port    : '+port)
	log.write('\n Cracked : username : '+dat1+' , password : '+dat2)
	log.close()
def savetwo(module, files, password):
	log=open('core/logs/logsBruteForce.log','a')
	log.write('\n ===================================== ')
	log.write('\n Module  : '+module)
	log.write('\n Data    : '+time.strftime('%c'))
	log.write('\n file    : '+files)
	log.write('\n Cracked : password : '+password)
	log.close()
def savethree(module,target,port,patch,username,password):
	log=open('core/logs/logsBruteForce.log','a')
	log.write('\n ===================================== ')
	log.write('\n Module  : '+module)
	log.write('\n Data    : '+time.strftime('%c'))
	log.write('\n target  : '+target)
	log.write('\n port    : '+port)
	log.write('\n Patch   : '+patch)
	log.write('\n Cracked : username: '+username+', password : '+password)
	log.close()
def savefour(module,target,port,patch,method,dat1,dat2,username,password):
	log=open('core/logs/logsBruteForce.log','a')
	log.write('\n ===================================== ')
	log.write('\n Module  : '+module)
	log.write('\n Data    : '+time.strftime('%c'))
	log.write('\n target  : '+target)
	log.write('\n port    : '+port)
	log.write('\n Patch   : '+patch)
	log.write('\n Cracked : '+dat1+':'+username+', '+dat2+':'+password)
	log.close()
def savefive(module,target,port,results):
	log=open('core/logs/logsAdminFinder.log','a')
	log.write('\n ===================================== ')
	log.write('\n Module  : '+module)
	log.write('\n Data    : '+time.strftime('%c'))
	log.write('\n target  : '+target)
	log.write('\n port    : '+port)
	log.write('\n Found   : '+results)
	log.close()
def PacketHandler(pkt):
  if pkt.haslayer(Dot11) :
		if pkt.type == 0 and pkt.subtype == 8 :
			if pkt.addr2 not in ap_list :
				ap_list.append(pkt.addr2)
				print " BSSID: %s \t ESSID: %s " %(pkt.addr2, pkt.info)

### AP's ###
def scanwifi():
	print " Scanning APs - "+colors.O+"Ctrl+C"+colors.W+" for Stop.\n"
	sniff(iface="mon0", prn = PacketHandler)

### MY LOCAL IP ### 
def myip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try: 
		s.connect(("google.com",80))
		if True:
			ip=s.getsockname()[0]
			s.close()
			return ip
	except:
		s.close()
		return False

### GET EXTANAL IP ###
def get_external_ip():
	try:	
	    site = urllib.urlopen("http://checkip.dyndns.org/").read()
	    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
	    address = grab[0]
	    if True:
	    	print(" You Public IP: "+address+"\n")
	except:
		print " ["+colors.R+"-"+colors.W+"] Not Connect to nothing Network.\n"

### INTERFACES SCANNING ###
def interfaces(output):
	Interfaces=commands.getoutput("airmon-ng | grep 'wlan' | awk '{print $1}'")
	Interfaces=Interfaces.replace("\n",",")
	if output==1:
		if Interfaces=="":
			Interfaces="Interfaces  : No network cards was found."
		else:
			print " Interfaces : ",Interfaces

### GET MONITORS ###
def monitor():
	Monitor=commands.getoutput("airmon-ng | grep 'mon' | awk '{print $1}'")
	Monitor=Monitor.replace("\n",",")
	if Monitor=="":
		Monitor="No monitor mode enabled, use 'start {Interface}' right here."
	print " Int... Monitor  : ",Monitor
	if Monitor!="No monitor mode enabled, use 'start {Interface}' right here.":
		scanwifi()
		print ""

### IP's SCANNING LAN ###
def lan_ips(output):
	test=conneted()
	if test!=False:
		array_ip=[]
		commands.getoutput('nmap -sP '+test+'/24 -oX tmp/ips.xml > null')
		xmldoc = minidom.parse('tmp/ips.xml')
		itemlist = xmldoc.getElementsByTagName('address')
		for s in itemlist:
		    ip=s.attributes['addr'].value
		    if ip!=test:
		    	array_ip.append(ip)

	if output==1 and test!=False:
		for ip in array_ip:
			if ip.find(":") <= 0 :
				mac=ip
				if get_gateway(2)==mac:
					mac+="]["+colors.B+"GATEWAY"+colors.W
			else:
				print " Host's up  : ["+mac+"]["+ip+"]"
		commands.getoutput('rm tmp/ips.xml > null')
	else:
		return False

### STATUS CMD ###
def status_cmd(cmd,tabulations):
	status_1=subprocess.call(cmd+' > null', shell=True)
	if status_1==0:
		return tabulations+""+colors.G+"[OK]"+colors.W
	else:
		return tabulations+""+colors.R+"[ERROR]"+colors.B+"[WARNING]"+colors.W


### GET GATEWAY ###
def get_gateway(output):
	test=conneted()
	if test!=False:
		ip_r_l=subprocess.Popen("ip r l",shell=True,stdout=subprocess.PIPE).communicate()[0]
		s = StringIO.StringIO(ip_r_l)
		for line in s:
			if "default" in line:
				gateway = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',line).group(0)

	if output==1 and test!=False:
		print " Gateway    :  "+gateway
	if output==2 and test!=False:
		return gateway

### am I Connected? ###
def conneted():
	test=myip()
	if test!=False:
		return test
	else:
		return False

### GET MY MAC ADRRESS ###
def my_mac_address(output):
	if conneted()!=False:
	    my_macs = [get_if_hwaddr(i) for i in get_if_list()]
	    for maca in my_macs:
	        if(maca != "00:00:00:00:00:00") and output==1:
	            print " Mac Address:  "+maca
	            return

### UPDATE PARAMATERS ###
def update(variable,value,name):
	var=len(name)+5
	value=value[var:]
	return value