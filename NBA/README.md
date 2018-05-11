# NBA Files
A series of files to perform specific NBA analysis or prediction tasks.

## grantland_shot_chart.py
Most of this has been taken from [doingthedishes](http://www.eyalshafran.com/scraping_basketball_reference.html) (a fabulous site for learning this stuff). The problem is that he uses NBAapi to scrape data, and I don't want to depend on that. Therefore, I am using it to learn from while I try to build my own scraper using Beautiful Soup and other libraries. 

## scrape_bball_ref.py
This is my playground for using BeautifulSoup and other files to scrape data from [basketball-reference.com](https://www.basketball-reference.com/). The player_info and player_detailed_info are from [doingthedishes](http://www.eyalshafran.com/scraping_basketball_reference.html), the rest are my own. (Using anything but the first table on a particular page of their website can be tricky).

## sports_vu_playground.py
Sports Vu data used to be freely available to the public but was taken away a couple years ago. Thankfully [neilmj's github](https://github.com/neilmj/BasketballData) contains like 600 games worth. Since I'm fascinated by improving the efficiency of, and finding patterns in human movement with machine learning, I figured his dataset would be a great place to start learning.

I came across [Dan Vatterott's Github](https://github.com/dvatterott) and found a great deal of code to learn from. I've used a bunch of his code as a starting place, then re-arranged things and added features to keep learning more.

So far I've matched the sports_vu data up with play by play data from stats.nba.com. Next I need to figure out how to make an animation at all, haha.