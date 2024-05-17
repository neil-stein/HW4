# Neil Stein
# neilstein
# neil-stein

"""
INSTRUCTIONS

Available: May 9th at 11:59PM

Due: May 16th at 11:59PM

Gentle reminder that, among other things, you

(a) Must answer your questions in the homework4.py file
(b) Must commit homework4.py and movies.csv to your clone of the 
GitHub homework repo
(c) Must link your GitHub repo to GradeScope
(d) Must NOT repeatedly use a hard-coded path for the working directory

Failure to do any of these will result in the loss of points
"""

"""
HOMEWORK 4

You and your roommate have decieded to delve into the history of US cinema,
choosing a random blockbuster every Friday to watch. The problem, of course, is
that (a) you don't have a list of US blockbusters and (b) your roommate is 
indecisive and choosing a "random" movie to watch is going to be a nightmare!

Wikipedia to the rescue! It has a set of pages detailing all American films 
released in a particular year. For example:
    
    https://en.wikipedia.org/wiki/List_of_American_films_of_1982
    
You can look at different pages by changing the year at the end of the URL
e.g. replacing 1982 with 1997

At the top of these pages is a table containing the top 10 highest-grossing films 
for that year. The structure of this page is pretty stable - every such page from
1970 onwards has this table.

YOUR TASK

In this exercise, you will create a python program that will scrape 
each such page from Wikipedia for the period 1970 to 2023. Using this 
information it will create a dataset of all the top-grossing movies, then open
the dataset and pick a movie at random.

MANDATORY

Do not use the wikipeia package or API

Ensure that you insert a pause of 3 seconds between requests for 
data to wikipedia. 

By "create a dataset", we mean you must save the data to a CSV file named
"movies.csv". Then, open the CSV file and pick a movie at random. Print 
the name of the chosen movie with the year in brackets e.g. John Wick (2004)

The CSV file must include the following columns: Year, Rank, Title, 
Distributor, Domestic gross

SUGGESTED WORKFLOW

This is a somewhat complex project, so I recommend executing it in the following 
steps. Obviously, you don't have to execute in these steps - there is no way for
us to check!
    
    1. Write code that takes the URL for a particular year, fetches the html,
    and converts the relevant table into a list object.
    
    2. Create a function that takes a year as an input, generates the appropriate
    url, and uses the code from step (1) to fetch html and convert the relevant
    table.
    
    3. Write a loop that goes from 1970 to 2023 and uses the function from (2)
    to add the data to a final_table list object. Use the sleep() method from
    the time package to ensure that you take a 3 second break between requests
    
    4. Convert final_table into a dataframe df; save it as a CSV
    
    5. Open the CSV and pick a random movies
    
HINTS

Hints for step 1:
    - Start with 1970, and make sure your code is working before you proceed
    - Be careful - there are many tables on this page, and the one
    you are looking for isn't the first one!
    - Don't forget to deal with the row that says "Rank", "Title" etc.
    - The table merges cells when the distributor is the same. For example, in
    1970, both MASH and Patton were distributed by 20th Century Fox, so the two
    cells are merged. For example, when converting the table to a list, the 
    entry for 'Patton' will not include the distributor, resulting in a row 
    shorter than expected.. Think of a way to deal with this!
    - Don't forget to add a Year "column"

Hints for step 2: 
    - You can copy paste the code from step 1 into this function
    and make a few changes to complete this step
    - Remember that the URL must be a string object even if the incoming year
    variable is an int
    
Hints for step 3:
    - Use the sleep() method from the time package to add a pause
    - For your peace of mind, print a note at the start of each iteration so that
    you know that it is working
    - Don't try to iterate over everything at once! Try 1970, then 1970 to 1971
    and so on till you are comfortable running it for 1970 to 2023
    
Hints for step 4:     
    You will know  your program works as intended if print(df.head()) generates
the following output:
    
      Rank           Title       Distributor Domestic gross  Year
    0    1      Love Story         Paramount   $106,397,186  1970
    1    2         Airport         Universal   $100,489,150  1970
    2    3         M*A*S*H  20th Century Fox    $81,600,000  1970
    3    4          Patton  20th Century Fox    $62,500,000  1970
    4    5  The Aristocats       Walt Disney    $41,162,795  1970

and print(df.tail()) generates the following output:
    
print(df.tail())
     Rank                              Title  ... Domestic gross  Year
525     6                 The Little Mermaid  ...   $298,172,056  2023
526     7                              Wonka  ...   $218,377,073  2023
527     8  Ant-Man and the Wasp: Quantumania  ...   $214,506,909  2023
528     9               John Wick: Chapter 4  ...   $187,131,806  2023
529    10                   Sound of Freedom  ...   $184,174,617  2023

Hints for step 5:
    - Use the random package
    - What kind of indexes does your data have?
"""
# set-up steps

import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

"""
step 1 - using the URL to pull information and storing in a list
"""

url = "https://en.wikipedia.org/wiki/List_of_American_films_of_1970"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")
print("Number of tables = ",len(tables))

# with the number of tables, find the correct one to pull from
table = tables[1]
print(table)

# with the correct number, begin to structure the pulling of information

movie_data = [] 

for i, row in enumerate(table.find_all("tr")):
    cells = row.find_all(['td']) 
    cleaned_row = []
    year = (url[-4:])
    if len(cells) > 2:        
        for cell in cells:
            cleaned_text = cell.text.strip().replace('\n', ' ')
            cleaned_row.append(cleaned_text)
        cleaned_row.insert(3, year)
        movie_data.append(cleaned_row)

    elif len(cells) == 2:
        title = cells[0].text.strip().replace('\n', ' ')
        distributor = movie_data[-1][1]
        domestic_gross = cells[1].text.strip().replace('\n', ' ')
        year = (url[-4:])
        movie_data.append([title, distributor, domestic_gross, year])

"""
step 2 - gathering all of our data
"""

# creating our list of URLs

url_list = []
for i in range(0, 55):
    year = 1970 + i
    url = f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}"
    url_list.append(url)

# next, defining our function

def movie_scrape(url):
    movie_data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    year = (url[-4:])
    tables = soup.find_all("table")
    if len(tables) > 1:
        table = tables[1]    
    
        for i, row in enumerate(table.find_all("tr")):
            cells = row.find_all(['td']) 
            cleaned_row = []
            if len(cells) > 2:        
                for cell in cells:
                    cleaned_text = cell.text.strip().replace('\n', ' ')
                    cleaned_row.append(cleaned_text)
                cleaned_row.insert(3, year)
                movie_data.append(cleaned_row)
    
            elif len(cells) == 2:
                title = cells[0].text.strip().replace('\n', ' ')
                distributor = movie_data[-1][1]
                domestic_gross = cells[1].text.strip().replace('\n', ' ')
                movie_data.append([title, distributor, domestic_gross, year])
    else:
        return print(f"Data table not found for {year}")
    return movie_data

"""
step 3 -- looping over the time range
"""


# empty data frame for storage

df_films = pd.DataFrame(columns= ["Title","Distributor","Domestic_Gross","Year"])

for i in range(0, 54):
    year = 1970 + i
    url = (f"https://en.wikipedia.org/wiki/List_of_American_films_of_{year}")
    film_data = movie_scrape(url)
    if film_data:
        df_films = pd.concat([df_films, pd.DataFrame(film_data, columns=["Title", "Distributor", "Domestic_Gross", "Year"])], ignore_index=True)
    else:
        print(f"Data table not found for {url}")
    time.sleep(3)
        
# Quality Check 
df_films.head()

# data improvements - restoring missing rank labels
num_rows = df_films.shape[0]
ranks = list(range(1, 11))*(num_rows// 10 + 1)
ranks = ranks[:num_rows]
ranks = pd.to_numeric(ranks)
df_films.insert(loc = 0, column= "Rank", value= ranks)


"""
step 4 - converting our dataframe to CSV
"""
# conversion to a dataframe took place in the previous step to improve the code's efficiency
# converting at this step does not work well on my computer's processing capacity

df_films.to_csv(r"/Users/neilstein/Documents/Academic/Spring 24/Python I/Homework/HW4/movies.csv")


"""
Step 5 - random movie selector
"""
#set-up steps
import pandas as pd
import os

# re-loading in our csv from the same folder we left it in earlier
path = os.path.join(r"/Users/neilstein/Documents/Academic/Spring 24/Python I/Homework/HW4/", "movies.csv")
films = pd.read_csv(path)


# picking random movies -- the prompt does ask for plural, this is written to allow for that!

def random_movies(num_movies):
    max_movies = len(films)
    num_movies = max(1, min(num_movies, max_movies))
    if num_movies != max_movies:
        print(f"Notice: Only {max_movies} movies are available. Selecting {num_movies} random titles.")
    random_movies = films.sample(num_movies)
    return random_movies["Title"].tolist()


try:
  num_movies_str = input("Enter the desired number of random movies (between 1 and {}): ".format(len(films)))
  num_movies = int(num_movies_str)

  random_movie_titles = random_movies(num_movies)

  print(f"\nSelected Movie Titles:")
  for title in random_movie_titles:
    print(title)
except ValueError:
  print("Invalid input. Please enter an integer.")
