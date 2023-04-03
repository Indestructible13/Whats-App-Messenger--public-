import pywhatkit
import datetime
import random
import time

run_flag = True
test_flag = False

if (test_flag):
    receiving_number = '+1678*******' # Test (send to myself)
else:
    receiving_number = '+1770*******'
     # Real (send to target phone number)


def get_random_msg():
    #msg=get_random_msg_from_msglist()
    msg=get_random_msg_from_array()
    return msg

def get_random_msg_from_msglist():
    s=open("message-list.txt","r")
    m=s.read()
    l=m.split('/m')
    l = sanitize_list(l)
    msg=random.choice(l)
    return msg

msg_array = []
def initialize_msg_array():
    msg_array.append("Example message 1")
    msg_array.append("Example message 2")
    msg_array.append("Example message 3")

def get_random_msg_from_array():
    # Shuffle the list so it sends in a random order.
    random.shuffle(msg_array)

    # Grab the message from the end of the array.
    try:
        msg = msg_array[len(msg_array)-1]
    # Exception happens if the list is empty.
    except: 
        msg = "Sorry I'm out of custom messages! Tell Jordan to make a longer list next time!"
    
    # Custom addition to the first message that sends.
    if len(msg_array) == 12:
        msg += '\n\nThis is the first message being sent!'

    # Pop it from the msg_array to prevent repeat sends.
    try:
        msg_array.pop()
    except:
        print("No msg to pop!")

    return msg + '\n\t\t\t\t\t- Jordan\'s Bot'

def sanitize_list(list):
    l = list
    # Iterates through list for these reasons:
    # 1. Gets rid of the extra \n characters in each string.
    # 2. Removes empty items like ''.
    for i in range(0,len(l)): # 1
        l[i] = remove_slash_n(l[i])
    pop_empty_list_items(l) # 2
    return l

def remove_slash_n(txt):
    txt = txt
    if txt.endswith('\n'):
        txt = txt[:-1]
    if txt.startswith('\n'):
        txt = txt[1:]
    return txt

def pop_empty_list_items(list):
    l = list
    popped = True # If an item was popped last time, try again until there are no more items to pop.
    while (popped):
        popped = False # Reset 'popped' flag. If no item is popped in the for loop below, then the while loop will stop.
        for i in range(0,len(l)):
            if l[i] == '':
                l.pop(i)
                popped = True
                break

def schedule_msg(number, msg, hour, minute):
    pywhatkit.sendwhatmsg(number,msg,hour,minute,wait_time=30,tab_close=True)
    
    
# Sends a message every even hour at the specified minute.
def calculate_next_time():
    currenttime = datetime.datetime.now()
    minute = 30 # Always schedule the minute to be 30.
    even_hour = currenttime.hour % 2 == 0 # True if the current hour is an even number.
    before_minute = currenttime.minute < minute # True if the current minute is before the specified minute.
    # Makes sure the scheduled hour is always the next even hour.
    if not even_hour:
        hour = currenttime.hour + 1
    elif before_minute:
        hour = currenttime.hour
    elif (not before_minute):
        hour = currenttime.hour + 2

    # Fix formatting errors. (e.g. hour cannot be 24 and minute cannot be 60)  
    if (minute == 60):
        minute = 0
        hour = hour + 1
    if (hour == 24):
        hour = 0
    if (hour == 25):
        hour = 1  
    return [hour, minute]

def calculate_next_test_time():
    currenttime = datetime.datetime.now()
    minute = currenttime.minute + 2
    hour = currenttime.hour

    # Fix formatting errors. (e.g. hour cannot be 24 and minute cannot be 60)  
    if (minute >= 60):
        minute = minute - 60
        hour = hour + 1
    if (hour >= 24):
        hour = hour - 24 
    return [hour, minute]



# Main execution section
initialize_msg_array()
while run_flag:
    if (test_flag) :
        print('---- TEST RUN ----')
        scheduled_time = calculate_next_test_time()
    else:
        print('---- REAL RUN ----')
        scheduled_time = calculate_next_time()
    
    msg = get_random_msg()
    print('Next message scheduled for ' + str(scheduled_time[0]) + ':' + str(scheduled_time[1]))
    print('Sending message to ' + receiving_number)
    print('Message to be sent: \n\n' + msg + '\n')
    schedule_msg(receiving_number, msg, scheduled_time[0], scheduled_time[1])
    print('Sleeping for 10 seconds to prepare for next transmission...')
    print('----------------------------------------------------------------------------------------')
    time.sleep(10)