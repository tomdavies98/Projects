#Tkinter shell for steam scraper
#This program implements threading to allow the gui to update
#as the computations are completed

#To Do:
#Add prices to the functionality
#Add quit button on second window

import time
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import Button, Tk, HORIZONTAL
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from tkinter import messagebox
import threading
from tkinter import Text, END
from tkinter import *
import random
from heapq import nlargest

#Top ten extra deals feature currently not working

master = tk.Tk()
master.geometry("400x225")
text = "STEAM SALE FINDER"
v = IntVar()

 
#Boolean variable used to see if output should be written to .csv
write = False

def change():
    #Making the variable global allows us to globally edit it's value
    global write
    write = True
def changeBack():
    #Making the variable global allows us to globally edit it's value
    global write
    write = False


#The printing method creates another window in tkinter that
#can then have the programs output printed to
def printing(win,total):
    #Creates RGB values for colour
    textCol = '#%02x%02x%02x' % (197, 203, 216)
    backColour = '#%02x%02x%02x' % (32, 34, 38)

    #Configuring new window for output
    window = tk.Toplevel(master)
    window.geometry("600x250")
    window.winfo_toplevel().title("Look what I found!!!")
    cop = []
    a = []
    
    u = Text(window)

    u.insert(END, "Author: Tom Davies 21/08/18\n")
    u.insert(END, win + "\n\nTen other good deals:\n")

    for i in range(len(total)):
        cop.append(total[i][-8:-6])
        
    top10 = nlargest(10, cop)

    #String manipulation of the 'total' list
    for i in range(len(top10)):
        if any(str(top10[i]) in s for s in total):
            a.append(str(i+1) + ": " + total[i])

    u.insert(END, "\n".join(a) + "\n")
    u.configure(bg=backColour,foreground=textCol)
    u.pack()


#Work2 refers to the function that takes
#reviews into consideration
def work2():
    #Initializing several lists
    nam = []
    rev = []
    sav = []
    end = []
    total = []
    
    my_url2 = 'https://store.steampowered.com/search/?os=win&specials=1&page='
    
    #opening up connection, grabbing the page
    uClient = uReq(my_url2)
    page_html = uClient.read()
    uClient.close()

    #HTML parsing
    page_soup = soup(page_html, "html.parser")

    #Finding the total amount of sales pages
    max_page = page_soup.findAll("div", {"class":"search_pagination_right"})
    max_page = max_page[0].text.strip().replace("\r","")
    max_page = [int(s) for s in max_page.split() if s.isdigit()]
    max_page = max_page[len(max_page)-1]

    #Create .csv file type
    filename = "BestDeals.csv"
    if(write is True):
        f = open(filename, "w")
        headers = "Title:, Sale%\n"
        f.write(headers)
        
    pages = max_page
    #Loop throught the containers to collect data
    for x in range(pages):#max_page
        progress['value']+= (100/pages)
        num = str(x+1)
        my_url = my_url2 + num

        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        #HTML parsing
        page_soup = soup(page_html, "html.parser")

        #Collect containers for tags
        containers = page_soup.findAll("div", {"class":"col search_discount responsive_secondrow"})
        names = page_soup.findAll("div", {"class":"col search_name ellipsis"})
        #prices = page_soup.findAll("div",{"class":"col search_price discounted responsive_secondrow"})
        reviews = page_soup.findAll("span",{"class":"search_review_summary positive"})
        
        for i in range (len(containers)-1):
            #Using try catch to avoid possible unseen errors
            try:
                #Collect span tag and check for Positive review
                review = str(reviews[i])
                if("Positive" in review):
                    n = names[i].span.text.strip().replace(",", "|")
                    saving = containers[i].span.text.strip().replace("-","").replace("%", "")

                    #Collect relevent data
                    nam.append(n)
                    rev.append("Positive")
                    sav.append(saving)

                    #Write information to .csv file
                    if(write is True):
                        f.write(nam[i].replace(",","|") + "," + sav[i].replace(",","|") + "% off" + "\n")
                    
                else:
                    pass
            except:
                pass
                
    #Find the max saving('s) and save it's index
    m = max(sav)
    fav = [i for i, j in enumerate(sav) if j == m]

    for i in range(len(nam)):
        total.append(nam[i] + " with " + sav[i] + "% off ")
    
    #Create complete string of all results from the index('s) recieved
    for i in range(len(fav)):
        end.append(nam[fav[i]] + " with " + sav[fav[i]] + "% off ")

    if(len(end) > 1):
        win = "The best well reviewed deals are:\n" + "\n".join(end) + "\n"
    else:
        win = "The best well reviewed deal is:\n" + end[0]

    printing(win,total)
    progress['value'] = 100
    if(write is True):
        f.close()
    

def work():
    end = []
    myls = []
    myls2 = []
    myls3 = []
    ans = []
    total = []
    my_url2 = 'https://store.steampowered.com/search/?os=win&specials=1&page='
    
    
    #opening up connection, grabbiong the page
    uClient = uReq(my_url2)
    page_html = uClient.read()
    uClient.close()

    #HTML parsing
    page_soup = soup(page_html, "html.parser")

    #Grabs each product
    containers = page_soup.findAll("div", {"class":"col search_discount responsive_secondrow"})
    names = page_soup.findAll("div", {"class":"col search_name ellipsis"})
    prices = page_soup.findAll("div",{"class":"col search_price discounted responsive_secondrow"})

    max_page = page_soup.findAll("div", {"class":"search_pagination_right"})
    max_page = max_page[0].text.strip().replace("\r","")
    max_page = [int(s) for s in max_page.split() if s.isdigit()]
    max_page = max_page[len(max_page)-1]

    answer1 = []
    answer2 = []
    answer3 = []
    #Create .csv file type
    filename = "AllSteamDeals.csv"
    filename2 = "BestDeals.csv"

    if(write is True):
        f = open(filename, "w")
        headers = "Title:, Sale%, Product-Price\n"
        f.write(headers)
    pages = max_page
    
    #Loop throught the containers to collect data
    for x in range(pages):#max_page
        progress['value']+= (100/pages)
        num = str(x+1)
        my_url = my_url2 + num

        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        #HTML parsing
        page_soup = soup(page_html, "html.parser")

        #Grabs each product
        containers = page_soup.findAll("div", {"class":"col search_discount responsive_secondrow"})
        names = page_soup.findAll("div", {"class":"col search_name ellipsis"})
        prices = page_soup.findAll("div",{"class":"col search_price discounted responsive_secondrow"})
        #For loop to recover information about products
        for i in range (len(containers)-1):
            try:
                price = prices[i].span.text.strip()
                myls3.append(price)

                saving = containers[i].span.text.strip().replace("-","").replace("%", "")
                myls.append(saving)

                n = names[i].span.text.strip().replace(",", "|")
                myls2.append(n)
                if(write is True):
                    f.write(myls2[i].replace(",","|") + "," + myls[i].replace(",","|") + "% off" + "," + myls3[i].replace(",",".") + "\n")
                
                
            except:
                pass
            
    m = max(myls)
    fav = [i for i, j in enumerate(myls) if j == m]

    
    for i in range(len(myls)):
        total.append(myls2[i] + " with " + myls[i] + "% off ")
    
    for i in range(len(fav)):
        end.append(myls2[fav[i]] + " with " + myls[fav[i]] + "% off ")
    
    if(len(end) > 1):
        win = "The best deals are:\n" + "\n".join(end) + "\n"
    else:
        win = "The best deal is:\n" + end[0]
    
    printing(win,total)
    progress['value'] = 100
    if(write is True):
        f.close()
    
def start():
    t.start()
        
def start2():
    t2.start()

#Initiate threading
t = threading.Thread(target = work)
t2 = threading.Thread(target = work2)


backColour = '#%02x%02x%02x' % (32, 34, 38)
bColour = '#%02x%02x%02x' % (22, 70, 120)
bColour2 = '#%02x%02x%02x' % (189, 187, 190)


master.configure(bg=backColour)
l = tk.Label(master, text=text, font=("Helvetica", 16), bg = bColour2,foreground = backColour)
l.place(x = 90, y = 20)


progress=tkk.Progressbar(master,length=200,orient=HORIZONTAL,mode='determinate')
progress.place(x = 100, y = 65)

b = tk.Button(master, command = start, text = "FIND SALES" , height = 2, width = 20, bg = bColour)
b.place(x = 20, y = 155)

b2 = tk.Button(master, command = start2, text = "FIND GOOD SALES" , height = 2, width = 20, bg = bColour)
b2.place(x = 225, y = 155)

#Radio Button
r1 = Radiobutton(master,font=(None,13),foreground= bColour2, text="Send output to .csv file",bg = backColour, variable=v, value=1,command = change)
r1.place(x = 85,y = 90)

r2 = Radiobutton(master,font=(None,13),foreground= bColour2, text="Don't send output to .csv file", bg = backColour, variable=v, value=2,command = changeBack)
r2.place(x = 85,y = 115)

master.attributes("-toolwindow",1)
master.winfo_toplevel().title("Simple Steam Sale Finder (0.54)")


master.mainloop()
