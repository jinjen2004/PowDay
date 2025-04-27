# PowDay

`pip install -r requirements.txt`  

Data: Migrated to DB. import_data.py is used to build db from csv. If instance/ski_resort.db is not there or corrupted it can be made by running `python import_data.py 'path/to/resortdata.csv`  

If you get ""⚠️ Could not reach the geocoding service – location filter skipped." and or "⚠️ Location not found." this is from the library used to filter search results based on a location and distance around that location. To fix try `/Applications/Python\ 3*/Install\ Certificates.command` ( on mac )  

#### Marco-ToDo:
- Shrink the legend that pops up on weather maps (resort page)
- Complete Search
  - pass_type: (Ikon,Epic,None) ✅ 
  - Price("$" = 150,"$$" = 150-250,"$$$" = 250+) ✅ 
  - Distance&LOC ✅
  - Size ✅
  - Vertical Drop ✅ (make slider/min and max more useful) 
  - Days of the week 🟡 (searching through busiest days. ex: user select monday. resort with monday as busiest day omited
  Problem: Busiest days arent standardized and stored like that)
  - snowboarders ✅

### frontend to do
- add confirmation page for booking a trip

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
  - Stats/Descriptions: Currently [Description,LocationCO,Lift Tickets Price,Difficulty,Annual Snowfall,Skiable Area,Vertical Drop,Busiest Days (This data may not be entirely accurate as of now)]
  - A Weather report
  - A Map of the resort which can be selected to display weather information
  - Reviews (empty currently)
  - Book now button (Stubbed currently, should take us to booking page when we have one) 
- **Booking** The user can book ski trips here. 
- **Explore** The user can browse through ski resorts provided by an algorithm
- **Search**  The usercan input diverse criteria and retrieve a list of resorts fitting said criteria. The user should be able to order these results in any sensible way.

#### Weather API
[openweathermap](openweathermap.org) as weather API. Student free tier gives 3,000 API calls/ minute, should be more than enough.

