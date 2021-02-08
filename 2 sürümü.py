import threading
import Queue
import time
import random

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

#bu asagidaki 4 function birbirlerinin aynisi, ilkinde dedigim degisiklikler hepsine uygulanmali dakika conversionu icin
def gise1(client,c_time):
	# c_time ile gosterilen butu arkadaslar c_time/60 olmali 
	lock1.acquire()
	print str(c_time) + ".dakikada " + client + " Gise-1 de hizmet almaya baslamistir."
	rand = random.randint(3,10) # 3*60 ve 10*60 yazilmali
	time.sleep(rand)
	c_time += rand
	print str(c_time) + ".dakikada " + client + " Gise-1 den ayrilmistir."
	global gise1_sure
	global gise1_musteri
	gise1_sure += rand
	gise1_musteri += 1
	lock1.release()

def gise2(client,c_time):
	lock2.acquire()
	print str(c_time) + ".dakikada " + client + " Gise-2 de hizmet almaya baslamistir."
	rand = random.randint(3,10)
	time.sleep(rand)
	c_time += rand
	print str(c_time) + ".dakikada " + client + " Gise-2 den ayrilmistir."
	global gise2_sure
	global gise2_musteri
	gise2_sure += rand
        gise2_musteri += 1
	lock2.release()

def gise3(client,c_time):
	lock3.acquire()
	print str(c_time) + ".dakikada " + client + " Gise-3 de hizmet almaya baslamistir."
	rand = random.randint(3,10)
	time.sleep(rand)
	c_time += rand
	print str(c_time) + ".dakikada " + client + " Gise-3 den ayrilmistir."
	global gise3_sure
	global gise3_musteri
	gise3_sure += rand
        gise3_musteri += 1
	lock3.release()

def gise4(client,c_time):
	lock4.acquire()
	print str(c_time) + ".dakikada " + client + " Gise-4 de hizmet almaya baslamistir."
	rand = random.randint(3,10)
	time.sleep(rand)
	c_time += rand
	print str(c_time) + ".dakikada " + client + " Gise-4 den ayrilmistir."
	global gise4_sure
	global gise4_musteri
	gise4_sure += rand
        gise4_musteri += 1
	lock4.release()


def musteri_ekle(q,sim_time):
	i = 1
	start = 0
	while True:
		if start == sim_time or start > sim_time:
			print "Simulasyon suresi bitmistir, kuyruga musteri ekleme durduruluyor, kuyruktakilere hizmet veriliyor..."
			break
		if q.qsize() < 500:
			client = "Musteri-" + str(i)
			print str(start) + ".dakikada " + client + " IDO'ya gelmis ve kuyruga eklenmistir..."
			#yukaridaki satirda start/60 yazmak gerek dakika cinsinden gostermesi icin 
			q.put(client + "_" + str(start))
			global max_qsize
			if q.qsize() > max_qsize:
				max_qsize = q.qsize()
			rand = random.randint(0,5) # burada dakika olmasi icin 60 ile carpin rakamlari
			time.sleep(rand)
			i += 1
			start += rand

q = Queue.Queue()
sim_time = int(raw_input("Simulasyon suresini giriniz: "))
#sim_time *= 60 // dakika icin burayi dahil edin yoksa girilen rakami saniye olarak alir
t = threading.Thread(target=musteri_ekle, args=(q,sim_time,))
t.start()
start = 0

lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()
lock4 = threading.Lock()

giseler = []
giseler.append(t)

while True:
	#print "Simulasyon basindan itibaren gecen zaman: " + str(start/60) + " dakika."
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
			gise = threading.Thread(target = gise1, args=(client,start,))
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
                        gise = threading.Thread(target = gise2, args=(client,start,))
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
                        gise = threading.Thread(target = gise3, args=(client,start,))
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
                        gise = threading.Thread(target = gise4, args=(client,start,))
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
	print "Wtime: " + str(wtime)
	total += wtime

#Asagidaki comment out edili satirlari dahil ederseniz dakika conversionu yapacaktir.

#max_waittime /= 60
avg = float(total)/len(waittimes)
#avg /= 60 
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

#res1 /= 60
#res2 /= 60
#res3 /= 60
#res4 /= 60

print "Simulasyon bitmistir."
print "Herhangi bir zamandaki kuyrukta bekleyen max musteri sayisi: " + str(max_qsize)
print "Kuyrukta en uzun bekleyen musterinin bekleme suresi: " + str(max_waittime)
print "Bir musterinin kuyrukta ortalama bekleme suresi: " + str(avg)
print "Gise No	Toplam Musteri Sayisi	Ortalama Hizmet Verme Suresi"
print "-------	---------------------	----------------------------"
print "   1   		  " + str(gise1_musteri) + "                         " + str(res1) 
print "   2   		  " + str(gise2_musteri) + "                         " + str(res2) 
print "   3   		  " + str(gise3_musteri) + "                         " + str(res3) 
print "   4   		  " + str(gise4_musteri) + "                         " + str(res4) 
