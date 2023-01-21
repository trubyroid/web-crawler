Web-crawler
===========
This app collect http-statuses of urls and remember domains, which already was requested.

If you want to use it you need to:  
1. Run server: python3 server_cached.py
2. (Other terminal) Run client with urls.  
For example: python3 crawl.py "http://google.com" "http://github.com"
3. Client will print the result and server will notify you if domains already been there.
