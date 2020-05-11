# -*- coding: utf-8 -*-
head='''
<!DOCTYPE html>
<html>
<head>
    <title>Weekly Report</title>
    <meta charset="utf-8">
    <style type="text/css">
        body {
            font-family: Helvetica,arial,freesans,clean,sans-serif;
        }
        ul {
            list-style-type: decimal;
        }
        #wrapper {
            width : 780px;
            margin : 0 auto;
        }
        .title {
            font-size: 180%;
            line-height: 20px;
            font-weight: bold;
            padding: 20px 20px;
            color: #4183C4;
            text-shadow: 0 1px 0 white;
            text-align: center;
            display: block;
            border: 1px solid #CACACA;
            border-bottom: 0 none;
            background: #FAFAFA;
            background: -moz-linear-gradient(#FAFAFA,#EAEAEA);
            background: -webkit-linear-gradient(#FAFAFA,#EAEAEA);
        }
        .content {
            text-align : left;
            padding : 3px;
            background : #EEE;
            border-radius:3px;
            margin-bottom: 20px;
        }
        .inner_content {
            background-color: white;
            border: 1px solid #CACACA;
            padding: 20px;
            line-height: 1.4;
            font-size:100%;
            color:#333;
        }
    </style>
</head>'''

td_html='''<body>
<div id="wrapper">
    <div>
          <h2></h2>
          <div class="content">
             <div class="title">每日回顾</div>
             <div class="inner_content">{content_td}</div>
          </div>
    </div>
</div>
</body>
</html>'''

wk_html='''<body>
<div id="wrapper">
    <div>
          <h2></h2>
          <div class="content">
             <div class="title">每周回顾 ({week})</div>
             <div class="inner_content">{content_wk}</div>
          </div>
    </div>
</div>
</body>
</html>'''

