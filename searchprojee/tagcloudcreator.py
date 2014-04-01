def createtagcloud(index):
    #f=open("myfile.txt","r")
    p=open("C:\\myprojee\\searchprojee\\templates\\tagcloud.html","w")
    p.write("""<!DOCTYPE HTML>
<html>
<head>
{% load staticfiles %}
<script src="{% static "searchprojee/tagcanvas.js" %}" type="text/javascript"></script>
</head>
<body>
<div id="myCanvasContainer">
 <canvas width="800" height="600" id="myCanvas">
  <p>Anything in here will be replaced on browsers that support the canvas element</p>
  <ul>
   """)
    for key in index:
        p.write("""<li><a href=""")
        #words=key.split()
        p.write('"')
        p.write(str(index[key]))
        p.write('"')
        p.write("""target="_blank">""")
        p.write(str(key))
        p.write("""</a></li>""")
    print("keywords inserted")
    p.write("""</ul>
 </canvas>
</div>
<script type="text/javascript">
  window.onload = function() {
    try {
      TagCanvas.Start('myCanvas');
    } catch(e) {
      // something went wrong, hide the canvas container
      document.getElementById('myCanvasContainer').style.display = 'none';
    }
  };
 </script>
</body>
</html>""")
    print("file wrote")
    p.close()
    #f.close()


