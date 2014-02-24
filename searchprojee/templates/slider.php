<html>
<head>
    <title>Nivo jQuery Slider Demo</title>
    
    <!--  Load the stylesheets  -->
    <link rel="stylesheet" href="themes/default/default.css" type="text/css" media="screen" />
    <link rel="stylesheet" href="nivo-slider.css" type="text/css" media="screen" />
    <link rel="stylesheet" href="style.css" type="text/css" media="screen" />
</head>
<body>
    <div id="wrapper">
    
        <!-- The slider wrapper div  -->
        <div class="slider-wrapper theme-default">
            <div id="slider" class="nivoSlider">
            
                <!--  Images to slide through.  -->
                <img src="images/toystory.jpg" data-thumb="images/toystory.jpg" alt="" />
                <a href="http://dev7studios.com"><img src="images/up.jpg" data-thumb="images/up.jpg" alt="" title="This is an example of a caption" /></a>
                <img src="images/walle.jpg" data-thumb="images/walle.jpg" alt="" data-transition="slideInLeft" />
                <img src="images/nemo.jpg" data-thumb="images/nemo.jpg" alt="" title="#htmlcaption" />
            </div>
            
            <!--  Captions to show for images  -->
            <div id="htmlcaption" class="nivo-html-caption">
                <strong>This</strong> is an example of a <em>HTML</em> caption with <a href="#">a link</a>. 
            </div>
        </div>

    </div>
    
    <!--  Load the javascript files  -->
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
    <script type="text/javascript" src="jquery.nivo.slider.js"></script>
    <script type="text/javascript">
    
    //<!--  Load the slider  --> 
    $(window).load(function() {
        $('#slider').nivoSlider();
    });
    
    </script>
</body>
</html>