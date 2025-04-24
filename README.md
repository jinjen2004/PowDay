# PowDay

#### QuickFix/ToDo:
- (marco)Data: I can migrate the csv file to an actual database. Why I want to fix the data first: its AI generated(possibly innacurate),there arent many entries,we may require additional fields. If not I can generate some more entries, check the accuracy of a few examples we want to use and put it in a database. 
- (marco)Shrink the legend that pops up on weather maps (resort page)
- (marco) Search Criteria: Pass(Ikon,Epic),Price($$$),Distance from location,Size,Vertical Drop, Duration, Days of the week, All snowboarders (T/F)

  - Since we want to search by pass type, we have to add that into the data. Some resorts will be neither Ikon nor Epic, so lets loosen the selection for pass types (Ikon, Epic, Both, Neither, Any)
  - Price will be easy, with the final dataset we can assign ($$$) according to the range of prices in the data.
  - Distance from location would be cool if it asked for the users location instead of asking for input but i dont know how to do that
  - Size we can do like price, maybe just divide to large and small if we dont have enough
  - Vertical Drop A slider makes sense, I dont even know if i would ever consider this parameter when searching for a ski resort but the more the better
  - Duration is difficult because im not sure what it would effect, unless we are determining if the resort is open for X days straight. otherwise I think duration is important for determining total price and alerting users if their trip will overlap with "busy days". Important for booking, not as much for searching (edge case resort is closed)
  - Days of the week, resorts open on those days. Seems good for me
  - All snowboarders (T/F) lol are there resorts like this? I like it
    
  (marco): just noting some unfinished ideas so i dont forget.

#### installing flask (on mac)

    in your terminal, check for your python version by inserting command: 'python3 --version'
    
    to be located in the virtual environment, insert command 'python3 -m venv venv' then 'source venv/bin/activate'
    
    then run the command 'pip install flask' in the terminal. If that doesnt work run 'pip3 install flask'
    
    you can then check for your flask version by inserting the command 'python3 -m flask --version'
    
    to check and store current installs run 'pip freeze > requirements.txt'

#### Pages/Templates
- **Home** Main/Home page. Empty for now. Navbar at top allows us to [Explore,Search,Home]
- **Resort** Dedicated page for each resort. 
  - Name of resort
  - Picture of resort
  - Stats/Descriptions: Currently [Description,LocationCO,Lift Tickets Price,Difficulty,Annual Snowfall,Skiable Area,Vertical Drop,Busiest Days (This data may not be entirely accurate as of now)
  - A Weather report
  - A Map of the resort which can be selected to display weather information
  - Reviews (empty currently)
  - Book now button (Stubbed currently, should take us to booking page when we have one) 
- **Booking** The user can book ski trips here. 
- **Explore** The user can browse through ski resorts provided by an algorithm
- **Search**  The usercan input diverse criteria and retrieve a list of resorts fitting said criteria. The user should be able to order these results in any sensible way.

#### Weather API
I hooked up the app to [openweathermap](openweathermap.org) for a weather API. Their free tier gives 60 API calls/minute, and the Student free tier gives 3,000 API calls/ minute. So the Student Free Tier (Which is what is currently connected) should be more than enough. It also gives us real time weather maps (snow wind temp...) so I put all of that on the resorts page. Ill probably trim some of it because its redundant. Anyway the real time weather data should work (Report and map). Also, I hard coded the API key in there. Its a free tier so im not really worried about it.

