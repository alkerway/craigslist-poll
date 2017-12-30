# Craigslist poller
Python app that polls craigslist on a url or filter and emails any new listings to an email specified.

The poll interval is set to 15 minutes because that is the interval Craigslist uses to push up posts to the rss api.

### How to use
1. Have python 2 installed
2. Clone the repo
3. Enter in your email credentials to example file credentials.py (email yourself from your own email)
1. Get desired url by searching craigslist  for what you want (example: 
https://phoenix.craigslist.org/search/msg?min_price=100&max_price=200)
1. Run main.py from terminal with a -url argument set to the url in quotes

python main.py -url "https://phoenix.craigslist.org/search/msg?min_price=100&max_price=200"

### Notes

* If the email isn't a gmail, edit line 90 of main.py to connect to the correct port
* You may have to [allow less secure apps](https://myaccount.google.com/lesssecureapps) to access your account