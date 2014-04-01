from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from py2neo import neo4j
from py2neo import node, rel
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Template
from models import *
from indexbookcreator import *
from tagcloudcreator import *
from django.db import *


graph_db = neo4j.GraphDatabaseService()
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
    keyword=keyword.lower()
    if  not isvalid(keyword) and  (not iscommon(keyword)) and len(keyword)>2:
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
    common=['the','be','and','of','a','in','to','have','to','it','I','that','for','you','he','with','on','do','say','this','they','at','but','we','his','from','that','not',"n't",'by','she','or','as','what','go','their','can','who','get','if','would','her','all','my','make','about','know','will','as','up','one','time','there']
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

def Similar_Keyword_Search(index):
        neo4j_insert_time=time.clock()
        ind_1={}
        ind_2={}
        politics_new=[]
        sports_new=[]
        google_new=[]
        news_new=[]
        others=[]

        politics_array=['CPI','Communist','votes','cash','win','Card','ministry','India','Products','Party','Shinde','AP','Congress','seat','Corruption','Sabha','BJP','AAP','BSP','election','vote','elects']
        prgm_array=['C','function','search','new','Java','C++','C#','PHP','Python','Javascript','Ruby','Perl','Pascal','MATLAB','PL/SQL','Lisp','Visual Basic']
        #google_array=['function', 'search', 'removed', 'from', 'solid', 'offered', 'else']
        sports_array=['cricket','tennis','South','directors','rules','Games','instructions','football','Chennai','captain','team','New','Amazon','coach','match','hockey','badminton','sachin','batsmen','ball','wicket','bowler','umpire','goal','kickoff','olympics','fifa']
        news_array=['india','state','international','Smartphone','TV','centre','sports','cash','minister','Group','Institute','issues','social','register','People','climate','advertisement']
        key=index.keys()
        #print key
        for keyword in key:
            if keyword in politics_array:
                politics_new.append(keyword)
            if keyword in sports_array:
                sports_new.append(keyword)
            if keyword in news_array:
                news_new.append(keyword)
            else:
                others.append(keyword)

        f=open("index_1.txt","w")
        
        print politics_new
        for i in politics_new:
            f.write(i+"\n")
        print "****************************************************"
        insert_data1(politics_new,index)


        print sports_new
        for i in sports_new:
            f.write(i+"\n")
        print "****************************************************"
        insert_data1(sports_new,index)

        print news_new
        for i in news_new:
            f.write(i+"\n")
        print "****************************************************"
        insert_data1(news_new,index)
        


        print "****************************************************"
        insert_data1(others[0:20],index)
        f.close()
        neo4j_insert_time=time.clock()-neo4j_insert_time
        return neo4j_insert_time
       
def insert_data1(li,index):
        f=open("C:\myprojee\\file.txt","w")
        data_array=[]
        a=[]
        count=1
        i=0
        j=1
        if len(li)>2:
            for key in li:
                a.append(key)
                #print key," " ,index[key]
            database_nodes=graph_db.create(
                node({"Keyword":"PARENT"}))
            for key in li:
                database_nodes1=graph_db.create(
                node({"Keyword":key,'URL':index[key]}),
                rel(database_nodes[0], "LINKS",0))
                count+=1
                if count == len(li):
                    break
                print database_nodes1
                f.write(str(database_nodes1)+"\n")
                
        f.close()
                 
        
    
        
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

    









def contact(request):
    f=open('C:\myprojee\searchprojee\myfile.txt','w')
    key_write=open('C:\myprojee\searchprojee\keywords','w')
    errors = []
    lookup_res=""
    if request.method == 'POST':
        if not request.POST.get('seed', ''):
            errors.append('Enter a seed page.')
        if not request.POST.get('depth', ''):
            errors.append('Enter a maximum depth.')
        if not request.POST.get('pages'):
            errors.append('Enter a maximum pages')
        if not request.POST.get('lookup_keyword'):
            errors.append('Enter a lookup keyword')
        
        if not errors:
          try:
            if request.POST.get('Radio1')=='bs':
                #print request.POST.get('Radio1')
                i,crawl_time,graph=crawl_web(
                request.POST['seed'],
                int(request.POST['pages']),
                int(request.POST['depth']),
            )
            
            
            lookup_res=str(index_tbl.objects.filter(key__startswith=str(request.POST['lookup_keyword'])))
            if index_tbl.objects.filter(key__startswith=str(request.POST['lookup_keyword'])==0):
                lookup_res+=str(Look_up(i,str(request.POST['lookup_keyword'])))
            ranks,ranking_time=compute_ranks(graph)
            stri =""
            rank=""
            for keyword in  i:
                p=index_tbl(key=keyword,value=i[keyword])
                
                p.save()
                
                f.write(keyword+" ")
                f.write(str(i[keyword][0])+"\n")
                key_write.write(keyword+"\n")
                stri+=keyword+ "        "+str(i[keyword])
            f.close()
            key_write.close()
            indexbook(i)
            
            Similar_Keyword_Search(i)
            createtagcloud(i)
            #execfile("C:\myprojee\searchprojee\indexbookcreator.py")
            length_index=len(i)
            for key in  ranks:
                rank+=key+ "        "+str(ranks[key])
            
            return render(request, 'contact_form.html',{'value': i,'rank': rank ,'time': crawl_time, 'rank_time':ranking_time,'len_index':length_index,'lk_res':lookup_res})
          except Exception, err: 
            return HttpResponse(str(err))
    return render(request, 'contact_form.html',
        {'errors': errors})




def indexbk(request):
    data=""
    return render(request, 'indexbook.html', data)

def dataoperations(request):
    return render(request, 'databaseop.html', data)


def tagcloudview(request):
    data=""
    return render(request, 'tagcloud.html', data)

def stattable(request):
    data=""
    return render(request, 'stat.html', data)
def sqlite_insert(index):
    sqlite_insert_time=time.clock()
    for keyword in  index:
        s=index_tbl.objects.filter(key=keyword)
        if s.count()==0:
            p=index_tbl(key=keyword,value=index[keyword])
            p.save()
    sqlite_insert_time=time.clock()-sqlite_insert_time
    return sqlite_insert_time 


import subprocess

def bootstrap(request):
    f=open('C:\myprojee\searchprojee\myfile.txt','w')
    key_write=open('C:\myprojee\searchprojee\keywords','w')
    errors = []
    lookup_res=""
    neo4j_insert_time=0.0
    sqlite_insert_time=0.0
    if request.method == 'POST':
        if request.POST.get('lookup_keyword') and not request.POST.get('seed', '') and not request.POST.get('depth', '') and not request.POST.get('pages'):
            lookup_res=str(index_tbl.objects.filter(key__startswith=str(request.POST['lookup_keyword'])).distinct())
            #lookup_res+="<br><br><br><br>"
            
            return render(request, 'bootstrap.html',{'lk_res':lookup_res})
        if request.POST.get('seed', '') and  request.POST.get('depth', '') and request.POST.get('pages'):
          try:
            if request.POST.get('Radio1')=='bs':
                #print request.POST.get('Radio1')
                i,crawl_time,graph=crawl_web(
                request.POST['seed'],
                int(request.POST['pages']),
                int(request.POST['depth']),
            )
                if request.POST.get('lookup_keyword'):
                    lookup_res=str(index_tbl.objects.filter(key__startswith=str(request.POST['lookup_keyword'])).distinct())
                    if len(lookup_res)==0:
                        lookup_res+=str(Look_up(i,str(request.POST['lookup_keyword'])))
                ranks,ranking_time=compute_ranks(graph)
                stri =""
                rank=""
                if request.POST.get('database1')=="sql":
                    sqlite_insert_time=sqlite_insert(i)
                    #sqlite_insert_time=time.clock()-sqlite_insert_time
                f.close()
                key_write.close()
                indexbook(i)
                if request.POST.get('database2')=="neo":
                    neo4j_insert_time=Similar_Keyword_Search(i)
                createtagcloud(i)
            #execfile("C:\myprojee\searchprojee\indexbookcreator.py")
                length_index=len(i)
                for key in  ranks:
                    rank+=key+ "        "+str(ranks[key])
                return render(request, 'bootstrap.html',{'value': i,'rank': rank ,'time': crawl_time, 'rank_time':ranking_time,'sql_time':sqlite_insert_time,'neo4j_time':neo4j_insert_time,'len_index':length_index,'lk_res':lookup_res})

            elif request.POST.get('Radio1')=='ps':
                noofpros= str(request.POST['processor'])
                lookup_res=""
                console_index=""
                li=['python','C:\\myprojee\\searchprojee\\parallelcode.py',"-n",noofpros,"-m",str(request.POST['pages']),"-d",str(request.POST['depth']),"-s",str(request.POST['seed'])]
                p1 = subprocess.Popen(li, shell=False, stdout=subprocess.PIPE)
                
                output = p1.communicate()
                f=open("C:\\myprojee\\searchprojee\\consoli_index.txt","r").read()
                #print rank_read
                index=eval(f)
                if request.POST.get('database1')=="sql":
                    sqlite_insert_time=sqlite_insert(index)
                if request.POST.get('lookup_keyword'):
                    lookup_res=str(index_tbl.objects.filter(key__startswith=str(request.POST['lookup_keyword'])).distinct())
                if len(lookup_res)==0:
                    lookup_res+=str(Look_up(index,str(request.POST['lookup_keyword'])))
                indexbook(index)
                if request.POST.get('database2')=="neo":
                    neo4j_insert_time=Similar_Keyword_Search(index)
                createtagcloud(index)
                #print console_index
                print output
                rank=open("C:\\myprojee\\searchprojee\\consoli_rank.txt","r").read()
                
                return render(request, 'bootstrap.html',{'rank':rank,'value':index,'parallel_time': output,'lk_res':lookup_res,'sql_time':sqlite_insert_time,'neo4j_time':neo4j_insert_time})
            elif request.POST.get('Radio1')=='hs':
                hadoop_index=open("C:\\Users\\$ivaram\\Dropbox\\myprojee\\Hadoop_Remya\\index.txt","r").read()
                index=eval(hadoop_index)
                sqlite_insert_time=sqlite_insert(index)
                neo4j_insert_time=Similar_Keyword_Search(index)
                
                rank=open("C:\\Users\\$ivaram\\Dropbox\\myprojee\\Hadoop_Remya\\ranks.txt","r").read()
                return render(request, 'bootstrap.html',{'value':index,'rank':rank,'sql_time':sqlite_insert_time,'neo4j_time':neo4j_insert_time})
            
          except Exception, err: 
            return HttpResponse(str(err))
    return render(request, 'bootstrap.html',
        {'errors': errors})




