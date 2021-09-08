# City-Crawler
A selenium based web crawler which gets you the top 100 attractions in a list of cities

The crawler_data.py scrapes the google things to do web site and saves each city's topp 100 attractions' names , rating and description

to run the chromedriver.exe and the input.csv should be in the same directory:
```
pip install requests selenium 
python3 crawler_data.py
```

The crawler_img.py fetches images for the city attractions in output.csv
to run :
```
python3 crawler_img.py
```
