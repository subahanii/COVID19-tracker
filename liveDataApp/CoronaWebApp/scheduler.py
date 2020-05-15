# Schedule Library imported 
import schedule 
import time 

# Functions setup 
def sudo_placement(): 
	print("Get ready for Sudo Placement at Geeksforgeeks") 

def good_luck(): 
	print("Good Luck for Test") 

def work(): 
	print("Study and work hard") 

def bedtime(): 
	print("It is bed time go rest") 
	
def geeks(): 
	print("Shaurya says Geeksforgeeks") 

# Task scheduling 
# After every 10mins geeks() is called. 
schedule.every(10).minutes.do(geeks) 

# After every hour geeks() is called. 
schedule.every().hour.do(geeks) 

# Every day at 12am or 00:00 time bedtime() is called. 
schedule.every().day.at("00:00").do(bedtime) 

# After every 5 to 10mins in between run work() 
schedule.every(1).to(3).minutes.do(work) 

# Every monday good_luck() is called 
schedule.every().monday.do(good_luck) 

# Every tuesday at 18:00 sudo_placement() is called 
schedule.every().tuesday.at("18:00").do(sudo_placement) 

# Loop so that the scheduling task 
# keeps on running all time. 
print("running")
while True: 

	# Checks whether a scheduled task 
	# is pending to run or not 
	schedule.run_pending() 
	time.sleep(1) 
