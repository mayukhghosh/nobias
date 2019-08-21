# Data visualization of search history

This program visualizes search history data stored in .json files. The main features of this program are:\
* Find the k-most used terms in search-queries of all the users.
* Find the similarity of search terms among users.
* Find the k-most common terms in search results of users based on a search query word/phrase.
* View raw json data of person(s).
* View the search queries of person(s).
 

## Pre-requisites

Python 3.7\
Pandas\
numpy

```bash
pip install foobar
```
## Json format
The data is in the following format:
* userID (string): A random id assigned to each user
* searchData (list/array): A list of json objects, where each object represents a page of google search results
  * searchQueryPageNum (float): The page number from google search 
  * searchQueryString (string): The query entered into google search
  * hostname (string): The host url, it should be google.com, feel free to ignore
  * timestamp (string): UTC formatted timestamp string of when the search was done
  * searchResults (list/array): A list of json objects, where each objects contains a single news article from the search page
    - title (string): The title of the news article
    - url (string): The url of the news article

Note: The timestamp field is missing in some of the files.

The .json files are stored in `\data\`.

## Usage
The program can be run by simply executing the `main.py` from the `src\` folder like this:
```python
python main.py
```
Following which, the name of the various data files containing the search histories will be shown along with a menu which will have various options to explore the data. This is the output when the above command is  run:
```shell
There are 5 files with the search history of 5 people. They are

p1
p2
p3
p4
p5


Choose an option
1) Display raw json data of person(s).
2) Display all search query results of person(s)
3) Display k-most used terms in search queries of users.
4) Display similarity of search terms in user queries.
5) Display k-most common term in search-results of users based on a search-query word/phrase.
6) Exit
Enter choice number:
```

One can choose any of the options to view particular trends in the search history data.

For example, the following shows the output when the user chooses 4 as his choice.

```shell
Enter choice number: 4
Enter the names of people whose search history is to be compared(Atleast 2).
Enter names separated by comma: p3,p4,p5
The search-query terms in common for the above users are:

passes
votes
acosta
wage
booker
election
scalia
liz
cheney
house
congresswoman
harris
2020
condemn
eugene
biden
aoc
trump
bill
alexander
minimum
----------------------Press any key and <enter> to continue----------------------
----------------------Press q and <enter> to exit----------------------
```
Note that `p3,p4,p5` in the third line is entered by the user.

If the user chooses option 3, the following is the output:
```bash
Enter choice number: 3
Enter k: 10
```
`k` is entered by the user which indicates that the top 10 common search-query terms are shown. The following figure is also shown.

![Image](images/query_common.png)

