import collections
import json_read 
import os
import process_terms

data_dir='../data/'

#check if query files have been made
def check_query_files():
    json_files=os.listdir(data_dir)
    json_len=len(json_files)-1
    query_files=os.listdir(data_dir+'queries/')
    query_len=len(query_files)-1
    if(query_len==json_len):
        json_files.remove('queries')
        return (json_len,json_files)
    else:
        json_files.remove('queries')
        build_query(json_files)
        return (json_len,json_files)

#build query files if not made
def build_query_files(files):
    for file in files:
        json_read.search_query(data_dir+file,True,data_dir+'queries/'+file.split('.')[0])

#display raw json format data or search queries of users
def display_data(files,ch):
    files=files.split(',')
    for file in files:
        print('Viewing data for: '+file)
        if(ch==1):
            out=json_read.raw_data(data_dir+file+'.json')
            print (out)
        elif(ch==2):
            json_read.search_query(data_dir+file+'.json')


#Menu of different fuctionalities for the data
def menu():
    print('Choose an option ')
    print('1) Display raw json data of person(s).')
    print('2) Display all search queries of person(s)')
    print('3) Display k-most used terms in search queries of users.')
    print('4) Display similarity of search terms in user queries.')
    print('5) Display k-most common term in search-results of users based on a search-query word/phrase.')
    print('6) Exit')
    ch = int(input("Enter choice number: "))
    return ch

#displays menu and driver functions
def main():
    num_users,users=check_query_files()
    print('There are '+ str(num_users) +' files with the search history of 5 people. They are\n')
    for user in users:
        print(user.split('.')[0])
    print('\n')

    while(True):
        ch=menu()
        if(ch==1):
            files=(input("Enter the name of files whose data is to be viewed. \nEnter names separated by comma: "))
            display_data(files,1)
        elif(ch==2):
            files=(input("Enter the name of files whose search queries are to be viewed.\nEnter names separated by comma: "))
            display_data(files,2)
        elif(ch==3):
            k = int(input("Enter k: "))
            common_lst=process_terms.most_used_terms(data_dir,k)
            process_terms.display_bar(common_lst)
        elif(ch==4):
            files=os.listdir(data_dir)
            files.remove('queries')
            person_lst=input("Enter the names of people whose search history is to be compared(Atleast 2).\nEnter names separated by comma: ")
            if(len(person_lst.split(','))>1 and len(person_lst.split(','))<=len(files)):
                similar_terms=process_terms.common_terms(person_lst)
                print('The common search-query terms for the above users are:\n')
                for terms in similar_terms:
                    print (terms)
            else:
                print('Invalid input')
        elif(ch==5):
            k = int(input("Enter k: "))
            print("Some of the most used words/phrases in search queries are:")
            common_lst=process_terms.most_used_terms(data_dir,k)
            recent=[]
            for person in (common_lst):
                for word,count in person:
                    if(count>10 and word not in recent):
                        print(word)
                        recent.append(word)
            search_term=input('Enter word/phrase to search results: ')
            result_lst=process_terms.search_results(data_dir,search_term,k)
            process_terms.display_bar(result_lst,search_term)
        elif(ch==6):
            break
        else:
            print('Input not recognized.')

        print("----------------------Press any key and <enter> to continue----------------------")
        inp=input("----------------------Press q and <enter> to exit----------------------\n")
        if(inp=='q' or inp=='Q'):
            break




main()


