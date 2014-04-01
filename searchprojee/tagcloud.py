from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
text=""
f=open('C:\myprojee\searchprojee\keywords','r')
for line in f:
    text+=line
    print line
f.close()
tags = make_tags(get_tag_counts(text), maxsize=30)

create_tag_image(tags, 'cloud_large.png', size=(1024,768), fontname='Lobster')
