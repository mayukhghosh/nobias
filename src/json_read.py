import json
import io

#searches search-queries in a particular json file.
def search_query(file,write=False,loc=''):
	if(write==True):
		f_query=open(loc,'w+')
	with io.open(file,encoding='utf-8') as f:
		data=json.load(f)
	out=(json.dumps(data, indent=4, sort_keys=False))
	out=json.loads(out)
	for i in range(1,len(out['searchData'])):
		if(out['searchData'][i]['searchQueryString']!='None'):
			print(out['searchData'][i]['searchQueryString'])
			if(write==True):
				f_query.write(str(out['searchData'][i]['searchQueryString'])+' ')

	if(write==True):
		f_query.close()


#returns raw json data
def raw_data(file):
	with io.open(file,encoding='utf-8') as f:
		data=json.load(f)
	out=(json.dumps(data, indent=4, sort_keys=False))
	return out



