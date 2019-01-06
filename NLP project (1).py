import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import urllib.request


dataset = pd.read_csv("Restaurant_Reviews.tsv",delimiter = "\t", quoting = 3)

import re 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
corp = []
for i in range(0,3013):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review) 
    corpus.append(review)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:,1].values


# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print ("\n\nConfusion Matrix:\n", cm)
print("Accuracy:", classifier.score(X_test, y_test)*100, "%")

def check(r):
    rev = re.sub('[^a-zA-Z]', ' ', r)
    rev = rev.lower()
    rev = rev.split()
    ps = PorterStemmer()
    rev = [ps.stem(word) for word in rev if not word in set(stopwords.words('english'))]
    rev = ' '.join(rev) 
    corpus.append(rev)

    a = cv.fit_transform(corpus).toarray()
    y_new = classifier.predict(a)
    a = y_new[-1]
    return str(a)



# written by Mani Raj Yadav
# importing required library
import requests
import urllib


# making a variable for received access token

access_token = '8911134469.1efef08.29bd2a882e594528b11ac2aaa137adf9'
# setting the base url that is to be used everywhere
base_url = 'https://api.instagram.com/v1/'


# function to display own information
def self_info():
    # setting the url according to the endpoint documentation
    url_req = base_url+"users/self/?access_token="+access_token
    # getting response from url
    x = requests.get(url_req)
    # getting json object
    user_info = x.json()
    # checking whether request is successful or not by getting status code
    if user_info['meta']['code'] == 200:
        # whether user is present
        if len(user_info['data']):
            # printing user information
            print ('\nUsername: %s' % (user_info['data']['username']))
            print ('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
            print ('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
            print ('No. of posts: %s' % (user_info['data']['counts']['media']))
        # if user is not present
        else:
            print ('User does not exist!')
    # request not successful
    else:
        print( 'Status code other than 200 received!')


# function to get user-id by given user name
def get_user_id(insta_username):
    # setting endpoint and creating and accessing json object
    request_url = (base_url+'users/search?q=%s&access_token=%s') % (insta_username , access_token)
    user_id = requests.get(request_url).json()
    # checking whether the request is successful
    if user_id['meta']['code'] == 200:
        # checking whether the user exist
        if len(user_id['data']):
            return user_id['data'][0]['id']
        else:
            return None
    # request unsuccessful
    else:
        print ("Status code other than 200 received.")


# function for getting info of user by its instagram username
def get_user_info(insta_username):
    # calling function to get user-id
    user_id = get_user_id(insta_username)

    # if user does not exist
    if user_id == None:
        print ("User with the given name does not exist.You are being sent back to the HOME!")
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url+'users/%s?access_token=%s') % (user_id, access_token)
    user_info = requests.get(request_url).json()

    # if request is successful
    if user_info['meta']['code'] == 200:
        # if user-info is present
        if len(user_info['data']):
            print ("Username: %s" % (user_info['data']['username']))
            print ('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
            print ('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
            print ('No. of posts: %s' % (user_info['data']['counts']['media']))
        # user does not exist
        else:
            print ('There is no data for this user!')
    # request unsuccessful
    else:
        print ('Status code other than 200 received!')


# function to get own posts
def get_own_post():
    # setting up endpoint url and accessing json object
    request_url = (base_url + 'users/self/media/recent/?access_token=%s') % access_token
    own_media = requests.get(request_url).json()
    # if request is successful
    if own_media['meta']['code'] == 200:
        # if some posts exist
        if len(own_media['data']):
            c = True
            # loop to avoid crashes on invalid insertion
            while c:
               
                    x = 1
                    c = False
                
                # downloading the post

            if own_media['data'][x-1]['type' ]== 'image':
                post_name = own_media['data'][x-1]['id'] 
               
    # request unsuccessful
    else:
        print ('Status code other than 200 received!')
    return(post_name)


# function to access user posts and downloading
def get_user_post(insta_username):
    # calling function to get user-id
    user_id = get_user_id(insta_username)
    # if user doesnt exit
    if user_id == None:
        print ('User does not exist!')
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    user_media = requests.get(request_url).json()
    # if request is successful
    if user_media['meta']['code'] == 200:
        # if posts exist
        if len(user_media['data']):
            c = True
            # loop for avoiding crashes on entering wrong choice
            while c:
                # if user wants any post other than the latest one
                answer = input( 'Do you want to get the latest post? Reply: Y/N' )
                if answer.upper() == 'Y':
                    x = 1
                    c = False
                elif answer.upper() == 'N':
                    print ('Choose from the following\n')
                    print ("2. Second last post\n3. Third last post..\nand so on..")
                    x = input()
                    if x.isdigit():
                        # checking whether user's choice does exist
                        if x <= len(user_media['data']) :
                            x = int(x)
                            c = False
                        else:
                            print ('This post does not Exist!!')
                    # when user chose a no. more than number of posts
                    else:
                        print ('You did not choose appropriate option. Try again!')
                # when user entered something except y and n
                else:
                    print ('Press only y or n!!')
                    c = True
            # downloading the post

            if user_media['data'][x-1]['type']== 'image':
                post_name = user_media['data'][x-1]['id'] + '.jpeg'
                post_url = user_media['data'][x-1]['images']['standard_resolution']['url']
                urllib.request.urlretrieve(post_url, post_name)
                print ('Your image has been downloaded!')

            else:
                post_name = user_media['data'][x-1]['id'] + '.mp4'
                post_url = user_media['data'][x-1]['videos']['standard_resolution']['url']
                urllib.urlretrieve(post_url, post_name)
                print ('Your video has been downloaded!')
        # post does not exist
        else:
            print ('Post does not exist!')
    # request unsuccessful
    else:
        print ('Status code other than 200 received!')


# function to get id of post
def get_post_id(insta_username):
    # calling function to get user id
    user_id = get_user_id(insta_username)
    # checking whether user exist
    if user_id == None:
        print ('User does not exist!\n You are being sent back to the HOME!!')
        start_bot()
    # making request and accessing obtained json object
    request_url = (base_url + 'users/%s/media/recent/?access_token=%s') % (user_id, access_token)
    
    user_media = requests.get(request_url).json()

    # check if the request is successful
    if user_media['meta']['code'] == 200:
        # check if media exist
        if len(user_media['data']):
            c = True
            # not letting application to terminate on a wrong choice
            while c:
                # in case user wants some other post than the latest one!
                answer = input( 'Do you want to get the latest post? Reply: Y/N' )
                if answer.upper() == 'Y':
                    x = 1
                    c = False
                elif answer.upper() == 'N':
                    print ('Choose from the following\n')
                    print ("2. Second last post\n3. Third last post..\nand so on..")
                    # taking input for post choice
                    x = input()
                    # checking whether we have posts of users's choice
                    if x.isdigit():
                        # checking whether user's choice does exist
                        if x < len(user_media['data']):
                            x = int(x)
                            c = False
                        else:
                            print ('This post does not Exist!!')
                    else:
                        print ('You did not choose appropriate option. Try again!')
                else:
                    print ('Press only y or n!!')
                    c = True
            # returning media id
            return user_media['data'][x-1]['id']
        # no recent post of user
        else:
            print ('There is no recent post of the user!')
            exit()
    # request unsuccessful
    else:
        print ('Status code other than 200 received!')
        exit()


# function to like a post
def like_a_post(insta_username):
    # calling functions to get recent posts id
    media_id = get_post_id(insta_username)
    # creating the endpoint url
    request_url = (base_url + 'media/%s/likes') % media_id
    # creating required payload
    payload = {"access_token": access_token}
        # accessing json object
    post_a_like = requests.post(request_url, payload).json()

    # check whether the request is successful
    if post_a_like['meta']['code'] == 200:
        print ('Like was successful!', 'red')
    # when request is unsuccessful
    else:
        print ('Your like was unsuccessful. Try again!')


# function to post a comment
def post_a_comment(insta_username):
    # getting media id
    media_id = get_post_id(insta_username)

    while True:
        # getting the comment by user
        comment_text = input("Your comment: ")
        if len(comment_text)>0 and comment_text.isspace() == False:
            # creating required payload
            payload = {"access_token": access_token, "text": comment_text}
            # creating endpoint url
            request_url = (base_url + 'media/%s/comments') % media_id
            # accessing json object
            make_comment = requests.post(request_url, payload).json()
            # if request successful
            if make_comment['meta']['code'] == 200:
                print ('\nSuccessfully added a new comment!','blue')
            # if request unsuccessful
            else:
                print ("Unable to add comment. Try again!")
            break
        else:
            print ('Cannot post an empty comment! Try again!')


# function to delete all negative comments from a post
def delete_negative_comment():
    # calling the function for getting media id
    media_id = get_own_post()
    # setting endpoint url and accessing json object
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    comment_info = requests.get(request_url).json()
    # if request successful
    if comment_info['meta']['code'] == 200:
        # if comment exists
        if len(comment_info['data']):
                # iterating over all comments
                for x in range(0, len(comment_info['data'])):
                    # getting comment id
                    comment_id = comment_info['data'][x]['id']
                    # getting comment text
                    comment_text = comment_info['data'][x]['text']
                    # analysing comment by 'TextBlob'
                    pred = check(comment_text)
                    # checking whether sentiments of comment are more negative than positive
                    if pred == '0':
                        print ((comment_text)+": Negative Comment")
                        # setting up endpoint url
                        #delete_url = (base_url+ 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, access_token)
            
                    # positive sentiments are greater than negative sentiments!
                    else:
                        print ((comment_text)+": Positive Comment")
        # no comments found
        else:
            print ("There are no comments on this post yet.")
    # request unsuccessful
    else:
        print ("Status code other than 200 received.")


# function to get list of people who liked a post
def get_like_list(insta_username):
    # getting media id
    media_id = get_post_id(insta_username)
    # setting endpoint url and accessing json object received
    request_url=(base_url+"media/%s/likes?access_token=%s") %(media_id,access_token)
    like_list = requests.get(request_url).json()
    # if likes accessed successfully
    if like_list['meta']['code'] == 200:
        # if any data of user liked the post present
        if len(like_list['data']):
            # displaying people who liked the post
            for x in range(len(like_list['data'])):
                print ('People who liked this post:')
                print ('%d. %s' %(x+1, like_list['data'][x]['username']))
        else:
            print ('No one liked this post yet! Be the first one to like.')
    else:
        print ('Status code other than 200 received.')


# function to get list of comments
def get_comment_list(insta_username):
    # getting media id by caliing function
    media_id = get_post_id(insta_username)
    # setting endpoint url and accessing j.son object
    request_url = (base_url+'media/%s/comments?access_token=%s') %(media_id,access_token)
    comment_list = requests.get(request_url).json()
    # if request is successful
    if comment_list['meta']['code'] == 200:
        # if there exist some comments
        if len(comment_list['data']):
            # displaying all the comments
            for x in range(len(comment_list['data'])):
                print ("%s : %s" %(comment_list['data'][x]['from']['username'], comment_list['data'][x]['text']))
        # if no comment exist
        else:
            print ('There are no comments on this post yet!')
    # if request is unsuccessful
    else:
        print ('Status code other than 200 received.')


# function to list of recent media liked by the owner of the access_token
def list_own_like():
    # setting up endpoint url and accessing json object
    request_url = base_url+ 'users/self/media/liked?access_token=' + access_token
    own_likes = requests.get(request_url).json()
    if own_likes['meta']['code'] == 200:
        print ('Posts liked by the user are:')
        for x in range(len(own_likes['data'])):

            print ('\nFrom:','blue')+own_likes['data'][x]['user']['full_name']+('\nType:','blue')+own_likes['data'][x]['type']
            print ('Post Id:','blue')+own_likes['data'][x]['id']

# starting the application
def start_bot():
    # starting with the application and greeting
    print ('\n')
    print ('Hey! Welcome to instaBot!')
    print ('It\'s way more smarter than you think it is!')
    print ('Try it yourself!!')
    while True:
        print ('\n')
        # displaying menu
        print ('Here are your menu options:\n')
        print ("1.Get your own details\n")
        print ("2.Get details of a user by username\n")
        print ("3.Download your own recent post\n")
        print ("4.Download the recent post of a user by username\n")
        print ("5.Get a list of people who have liked the recent post of a user\n")
        print ("6.Like the recent post of a user\n")
        print ("7.Get a list of comments on the recent post of a user\n")
        print ("8.Make a comment on the recent post of a user\n")
        print ("9.Categorize comments from the recent post of a user\n")
        print ("10.Get list of posts liked by the User.\n")
        print ("11.Exit.\n")

        # getting the choice from user to proceed with the app
        choice = input("Enter you choice: ")

        if choice == '1':
            self_info()

        elif choice == '2':
            while True:
                insta_username = input("Enter the username of the user: ")
                if len(insta_username)>0 and insta_username.isspace() == False:
                    get_user_info(insta_username)
                    break
                else:
                    print ('Enter a valid name!!')

        elif choice == '3':
            get_own_post()

        elif choice == '4':
            while True:
                insta_username = input("Enter the username of the user: ")
                if len(insta_username)>0 and insta_username.isspace() == False:
                    get_user_post(insta_username)
                    break
                else:
                    print ('Enter a valid name!!')
        elif choice == '5':
            while True:
                insta_username = input("Enter the username of the user: ")
                if len(insta_username) > 0 and insta_username.isspace() == False:
                    get_like_list(insta_username)
                    break
                else:
                    print ('Enter a valid name!!')

        elif choice == '6':
            while True:
                insta_username = input("Enter the username of the user: ")
                if len(insta_username) > 0 and insta_username.isspace() == False:
                    like_a_post(insta_username)
                    break
                else:
                    print ('Enter a valid name!!')

        elif choice == '7':
            while True:
                insta_username = input("Enter the username of the user: ")
                if len(insta_username) > 0 and insta_username.isspace() == False:
                    get_comment_list(insta_username)
                    break
                else:
                    print ('Enter a valid name!!')

        elif choice == '8':
            while True:
                insta_username = input("Enter the username of the user: ")
                if len(insta_username) > 0 and insta_username.isspace() == False:
                    post_a_comment(insta_username)
                    break
                else:
                    print ('Enter a valid name!!')

        elif choice == '9':
            while True:
                #insta_username = input("Enter the username of the user: ")
                #if len(insta_username) > 0 and insta_username.isspace() == False:
                delete_negative_comment()
                break
                
        elif choice == '10':
            list_own_like()

       
        elif choice == '11':
            exit()
        # wrong choice
        else:
            print ("Please choose the correct option!!")

# starting the app by calling the function
start_bot()


