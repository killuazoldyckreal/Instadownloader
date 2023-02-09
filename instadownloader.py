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
    #Enter the post/reel link to download
    url=input("Enter the post/reel link: ")
    if re.match(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",url):
        #Getting the code of the insta post/reel
        regexp = '^(?:.*\/(p|tv|reel)\/)([\d\w\-_]+)'
        shortcode = re.search(regexp, url).group(2)

        #Getting credentials from .env file
        session_id = os.getenv("SESSION_ID")
        USER= os.getenv("USER")
        PASSWORD= os.getenv("PASS")
        
        #Loading Instaloader
        if session_id:
            L = instaloader.Instaloader(filename_pattern=shortcode)
            L.context.session = session_id
        else:
            L = instaloader.Instaloader(filename_pattern=shortcode)
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
            cookie_jar = L.context._session.cookies
            for cookie in cookie_jar:
                if cookie.name == "sessionid":
                    session_id = cookie.value
                    #Saving session so that program doesn't require login next time
                    with open(".env", "a") as f:
                        f.seek(0, 2)
                        f.write(f"\nSESSION_ID = '{session_id}'")   
                    f.close()

        #Downloading post/reel
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target='videos')
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
