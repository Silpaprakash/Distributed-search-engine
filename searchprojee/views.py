from django.shortcuts import render

from django.http import HttpResponse

from django.template.loader import get_template

from django.template import Context


import urllib
import re
import time

def get_page(url):            
    try:
        f=urllib.urlopen(url)
        page=f.read()
        f.close()
        
        return page
       
    except:
       return ""

def get_next_url(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    page = page[start_quote + 1:end_quote]
    return page, end_quote


def get_all_links(page): 
    link = []
    while True:
        url, endpos = get_next_url(page)
        if url:
            link.append(url)
            page = page[endpos:]
        else:
            break
    
    return link



def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)




def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
     
def add_to_index(index, keyword, url):
    if  not isvalid(keyword) and  not iscommon(keyword):
        if keyword in index and not isduplicate(keyword,index,url):
            
            index[keyword].append(url)
        else:
            index[keyword] = [url]
           
def isvalid(test_str):  
    
    pattern = r'[^a-zA-Z]'
    if re.search(pattern, test_str):
        return True
    else:
        return False

def isduplicate(keyword,index,url): 
    if url in index[keyword]:
        return True
    return False        


            


def Look_up(index, keyword): 
    if keyword in index:
        return index[keyword]
    else:
        return None

def compute_ranks(graph):
    start_time=time.clock()
    d = 0.8 
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for p in graph:
               if page in graph[p]:
                   newrank+=d*ranks[p]/len(graph[p])
            newranks[page] = newrank
        ranks = newranks
    
    
    return ranks,time.clock()-start_time


def profile(index):
    count=0
    for key in index:
        print "KEYWORD  :",key, "URL LIST",index[key]
        count+=1
        if count==10:
            return None

def iscommon(keyword):
    common=['the','be','and','of','a','in','to','have','to','it','I','that','for','you','he','with','there','is','was','me']
    if keyword in common:
        return True
    return False

def best_rank(rank):
    bestkey=""
    maxi=0

    for key in rank:
        if rank[key]>maxi:
            bestkey=key
            maxi=rank[key]
    return key,rank[bestkey]
def sortprofile(index):
    max=0
    for key in index:
        if max<len(index[key]):
            max=len(index[key])
    length=max
    count=0
    while count<10:
        for key in index:
            if len(index[key])==length:
                print "KEY:", key ,"    VALUE:", index[key]
                count+=1
                if count>=10:
                    break
        length-=1    
        
        
    
        
def crawl_web(seed,max_pages,max_depth):
    start_time=time.clock()
    tocrawl = [seed]
    count =0
    crawled = []
    graph = {}  
    index = {}
    next_depth=[]
    depth=0
    while tocrawl and  len(crawled)<max_pages and depth<=max_depth: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(next_depth,outlinks)
            crawled.append(page)                           
        if not tocrawl:
             tocrawl,next_depth=next_depth,[]
             depth+=1
    total_crawling_time=time.clock()-start_time        
    return index,total_crawling_time,graph



from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import Template,Context
from indexbookcreator import *
from models import *
def contact(request):
    f = open('C:\myprojee\searchprojee\myfile','w')
    
    errors = []
    
    if request.method == 'POST':
        if not request.POST.get('seed', ''):
            errors.append('Enter a seed page.')
        if not request.POST.get('depth', ''):
            errors.append('Enter a maximum depth.')
        if not request.POST.get('pages'):
            errors.append('Enter a maximum pages')
        if not errors:
          try:
            i,crawl_time,graph=crawl_web(
                request.POST['seed'],
                int(request.POST['pages']),
                int(request.POST['depth']),
            )
            ranks,ranking_time=compute_ranks(graph)
            stri =""
            rank=""
            for keyword in  i:
                p=index_tbl(key=keyword,value=i[keyword])
                p.save()
                f.write(keyword+" ")
                f.write(str(i[keyword][0])+"\n")
                stri+=keyword+ "        "+str(i[keyword])
            f.close()
            #execfile("C:\myprojee\searchprojee\indexbookcreator.py")
            
            for key in  ranks:
                rank+=key+ "        "+str(ranks[key])
            indexbook()
            return render(request, 'contact_form.html',{'value': i,'rank': rank ,'time': crawl_time, 'rank_time':ranking_time})
          except Exception, err: 
            return HttpResponse(str(err))
    return render(request, 'contact_form.html',
        {'errors': errors})












