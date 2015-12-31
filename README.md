# eBay  web Scraper

## Overview
Problem: There are a lot of records I want. As much as I would like to, I do not have time to constantly search eBay for them. Also, a good portion of my want list are rare titles that: do not come up for auction very often thus searching for them typically yields no results. Solution: Remove myself from the equation; Create a list of search queries, search eBay automatically, and return a list of results. Sounds like a perfect job for a web scraper.

## Details
First, the easy part, I made a plain text file of searches I want to perform. Then, for each search query I use Mechanize to traverse and search eBay and Beautiful Soup to parse the page of search results. After the results are collected, the gspread library posts them to a Google Spreadsheet. Finally, if there are any rare matches, the program will tweet me.

## Notes
I have excluded the json file that contains my Google API credentials :)
