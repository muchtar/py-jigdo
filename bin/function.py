#This is the function
import time

#info = "PyRamid 1.0"

#untuk button
btn_size = (100,30)

#untuk table
myColor = 'Aquamarine'

tanggal = []
for i in range(1, 32):
	tanggal.append(`i`)

months = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 
	'Agustus', 'September', 'Oktober', 'November', 'Desember']

week = []
for i in range(1, 53):
	week.append(`i`)

tahun = []
for i in range(2009, 2016):
	tahun.append(`i`)
	
hours = []
for i in range(0, 25):
	hours.append(`i`)
	
minutes = []
for i in range(0, 60):
	minutes.append(`i`)
	
seconds = []
for i in range(0, 60):
	seconds.append(`i`)
	
#Untuk menampilkan format tanggal, contoh: SELASA, 10 FEBRUARI 2009  |  14:00:00
def formattanggal(x):
	#harilist = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
	harilist = {'Mon':'Senin', 'Tue':'Selasa', 'Wed':'Rabu', 'Thu':'Kamis', 'Fri':'Jumat', 'Sat':'Sabtu', 'Sun':'Minggu'}
	#bulanlist = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
	
	frm = time.strftime('%a', x)
	
	tgl = int(x[2])
	hari = harilist[frm]
	bln = int(x[1])
	bulan = months[bln-1]
	thn = int(x[0])
	jam = int(x[3])
	mnt = int(x[4])
	det = int(x[5])
	tanggaljam = "%s, %s %s %s" % (hari, tgl, bulan, thn)
	return tanggaljam	
	

def AddYear(x): #Untuk mengganti format tahun '09' menjadi '2009'
	val = '0'
	if len(x) == 2:
		val = '20'+x
	else:
		val = x
	return val
		
def AddZero(x): #Untuk mengganti format tahun satu digit menjadi dua digit, contoh: 1 menjadi 01, 2 menjadi 02
	val = '0'
	if len(`x`) == 1: #and `x` != '0':
		val = '0'+`x`
	else:
		val = `x`
	return val

