#Importing all required modules
import os
import re
import subprocess
import warnings
import instaloader
import traceback
from dotenv import load_dotenv
load_dotenv()
while True:
    #Getting credentials from .env file
    sessionid = os.getenv("SESSION_ID")
    USER= os.getenv("USER")
    PASSWORD= os.getenv("PASS")
    token = os.getenv("TOKEN")
    #Loading Instaloader
    loginmethod = None
    if sessionid:
        loginmethod = 1
        print("\n+--------------------------------------------+")
        print("| Loading previous session using session_id! |")
        print("+--------------------------------------------+\n")
        L = instaloader.Instaloader()
        L.context.session = sessionid
    else:
        loginmethod = 2
        L = instaloader.Instaloader()
        try:
            print("\n+--------------------------------------------------------------------------+")
            print("| Your session is not saved!! Trying to Login using USERNAME and PASSWORD! |")
            print("+--------------------------------------------------------------------------+\n")
            #Login directly from the given username and password
            L.login(USER, PASSWORD)
        except instaloader.exceptions.ConnectionException:
            #This method will be used if upper login method doesn't work
            print("\n+---------------------------------------------------------------+")
            print("| Login failed due to malformed data! Trying to Login manually! |")
            print("+---------------------------------------------------------------+\n")
            USER=input("Enter your instagram username: ")
            warnings.simplefilter('ignore')
            L.interactive_login(USER)
        except instaloader.exceptions.BadCredentialsException:
            print("\n+--------------------------------------------------------------------+")
            print("| Login failed due to inavlid Credentials! Trying to Login manually! |")
            print("+--------------------------------------------------------------------+\n")
            USER=input("Enter your instagram username: ")
            warnings.simplefilter('ignore')
            L.interactive_login(USER)
        except:
            traceback.print_exc()
            break
            
        if loginmethod != 1:
            #Saving session so that program doesn't require login next time
            cookie_jar = L.context._session.cookies
            for cookie in cookie_jar:
                if cookie.name == "sessionid":
                    session_id = cookie.value
                    if session_id!="":
                        with open(".env", "r") as file:
                            contents = file.readlines()
                        e=0
                        for line in contents:
                            if "SESSION_ID" in line:
                                contents[e]=f"SESSION_ID = '{session_id}'\n"
                                e='y'
                                break
                            e+=1
                        if str(e).isdigit():
                            contents[-1]=f"SESSION_ID = '{session_id}'\n"
                        with open(".env", "w") as f:
                            f.writelines(contents)
                        f.close()
                        file.close()
                        
    #Enter the post/reel link to download
    url=input("Enter the post/reel link: ")
    if re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",url):
        #Getting the code of the insta post/reel
        regexp = '^(?:.*\/(p|tv|reel)\/)([\d\w\-_]+)'
        shortcode = re.search(regexp, url).group(2)
        L.filename_pattern=shortcode
        #Downloading post/reel
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=f'videos')
            print("\nFile downloaded!")
            os.remove(f"./videos/{shortcode}.json.xz")
            os.remove(f"./videos/{shortcode}.txt")
        except instaloader.exceptions.QueryReturnedBadRequestException:
            print("Incorrect URL or File is Private")
    elif url.lower()=="s":
        break
    else:
        print("Enter Valid URL!!\n")
    print("\nType s to stop!")
print("\n+--------------------------------------+")
print("| Thank you for using Insta downloader |")
print("+--------------------------------------+")
