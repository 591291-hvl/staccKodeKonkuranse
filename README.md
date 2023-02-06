# staccKodeKonkuranse
 


## Task description
Project is written in python as i thought a little variation in submissions was needed:). Flask backend + plain js frontend.

I decided to create an application where it is possible to upload a json file of own electricity usage.

User can select kr/kWh to calculate price for uploaded period.
User can select area to calculate price for "spotpris".

User is given a graph displaying amount of electricity usage, average electricity usage, and "spotpris".

## How to run

python packages:
flask
matplotlib
pandas
base64


Run main.py and open http://127.0.0.1:5000/ to run on local

To just view, the site is being run on:

If no file is selected, a default from: https://github.com/stacc/future-of-fintech-V2023/blob/main/data/consumption.json 
is given, otherwise please upload a .json file.

## Comments
The solution should have been expanded to accept other files than just json, and check if file is valid.

"SpotPris" is pre downloaded for a year, this is mostly done to improve response time. Otherwise it could easily be done through "Nord Pool"'s api.

main.ipynb was used for testing functions before moving to main.py.

Code lacks comments, i hope variable/function names are enough to understand:)

There is also 2 global variables due to some complications with what i was able to send/receive in one fetch, otherwise it would be a single fetch.
