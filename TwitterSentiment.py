from tkinter.constants import COMMAND
import tweepy,re
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
from tkinter import * 
import tkinter as tk

# creating some variables to store info





tweets = []
tweetText = []

def submit():
    keywrd=key.get()
    NoOfTweet=numb.get()
    DownloadData(keywrd,NoOfTweet)
        
        

def DownloadData(keywrd,NoOfTweet):
    # authenticating with twitter handle
    consumerKey ='FnYQZgKZyFzoiiPYgxIaZJ0AT'
    consumerSecret ='AfUVnQotAQ7Q16XDeCyYLgYlyYGj1g0oQV1G2mhZzvlTbafxlU'
    accessToken ='1392423312102408193-bQcJtiP6Oy9EAewFikk0wAbEJU6xuF'
    accessTokenSecret ='AyxieqA681aTMGdlKlHlu62rgMpNtNacaQEiXU0OZwsz2'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
        
        
    # input the keyword to be searched and number of tweets to search
        
    # keywrd = input("Enter Keyword to search about: ")
    #NoOfTweet = int(input("Enter number of tweets to be searched: "))
        
       
        
        
        
        
        
    #NoOfTweet=10
        


    # searching for tweets
    tweets = tweepy.Cursor(api.search, q=keywrd, lang = "en").items(NoOfTweet)
    polarity = 0
    neutral=0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    
        


    

    #print(tweets)
    #f = open("twitter_data.txt", "a")
    #f.write(tweets)
    #f.close()
    # iterating through tweets fetched
    

    for tweet in tweets:
     
  

        
        
        #print(tweet)
        #Append to temp so that we can store in csv later. I use encode UTF-8
        tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        #print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        # print(analysis.sentiment)  # print tweet's polarity
        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

        if (analysis.sentiment.polarity == 0):  # adding reaction of people's reaction to find average later
            neutral += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
            positive += 1
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
            negative += 1
        elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1
    

        
   
    # finding average of how people are reacting
    positive = percentage(positive, NoOfTweet)
    wpositive = percentage(wpositive, NoOfTweet)
    spositive = percentage(spositive, NoOfTweet)
    negative = percentage(negative, NoOfTweet)
    wnegative =percentage(wnegative, NoOfTweet)
    snegative = percentage(snegative, NoOfTweet)
    neutral = percentage(neutral, NoOfTweet)

    # finding average reaction
    polarity = polarity / NoOfTweet


    # printing out data
    print("How people are reacting on " + keywrd + " by analyzing " + str(NoOfTweet) + " tweets.")
    print()
    print("General Report: ")

    if (polarity == 0):
        print("Neutral")

    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
        
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
        
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
        
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
        
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
        
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")

    
    widgetText.insert(END, "Detailed Report: ")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(positive) + "% people thought it was positive")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(wpositive) + "% people thought it was weakly positive")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(spositive) + "% people thought it was strongly positive")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(negative) + "% people thought it was negative")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(wnegative) + "% people thought it was weakly negative")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(snegative) + "% people thought it was strongly negative")
    widgetText.insert(END, '\n')
    widgetText.insert(END, '\n')
    widgetText.insert(END, str(neutral) + "% people thought it was neutral")
    

    #print("Detailed Report: ")
    #print(str(positive) + "% people thought it was positive")
    #print(str(wpositive) + "% people thought it was weakly positive")
    #print(str(spositive) + "% people thought it was strongly positive")
    #print(str(negative) + "% people thought it was negative")
    #print(str(wnegative) + "% people thought it was weakly negative")
    #print(str(snegative) + "% people thought it was strongly negative")
    #print(str(neutral) + "% people thought it was neutral")

    plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keywrd, NoOfTweet)
    #plotChart()

def cleanTweet(tweet):
    # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

# function to calculate percentage
def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

    
def plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keywrd, noOfkeywrds):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + keywrd + ' by analyzing ' + str(noOfkeywrds) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
    










frame = tk.Tk()
frame.title("TextBox Input")
frame.geometry('1800x900')
frame['background']='#856ff8'
#bg = PhotoImage(file = 'gui_bg.jpg')
widgetText = Text(frame, font='Arial 12 bold', cursor='arrow', bg='lightblue', height=19, width=60)
widgetText.tag_configure('tag-right', justify='right')
widgetText.place(x=185, y=310)
label=tk.Label(frame,text="Welcome to Twitter Sentiment Analysis!",font=('Helvetica bold',40),foreground="green",background="yellow")
label.pack()
l1=tk.Label(frame,text="Enter the keyword!----->",font=('Arial', 25))
l1.pack()   
key=tk.StringVar()
name_entry = tk.Entry(frame,textvariable = key, font=('calibre',10,'normal'))
name_entry.pack()
l2=tk.Label(frame,text="Enter the num of Tweets!----->",font=('Arial', 25))
l2.pack()   
numb=tk.IntVar()
name2_entry = tk.Entry(frame,textvariable = numb, font=('calibre',10,'normal'))
#inputtxt.pack()
   
   
name2_entry.pack()
   
sub_btn=tk.Button(frame,text = 'Submit', command = submit)
sub_btn.pack()

#text = Label(gui,text="enter the keyword to search").pack()
#if True:
frame.mainloop()