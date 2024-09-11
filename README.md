# Elections-Scraper for Czech Republic's elections results
Python web scraper

Description of assignment
---
This application extracts and organizes data from the 2017 parliamentary election results. You can select any district to scrape data from the [official government website](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). The output will be a CSV file containing all the information needed for analysis.


Installation of libraries 
---
The packages used in this projects are located in the requirements.txt file.
To be able to install the used libraries, create a **virtual environment** and install the necessary packages:

```
$ pip3 --version # manager version verification

$ pip3 install -r requirements.txt # installing libraries
```

Starting the program 
---
To run the election.py file, you need to input 2 mandatory arguments.

python election.py <"url referring to the desired territory"> <"filename.csv">

```

python results.py "https://www.volby.cz/pls/ep2024/ep133?xjazyk=CZ&xnumnuts=2108" "Nymburk_results.csv"```





