import urllib, sgmllib
common = ['and', 'if', 'a', 'or', 'also', 'with', 'is', 'has', \
				'for', 'to', 'in', 'how', 'on', 'here', 'html', 'of', 'you', \
				'that', 'an', 'be', 'by', 'http', 'href', 'id', 'more', 'link', \
				'title', 'style', 'head', 'body', 'much', 'the', 'type', 'src', 'img',\
				'javascript', 'DOCTYPE', 'noscript']
common_c = list([w.capitalize() for w in common])	
common_words = set(common).union(common_c)
	
class MyParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []
    

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."
        for name, value in attributes:
            if name == "href" and value[0:5]=="http:":
                self.hyperlinks.append(value)
            
    def get_hyperlinks(self):
        "Return the list of hyperlinks."
        return self.hyperlinks

def get_page (url, tag="*"):
  try:
    #print "{0}:reading {1}...".format(tag, url)
    f = urllib.urlopen(url)
    s = f.read()
    return s
  except IOError as e:
    #print "{0}:I/O error({0}):{1}".format(tag, e.errno, e.strerror)
    return False
  except:
    #print "{0}:Unexpected error:{1}".format(tag, sys.exc_info()[0])
    return False


from string import translate, maketrans, punctuation 
def split(txt):
  T = maketrans(punctuation, ' '*len(punctuation))
  return translate(txt, T).split()
def common_word(keyword):
    c=['the','was','you','if','of','var','from','search','else','by','solid','is','we','an']
    if keyword in c:
        return False
    return True    


def valid(test_string):
    import re
    pattern = r'[^a-zA-Z]'
    if re.search(pattern, test_string):
       return False
    else:
        return True


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
def is_valid_keyword (s):
	return is_number(s)
    
def add_urls_to_index(index, keyword, set_of_urls):
  if keyword in index:
    index[keyword] = index[keyword].union(set_of_urls)
  else:
    index[keyword] = set_of_urls
def add_to_index(index, keyword, url):
    keyword=keyword.lower()
    if valid(keyword)and common_word(keyword) and len(keyword)>2:
        if keyword in index:
            if url not in index[keyword]:
                index[keyword].add(url)
        else:
            index[keyword] = url
    return True
def add_page_to_index(index, url, content):
	global common_words  # this is initialized in crawl_init as a set
	count = 0
	words = set(split(content))
	words.difference_update(common_words)#return set word after removing elements found in t
	for word in words:
		if add_to_index(index, word, url):
			count += 1
	return count

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None
				  
def extract_tag (str):
	str = str.upper()
	first = str.find(".")
	second = str.find(".",first+1)
	return str[first+1:second]

def crawl_init (seed_list):
	global counter, single_seed, d_count, max_count
	tocrawl = set([])
	counter.value += 1
	tag = "P"+str(counter.value)
	while seed_list:
		url = seed_list.pop()
		tocrawl.add(url)
		if single_seed.value == False:
			tag = tag + "." + extract_tag(url)

	if d_count.value:
		max_depth = d_count.value
		#print "max_depth",max_depth
	if max_count.value:
		max_links = max_count.value	  
	
	
	global common_words
	common = ['and', 'if', 'a', 'or', 'also', 'with', 'is', 'has', \
				'for', 'to', 'in', 'how', 'on', 'here', 'html', 'of', 'you', \
				'that', 'an', 'be', 'by', 'http', 'href', 'id', 'more', 'link', \
				'title', 'style', 'head', 'body', 'much', 'the', 'type', 'src', 'img',\
				'javascript', 'DOCTYPE', 'noscript']
	common_c = list([w.capitalize() for w in common])	
	common_words = set(common).union(common_c)
	
	return tocrawl, tag, max_depth, max_links
	
def crawl_web1(seed_list, max_depth=2, max_links=5): # returns index, graph of inlinks
   
    tocrawl, tag, max_depth, max_links = crawl_init(seed_list)
          
    #print "*** Process tagged with {0}, depth {1}, max {2} ".format(tag, max_depth, max_links)
    
    crawled, next_depth, crawl_len, depth, parseErr = [], set([]), 0, 0, 0
    graph = {}  
    index = {}  
    myparser = MyParser()
    
    while tocrawl and depth <= max_depth and crawl_len < max_links:
      page = tocrawl.pop()
      content = get_page(page, tag)
      if content != False:
        try:
          myparser.parse(content)
          wcount = add_page_to_index(index, page, content)
          outlinks = myparser.get_hyperlinks()          
          graph[page] = outlinks
          next_depth.update(outlinks)
        except:
          #print "{0}:Unexpected Parser error: {1}".format(tag, sys.exc_info()[0])
          parseErr += 1
          pass     
        crawled.append(page)
        crawl_len = len(crawled)
        if not tocrawl:
          tocrawl, next_depth = next_depth, set([])
          depth = depth + 1        
    #print "\n------------------------------------------"	
    #print "*** Process {0} done *** index size:{1}, graph size:{2}, ParseErr:{3}".format(tag, len(index), len(graph), parseErr)
    #print "------------------------------------------"	
    return (index, graph, tag)

def lucky_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    samples = []
    if pages:
        i = iter(pages)  
        bestpage = i.next()
        for candidate in pages:
            if ranks[candidate] > ranks[bestpage]:
                bestpage = candidate
        if len(pages) >= 4:
          for c in range(1,4):
            s = i.next()
            if s != bestpage:
              samples.append(s)
        else:
          samples = pages
        return str(ranks[bestpage]*100)[:9], bestpage, samples
    else:
        return None
def profile_index(index, ranks):
    max = 0
    for e in index:
        if len(index[e]) > max:
            max = len(index[e])
            #print "{0} {1} {2}".format(e[:15].rjust(15), \
				#str(max).ljust(5), lucky_search(index,ranks,e)[0:2])

from datetime import datetime

def p_compute_ranks(c):
	global rgraph, rranks
	
	# prepare for parallelizing the rank computation	
	rranks = {}
	start = time.clock()
	#npages = len(rgraph)
	npages=len(rgraph)
	for page in rgraph:
		rranks[page] = 1.0/npages
	
	numloops = 5
	rgraph_keys = rgraph.keys()
	chunksize = len(rgraph_keys)/c
	
	#print "RankCal. initated @ {0}...".format(datetime.time(datetime.now()))
	for i in range (0, numloops):
		pool = Pool (processes=c, initializer = initranks, initargs = (counter, rgraph, rranks))		
		partitioned_keys = list(chunks (rgraph_keys, chunksize))
		results = pool.map(p_compute_new_ranks, partitioned_keys)
		for r in results:
			tag, newranks = r[0], r[1]
			rranks.update(newranks)
		#print "Loop of {0}/{1} done @ {2}".format(i+1, numloops, datetime.time(datetime.now()))
	ranktime=time.clock() - start
	print "Rank Calculation Time :",ranktime
	return ranktime,rranks
	
def p_compute_new_ranks(keys):
    global counter, rgraph, rranks
    counter.value += 1
    tag = "P:{0}".format(counter.value)
    d = 0.8 # damping factor
    npages = len(rgraph)
    
    newranks = {}
    for page in keys:
        newrank = (1 - d) / npages
        for node in rgraph:
            if page in rgraph[node]:
                try:
                    newrank = newrank + .8 * (rranks[node] / len(rgraph[node]))
                except:
                    #print "Error in line 329 newrank calculation"
                    continue
        newranks[page] = newrank
    
    return tag, newranks

def test_difference():
	i1 = {1:1, 2:2, 3:3}
	i2 = {1:1, 4:4, 5:5}
	# new set with elements in i2 but not in i1
	new_keys = set(i2.keys()).difference(i1.keys()) 
	# set([4, 5])

	
def merge_indexes(i1, i2):
  new_keys = set(i2.keys()).difference(i1.keys())
  for k in new_keys:
    add_urls_to_index(i1, k, i2[k])
  return i1
  
  
def chunks(l, n):
	for i in xrange(0,len(l),n):
		yield l[i:i+n] # instantly makes chunks a "generator function" instead of a normal function
	  
def c_ig(results):
    global rgraph
    start = time.clock()
    rgraph = {}
    for index, graph, rtag in results:
        rgraph.update(graph)
        rindex = reduce(merge_indexes, [i for i, g, t in results])
    #print "consolidated index:\n",rindex
    #print "consolidated graph:\n",rgraph  
    end =time.clock()-start
    #print "end time:",end
    return rindex,rgraph
	  
import os, sys, time, inspect
from multiprocessing import Process, Pool, Value
counter = None
single_seed = None
d_count = None
max_count = None
rgraph = None
rranks = None
def init(arg0, arg1, arg2, arg3):
    global counter, single_seed, d_count, max_count
    counter, single_seed, d_count, max_count = arg0, arg1, arg2, arg3 
def initranks(arg0, arg1, arg2):
	global counter, rgraph, rranks
	counter, rgraph, rranks = arg0, arg1, arg2

def set_parameters (cArgs):
	global d_count, max_count, single_seed
	
	single_seed = Value('b',True)
	seed_page = "http://www.google.com"
	if len(cArgs) > 0:
		#print "cArgs:", cArgs
		if cArgs[0] == "-n" and len(cArgs[1]):
			c = int(cArgs[1])
			#print "No of processes", c
		if cArgs[2] == "-m" and len(cArgs[3]):
			#max_count = Value ('i', 10)
			max_count = Value("i",int(cArgs[3]))
			#print "max_page",max_count.value
		if cArgs[4] == "-d" and len(cArgs[5]):
			#d_count = Value('i', 5)
			d_count = Value('i',int(cArgs[5]))
			#print "max_depth",d_count.value
		if cArgs[6] == "-s" and len(cArgs[7:]) == 1:
			single_seed = Value('b',True)
			seed_page = cArgs[7]
			#print "seed_page:", seed_page
		elif cArgs[6] == "-s" and len(cArgs[7:]) > 1:
			single_seed = Value('b', False)
			seed_page = None
			links = list(cArgs[7:])
			#print "links:", links
    
	else:
		c = 4 
		max_count = Value ('i', 10)  # overriding the default of max_links = 10
		d_count = Value('i', 5) # overriding the default of max_depth = 3
		seed_page ='http://www.google.com'
		single_seed = Value('b',True)
	
	if single_seed.value:
		tag = extract_tag(seed_page)
		try:         
			content = get_page(seed_page, tag)	
			myparser = MyParser()
			myparser.parse(content)
			links = myparser.get_hyperlinks()
		except:
			#print "{0}:Unexpected Parser error:{1}".format(tag, sys.exc_info()[0])
			sys.exit()		

	return c, seed_page, links

if __name__=='__main__':
    f=open("C:\\myprojee\\searchprojee\\consoli_index.txt","w")
    rank_write=open("C:\\myprojee\\searchprojee\\consoli_rank.txt","w")
    cargs = sys.argv[1:]
    v = set_parameters(cargs)
    c, seed_page, seed_links = v[0], v[1], v[2]
    #print "c, seed_page, seed_links:", c, seed_page,seed_links
    chunksize = len(seed_links)/c
    if chunksize < 1:
        chunksize = 1	
    counter = Value('i',0) # useful for tagging processes with a number when using single_seed
    pool = Pool (processes=c, initializer = init, initargs = (counter, single_seed, d_count, max_count ))
    partitioned_links = list(chunks (seed_links, chunksize))
    nchunks = len(partitioned_links)
    #print partitioned_links
    #print "Processes=",c
    #print "links/c", chunksize
    #print "No of chunks:", nchunks
    start = time.clock()
    results = pool.map(crawl_web1, partitioned_links)
    #print results
    console_index,console_graph=c_ig(results)
    #print "CONSOLIDATED INDEX:",console_index
    #print "CONSOLIDATED GRAPH:",console_graph
    for s in str(console_index):
        f.write(s)
    f.close()
    rank_time,rranks=p_compute_ranks(c)
    #print rranks
    for line in str(rranks):
        rank_write.write(line)
    rank_write.close()
    
    t=time.clock() - start
    output="CRAWLING TIME "+str(t)
    print output
    	#print "time:\n",t
"""
        #console_index,console_graph=c_ig(results)
	#print "CONSOLIDATED INDEX:",console_index
	#print "CONSOLIDATED GRAPH:",console_graph
	#print c_rank(results)
"""



	
