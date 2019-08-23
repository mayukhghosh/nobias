import collections
import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import json_read

key_phrases_file = '../data/queries/key_phrases.txt'
queries_dir = '../data/queries/'
stopwords=['to','the','her','how','and','none','him','is','so','which','of','a','in','to','us','on','for','it']


#Finds common terms in search queries of users
def common_terms(files):
    terms=[]
    files=files.split(',')
    for i in range(len(files)):
        terms.append([])

    for i,file in enumerate(files,0):
        file = open(queries_dir+file+'.txt')
        a = file.read()
        # Instantiate a dictionary, and for every word in the file, 
        # Add to the dictionary if it doesn't exist. If it does, increase the count.
        wordcount = {}
        for word in a.lower().split():
            if word not in stopwords:
                terms[i].append(word)
    #Finds intersection of the sets where each set contains terms for a single person
    common=set(terms[0])
    for i in terms[1:]:
        common.intersection_update(i)
    return(common)




# This is a *crude* function which checks if two different words make better sense together by cheking the key_phrases_file. For eg. 'liz' and 'cheney'
# would make better sense as 'liz cheney'. Note: This only checks for pharases with 2 words only.
def search_keywords(words):
    f = open(key_phrases_file)
    a = f.read()
    lst = a.split(',')
    new_dict = {}
    cnt = 0
    flag = 0
    prev_wrd = ''
    prev_cnt = 0
    #print(words)
    for word,count in words:
        if (cnt==0):
            prev_wrd=word
            prev_cnt=count
            cnt=cnt+1
            continue
        flag=0
        if(count==prev_cnt and (prev_wrd+' '+word in lst)):
            new_dict[prev_wrd+' '+word] = count
            cnt=0
            flag=1
        else:
            new_dict[prev_wrd] = prev_cnt
            prev_wrd=word
            prev_cnt=count
        
    if(flag==0):
        new_dict[prev_wrd]=prev_cnt
        
    f.close()
    return new_dict

#searches all the queries of all the users and finds the k-most used terms in the queries
def most_used_terms(data_dir,k):
    files=os.listdir(data_dir)
    files.remove('queries')
    
    final_lst=[]
    for i in range(len(files)):
        final_lst.append([])

    files=os.listdir(queries_dir)
    files.remove('key_phrases.txt')
    
    for i,file in enumerate(files,0):
        file = open(queries_dir+file)
        a = file.read()

        # Instantiate a dictionary, and for every word in the file, 
        # Add to the dictionary if it doesn't exist. If it does, increase the count.
        wordcount = {}
        for word in a.lower().split():
            if word not in stopwords:
                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1

        #collections orders the dictionary with most-used terms first
        word_counter = collections.Counter(wordcount) 
        word_counter = search_keywords(word_counter.most_common())
        word_counter = collections.Counter(word_counter)
        word_counter = word_counter.most_common(k)

        for word, count in word_counter:     
            #print(word+" : "+ str(count))
            final_lst[i].append((word,count))
            """if (' ' in word):
                final_lst[i].append(word.split(' ')[0])
                final_lst[i].append(word.split(' ')[1])
                final_lst[i].append(word)
            else:
                final_lst[i].append(word)"""

 
    return final_lst

#searches for common terms in search-results of certain search queries
def search_results(data_dir,search_term,k):
    files=os.listdir(data_dir)
    files.remove('queries')
    results=[]
    final_lst=[]
    for i in range(len(files)):
        results.append([])

    #For search-results each title is only considered once,i.e, there is no repetition of titles as a user may visit the same page  more than once
    for cnt,file in enumerate(files,0):
        out=json_read.raw_data(data_dir+file)
        out=json.loads(out)
        for i in range(1,len(out['searchData'])):
            u=out['searchData'][i]['searchQueryString']
            if(u is None):
                continue
            if(search_term in out['searchData'][i]['searchQueryString']):
                v=out['searchData'][i]['searchResults']
                if(v is None):
                    continue
                recent=[]
                for j in range(len(out['searchData'][i]['searchResults'])):
                    title=out['searchData'][i]['searchResults'][j]['title']
                    if(cnt==0):
                        if(title not in recent):
                            results[cnt].append(title)
                            recent.append(title)
                            #print(file)
                            #print(title)
                    else:
                        for l in range(cnt):
                            if (title not in results[l]) and (title not in recent):
                                results[cnt].append(title)
                                recent.append(title)
                                #print(file)
                                #print(title)

    wordcount={}
    for i,person in enumerate(results,0):
        for title in person:
            for word in title.lower().split():
                word = word.replace(".","")
                word = word.replace(",","")
                word = word.replace(":","")
                word = word.replace("|","")
                word = word.replace("...","")
                word = word.replace("?","")
                word = word.replace("-","")
                word = word.replace("–","")
                if(word==""):
                    continue       
                if word not in stopwords:
                    if word not in wordcount:
                        wordcount[word] = 1
                    else:
                        wordcount[word] += 1
    

    word_counter = collections.Counter(wordcount)
    print('\nThe common terms in search-results are')
    for word, count in word_counter.most_common(k):     
        print(word, ": ", count)
        final_lst.append((word,count))
    
    return final_lst

#search for trends across time for a particular search-query term
def time_search(data_dir,search_term):
    files=os.listdir(data_dir)
    files.remove('queries')
    results=[]
    for i in range(len(files)):
        results.append({})

    for cnt,file in enumerate(files,0):
        out=json_read.raw_data(data_dir+file)
        out=json.loads(out)
        for i in range(1,len(out['searchData'])):
            u=out['searchData'][i]['searchQueryString']#search query string may not always be present in the data
            if(u is None):
                continue
            if(search_term in out['searchData'][i]['searchQueryString']):#timestamp may not always be present in the data
                if('timestamp' in out['searchData'][i]):
                    time=out['searchData'][i]['timestamp'].split('T')[0]
                    if(time not in results[cnt]):
                        results[cnt][time]=1
                    else:
                        results[cnt][time]+=1
    return (results)




# Create a data frame of the most common words 
# Draw a bar chart
def display_bar(lst,search_term=None):
    if(type(lst[0])==dict):#For displaying search trends across time
        not_avl=[]
        fig,ax=plt.subplots()
        for i,ts in enumerate(lst):
            if (ts):
                df=pd.DataFrame(list(ts.items()),columns=['Date','p'+str(i+1)])
                df['Date']=pd.to_datetime(df['Date'])
                df.set_index('Date',inplace=True)
                print(df)
                df.plot(ax=ax)
            else:
                not_avl.append(str(i+1))
        
        print('****************************')
        for i in not_avl:
            print('Data for p'+(i)+' not available.')
        print('****************************')
        plt.title('Search-query trend for "'+search_term+'"',fontsize=16)
        plt.show()
    elif(type(lst[0])==tuple):#For displaying search-results
        fig,axes=plt.subplots(nrows=1,ncols=1)
        df = pd.DataFrame(lst, columns = ['Word', 'Count'])
        df.plot.bar(ax=axes,x='Word',y='Count')
        fig.suptitle('Frequency of key-words in search results for "'+search_term+'"', fontsize=16)
        plt.show()
    else:#For displaying most used terms in search-queries
        fig,axes=plt.subplots(nrows=1,ncols=len(lst),figsize=(15,9))
        for i,person in enumerate(lst):    
            df = pd.DataFrame(person, columns = ['Word', 'Count'])
            df.plot.bar(ax=axes[i],x='Word',y='Count')
        fig.suptitle('Frequency of key-words in search queries for each person', fontsize=16)
        plt.show()
