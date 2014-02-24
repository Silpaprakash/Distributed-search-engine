ins=open("myfile","r")
for line in ins:
        p.write("""<div class="bb-item">

							<a href=\"""")
        word=line.split()        
        p.write(word[1])
        p.write(""""><h1>""")
        
        p.write(word[0])
        p.write("""</h1></a>""")
