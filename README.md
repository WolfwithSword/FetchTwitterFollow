# Fetch Twitter Follow
Export a user's twitter follows or following to a CSV, including data on each user's description, links, etc.

# Setup Steps
1) Create an application under development on twitter https://developer.twitter.com/en/portal/projects-and-apps
2) Give it a name and fill in some fluff on the purpose such as "testing or exploring the api"
3) Open auth.ini to copy some stuff in
4) Copy the api key, api key secret and bearer token
5) Click in bottom right "App settings"
6) In the Keys and Tokens page on the app settings, click Generate under "Access Token and Secret"
7) Copy the access token and access token secret
8) Fill in all the fields in auth.ini with the copied values


#Running the program

1) Open terminal where the .exe is, and make sure the other files are present (auth.ini, USER_FIELDS)
2) CLI Options
    - -u
       - REQUIRED
       - The username of the account you want to fetch data from (like your username, no @ symbol)
    - -m
      - SEMI-REQUIRED
      - DEFAULT: following
      - Mode select. "following" for getting a list of accounts the user follow. "followers" for user's followers. No quotes
    - -auth
       - OPTIONAL BUT FILE IS REQUIRED
       - DEFAULT: ./auth.ini
       - The directory of the auth.ini file
    - --urlexpand
       - OPTIONAL BUT RECOMMENDED
       - Usage: "--urlexpand" at the end of command
       - If added, the "website url" field on each user account will be expanded from the https://t.co/ link to the full link.
        WARNING: If included, it will make this tool MUCH MUCH MUCH slower, since it needs to do a GET request on each URL individually.
        NOTE: It only does it for the "url" website field. Any in the tweet "status" or description won't be expanded.
        
3) Run Examples:

    - ./FetchTwitterFollow.exe -m followers -u _WolfwithSword --urlexpand
    - ./FetchTwitterFollow.exe -m following -u _WolfwithSword -auth ./custom-auth.ini
    - ./FetchTwitterFollow.exe -m following -u _WolfwithSword
    - ./FetchTwitterFollow.exe -u _WolfwithSword

4) Output
 
    - It will output a CSV based on the mode, username, date, and columns found in USER_FIELDS (see below for this)

    - Format: [username]-[mode: following or followers]-[date: YYYYMMDD].csv

5) Notes

    - Rate limiting is a thing. This program will pause/sleep on rate limits for about 5 minutes, but will continually do so.
 
6) USER_FIELDS

    - These are the fields that exist on a User object and will be columns in the CSV
    - Below are the available options. In the default file, a bunch are removed for being somewhat useless.

    - I also put descriptions next to some which aren't intuitive

- USER_FIELDS OPTIONS
   
   -        contributors_enabled
            created_at 
            default_profile 
            default_profile_image 
            description 
            email 
            favourites_count        : # of likes
            followers_count          
            following 
            friends_count             : # of following
            geo_enabled 
            id 
            id_str 
            lang 
            listed_count 
            location 
            name 
            notifications 
            profile_background_color 
            profile_background_image_url 
            profile_background_image_url_https 
            profile_background_tile 
            profile_banner_url 
            profile_image_url 
            profile_image_url_https 
            profile_link_color 
            profile_sidebar_border_color 
            profile_sidebar_fill_color 
            profile_text_color 
            profile_use_background_image 
            protected 
            screen_name 
            status                   : Their status aka most recent tweet. This will be in JSON
            statuses_count           : # of tweets
            time_zone 
            url                      : The "website" field
            utc_offset 
            verified                 : Haha, yeah, this API is from way before the plague of "blue verified" existed.
            withheld_in_countries 
            withheld_scope 
            
