#Importing all required modules
import os
import re
import subprocess
import warnings
import instaloader

while True:
    #Enter the post/reel link to download
    url=input("Enter the post/reel link: ")
    if re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",url):
        #Getting the code of the insta post/reel
        regexp = '^(?:.*\/(p|tv|reel)\/)([\d\w\-_]+)'
        shortcode = re.search(regexp, url).group(2)

        #Loading Instaloader
        L = instaloader.Instaloader(filename_pattern=shortcode)
        path="./sessionid"
        USER="Your Instagram Username"


        #Loading saved session
        if os.path.isfile(path):
            L.load_session_from_file(USER, filename="sessionid")

        #Login if session not found
        else:
            PASSWORD="Your Instagram Password"
            try:
                #Login directly from the given username and password
                L.login(USER, PASSWORD)
            except instaloader.exceptions.ConnectionException:
                #This method will be used if upper login method doesn't work
                print("\n+---------------------------------------------+")
                print("| Your session is not saved!! Login required! |")
                print("+---------------------------------------------+\n")
                USER=input("Enter your instagram username: ")
                warnings.simplefilter('ignore')
                L.interactive_login(USER)
            
            #Saving the session so we don't need to login again
            L.save_session_to_file(filename="sessionid")   


            #Downloading post/reel
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target='videos')
            print("\nFile downloaded!")
            os.remove(f"./videos/{shortcode}.json.xz")
            os.remove(f"./videos/{shortcode}.txt")
        except instaloader.exceptions.QueryReturnedBadRequestException:
            print("bad")
    elif url.lower()=="s":
        break
    else:
        print("Enter Valid URL!!\n")
    print("\nType s to stop!")
print("\n+--------------------------------------+")
print("| Thank you for using Insta downloader |")
print("+--------------------------------------+")
