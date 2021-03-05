#threading ve queue birlikte kullunýldý. threding paralel iþlem yapar. kuyruðun üzerine elamn ekleme gibi. zamanlayýcý için kullanýlan kütüphanedir.(threadig)

import threading   
import queue
import time
import random
import sys

max_qsize = 0
waittimes = []
max_waittime = 0
gise1_sure = 0
gise1_musteri = 0
gise2_sure = 0
gise2_musteri = 0
gise3_sure = 0
gise3_musteri = 0
gise4_sure = 0
gise4_musteri = 0

#Asagidaki 4 fonksiyon birbirlerinin aynisi, her bir giþe için ayrý ayrý class'lar yapýlmalý. 

def gise1(client,c_time,f):
     #lock.acquire()fonksiyonu zaman aþýmýný engeller.Ýstenen 	zaman gelince müþteri alýmýný durdurur.Zamanlayýcýdýr.
     #lock.release() ise,acquire ile kitli olan durumu kilitli    	deðil yapar.
     #str(c_time), c_time'ý önceden tanýmlamadan kullanmamýzý    	saðlar. 
	lock1.acquire()
	f.write (str(c_time) + ".dakikada " + client + " Gise-1 de hizmet almaya baslamistir. \n")
	rand = random.randint(3,10) 
	time.sleep(rand)
	c_time += rand
	f.write (str(c_time) + ".dakikada " + client + " Gise-1 den ayrilmistir. \n")
	global gise1_sure
	global gise1_musteri
	gise1_sure += rand
	gise1_musteri += 1
	lock1.release()

def gise2(client,c_time,f):
	lock2.acquire()
	f.write (str(c_time) + ".dakikada " + client + " Gise-2 de hizmet almaya baslamistir. \n")
	rand = random.randint(3,10)
	time.sleep(rand)
	c_time += rand
	f.write (str(c_time) + ".dakikada " + client + " Gise-2 den ayrilmistir. \n")
	global gise2_sure
	global gise2_musteri
	gise2_sure += rand
	gise2_musteri += 1
	lock2.release()

def gise3(client,c_time,f):
	lock3.acquire()
	f.write (str(c_time) + ".dakikada " + client + " Gise-3 de hizmet almaya baslamistir.\n")
	rand = random.randint(3,10)
	time.sleep(rand)
	c_time += rand
	f.write (str(c_time) + ".dakikada " + client + " Gise-3 den ayrilmistir.\n")
	global gise3_sure
	global gise3_musteri
	gise3_sure += rand
	gise3_musteri += 1
	lock3.release()

def gise4(client,c_time,f):
	lock4.acquire()
	f.write (str(c_time) + ".dakikada " + client + " Gise-4 de hizmet almaya baslamistir.\n")
	rand = random.randint(3,10)
	time.sleep(rand)
	c_time += rand
	f.write (str(c_time) + ".dakikada " + client + " Gise-4 den ayrilmistir.\n")
	global gise4_sure
	global gise4_musteri
	gise4_sure += rand
	gise4_musteri += 1
	lock4.release()


def musteri_ekle(q,sim_time,f): 
#sim simülasyonu, q kuyruðu ifade eder.
	i = 1
	start = 0
	while True:
		if start == sim_time or start > sim_time:
			f.write ("Simulasyon suresi bitmistir, kuyruga musteri ekleme durduruluyor, kuyruktakilere hizmet veriliyor... \n")
			break
		if q.qsize() < 500:
			client = "Musteri-" + str(i)
			f.write (str(start) + ".dakikada " + client + " IDO'ya gelmis ve kuyruga eklenmistir... \n")
			q.put(client + "_" + str(start))
			global max_qsize
			if q.qsize() > max_qsize:
				max_qsize = q.qsize()
			rand = random.randint(0,5) 			   				time.sleep(rand)
			i += 1
			start += rand

q = queue.Queue()
sim_time = int(input("Simulasyon suresini giriniz: "))
f = open("output.txt","a+")
t = threading.Thread(target=musteri_ekle, args=(q,sim_time,f,))
t.start()
start = 0

#locklarýn olduðu sýnýflarý kilitler.
lock1 = threading.Lock()  
lock2 = threading.Lock()
lock3 = threading.Lock()
lock4 = threading.Lock()

giseler = []
giseler.append(t)

while True:
	#f.write "Simulasyon basindan itibaren gecen zaman: " + str(start/60) + " dakika."
	if not t.is_alive() and q.empty():
		break

	if not lock1.locked():
		if not q.empty():
			arr = q.get().split("_")
			client = arr[0]
			begin = arr[1]
			waittimes.append(start-int(begin))
			if start - int(begin) > max_waittime:
                                max_waittime = start - int(begin)
			gise = threading.Thread(target = gise1, args=(client,start,f,))
			gise.start()
			giseler.append(gise)

	elif not lock2.locked():
                if not q.empty():
                       	arr = q.get().split("_")
                        client = arr[0]
                        begin = arr[1]
                        waittimes.append(start-int(begin))
                        if start - int(begin) > max_waittime:
                                max_waittime = start - int(begin)
                        gise = threading.Thread(target = gise2, args=(client,start,f,))
                        gise.start()
                        giseler.append(gise)

	elif not lock3.locked():
                if not q.empty():
                        arr = q.get().split("_")
                        client = arr[0]
                        begin = arr[1]
                        waittimes.append(start-int(begin))
                        if start - int(begin) > max_waittime:
                                max_waittime = start - int(begin)
                        gise = threading.Thread(target = gise3, args=(client,start,f,))
                        gise.start()
                        giseler.append(gise)

	elif not lock4.locked():
                if not q.empty():
                        arr = q.get().split("_")
                        client = arr[0]
                        begin = arr[1]
                        waittimes.append(start-int(begin))
                        if start - int(begin) > max_waittime:
                                max_waittime = start - int(begin)
                        gise = threading.Thread(target = gise4, args=(client,start,f,))
                        gise.start()
                        giseler.append(gise)

	else:
		pass

	time.sleep(1)
	start += 1

for t in giseler:
	t.join()

total = 0
for wtime in waittimes:
	#f.write "Wtime: " + str(wtime)
	total += wtime

avg = float(total)/len(waittimes)
res1 = 0
res2 = 0
res3 = 0
res4 = 0
if not gise1_musteri == 0:
	res1 = float(gise1_sure) / gise1_musteri

if not gise2_musteri == 0:
        res2 = float(gise2_sure) / gise2_musteri

if not gise3_musteri == 0:
        res3 = float(gise3_sure) / gise3_musteri

if not gise4_musteri == 0:
        res4 = float(gise4_sure) / gise4_musteri


f.write ("Simulasyon bitmistir.")
f.write ("Herhangi bir zamandaki kuyrukta bekleyen max musteri sayisi: " + str(max_qsize) + "\n")
f.write ("Kuyrukta en uzun bekleyen musterinin bekleme suresi: " + str(max_waittime) + "\n")
f.write ("Bir musterinin kuyrukta ortalama bekleme suresi: " + str(avg) + "\n")
f.write ("Gise No	Toplam Musteri Sayisi	Ortalama Hizmet Verme Suresi \n")
f.write ("-------	---------------------	---------------------------- \n")
f.write ("   1   		  " + str(gise1_musteri) + "                         " + str(res1) + "\n") 
f.write ("   2   		  " + str(gise2_musteri) + "                         " + str(res2) + "\n") 
f.write ("   3   		  " + str(gise3_musteri) + "                         " + str(res3) + "\n") 
f.write ("   4   		  " + str(gise4_musteri) + "                         " + str(res4) + "\n")
f.close()
