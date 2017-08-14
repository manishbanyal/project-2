# importing requests library to make http requests
import requests
# importing urllib3 to download Image
import urllib3

# These variables are global variables
APP_ACCESS_TOKEN = "1535735401.817928f.fe7efbea003b46c4ac08d0f3af81182c"
BASE_URL = 'https://api.instagram.com/v1/'
sandbox_users = ["eviledmpredator"]
# creating a variable menu
menu = "\nMenu:\n0.Fetch your own details\n1.Fetch a user's details\n2.Fetch user id of  instagram user\n" \
       "3.Fetch latest post of yours \n4.Fetch a user's latest post\n5.Fetch media you liked recently\n" \
       "6.Like a user's post\n7.List the comments on a user's post\n8.Comment on a user's post" \
       "\n9.exit\n"


# function to show one's own information
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=' + APP_ACCESS_TOKEN)
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            print("Username: {}".format(user_info["data"]["username"]))
            print("No. of followers: {}".format(user_info["data"]["counts"]["followed_by"]))
            print("No. of people you are following: {}".format(user_info["data"]["counts"]["follows"]))
            print("No. of posts: {}".format(user_info["data"]["counts"]["media"]))
        else:
            print("User does not exist")
    else:
        print("status code other than 200")
    start_bot()


# Defining a function to get user info using the username
def get_user_info(insta_username):
    user_id = getUserID(insta_username)  # Using the previous get_user_id function to get the user_id
    if user_id is None:
        print('The user does not exist')
        exit()
    req_url = BASE_URL + 'users/' + user_id + '/?access_token=' + APP_ACCESS_TOKEN
    user_info = requests.get(req_url).json()

    # Printing the user details in a readable way
    if user_info['meta']['code'] == 200:
        if len(user_info['data']) > 0:
            print('Username: %s' % (user_info['data']['username']))
            print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
            print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
            print('No. of posts: %s' % (user_info['data']['counts']['media']))
        else:
            print('There is no data for this user!')
    else:
        print('Status code other than 200 received!')
    start_bot()


# function to return user_id of a user
def getUserID(insta_username):
    request_url = BASE_URL + "users/search?q={}&access_token={}".format(insta_username, APP_ACCESS_TOKEN)
    print("Requesting URL \n{}".format(request_url))
    user_info = requests.get(request_url).json()
    if user_info["meta"]["code"] == 200:
        if len(user_info["data"]):
            return user_info['data'][0]['id']
        else:
            print("No user found")
    else:
        print("Status code other than 200 found")


# function to return one's own recent post's id
def getOwnRecentPost():
    request_url = BASE_URL + "users/self/media/recent/?access_token={}".format(APP_ACCESS_TOKEN)
    print("Requesting:\n{}".format(request_url))
    recent_post = requests.get(request_url).json()
    if recent_post["meta"]["code"] == 200:
        if len(recent_post["data"]) > 0:
            recent_img_url = recent_post["data"][0]["images"]["standard_resolution"]["url"]
            urllib3.disable_warnings()
            connection_pool = urllib3.PoolManager()
            resp = connection_pool.request('GET', recent_img_url)
            f = open("own_post.jpg", 'wb')
            f.write(resp.data)
            f.close()
            return recent_post["data"][0]["id"]
        else:
            print("No posts to show")
            return None
    else:
        print("Status code other than 200")
        return None


# full fledged function to take username as input and return user's recent post's id
def recentPostOfUser(insta_username):
    user_id = getUserID(insta_username)
    if user_id is not None:
        request_url = "https://api.instagram.com/v1/users/{}/media/recent/?access_token={}".format(user_id,
                                                                                                   APP_ACCESS_TOKEN)
        recent_post = requests.get(request_url).json()
        if recent_post["meta"]["code"] == 200:
            if len(recent_post["data"]) > 0:
                recent_img_url = recent_post["data"][0]["images"]["standard_resolution"]["url"]
                urllib3.disable_warnings()
                connection_pool = urllib3.PoolManager()
                resp = connection_pool.request('GET', recent_img_url)
                f = open("recent.jpg", 'wb')
                f.write(resp.data)
                f.close()
                resp.release_conn()
                return recent_post["data"][0]["id"]
            else:
                print("No posts to show")
                return None
        else:
            print("Status code other than 200")
            return None


# function to print the id of media liked by self
def postLikedByMe():
    request_url = BASE_URL + "users/self/media/liked?access_token={}".format(APP_ACCESS_TOKEN)
    media_liked = requests.get(request_url).json()
    if media_liked["meta"]["code"] == 200:
        if len(media_liked["data"]) > 0:
            print(media_liked["data"][0]["id"])
        else:
            print("No media to show")
    else:
        print("Status code other than 200")
    start_bot()


# function to like a user's recent post
def likePost(insta_username):
    post_id = recentPostOfUser(insta_username)
    req_url = BASE_URL + 'media/' + post_id + '/likes'
    payload = {"access_token": APP_ACCESS_TOKEN}
    post_a_like = requests.post(req_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print('Like was successful!')
    else:
        print('Your like was unsuccessful. Try again!')
    start_bot()


# function to get a list of comments on a user's recent post
def listComments(insta_username):
    post_id = recentPostOfUser(insta_username)
    request_url = BASE_URL + "media/{}/comments?access_token={}".format(post_id, APP_ACCESS_TOKEN)
    print("Requesting:\n{}".format(request_url))
    comments_on_this_post = requests.get(request_url).json()
    if comments_on_this_post["meta"]["code"] == 200:
        for i in range(0, len(comments_on_this_post["data"])):
            print(comments_on_this_post["data"][i]["from"]["username"], end=" : ")
            print(comments_on_this_post["data"][i]["text"])
            print()
    else:
        print("Status code other than 200")
    start_bot()


# function to comment on a uer's post
def comment(insta_username):
    post_id = recentPostOfUser(insta_username)
    comment_ = input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_}
    req_url = BASE_URL + 'media/' + post_id + '/comments'

    make_comment = requests.post(req_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print("Successfully added a new comment!")
    else:
        print("Unable to add comment. Try again!")
    start_bot()


uname = input("Enter the username :\n"
              "Your Sandbox users are:\n{}\n"
              .format(sandbox_users))


# this will start the instabot
def start_bot():
    choice = int(input(menu))
    if choice == 0:
        self_info()
    elif choice == 1:
        get_user_info(uname)
    elif choice == 2:
        user_id = getUserID(uname)
        print(user_id)
        start_bot()
    elif choice == 3:
        own_post_id = getOwnRecentPost()
        print("Post Downloaded")
        print("Post ID : ", own_post_id)
        start_bot()
    elif choice == 4:
        user_post_id = recentPostOfUser(uname)
        print("Post downloaded")
        print("Post ID: ", user_post_id)
        start_bot()
    elif choice == 5:
        postLikedByMe()
    elif choice == 6:
        likePost(uname)
    elif choice == 7:
        listComments(uname)
    elif choice == 8:
        comment(uname)
    elif choice == 9:
        exit(code="Application Closed")
    else:
        exit(code="You did'nt entered one of the choices above")


start_bot()
