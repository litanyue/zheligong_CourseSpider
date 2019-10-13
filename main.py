import requests
import re
import os
import os.path
from lxml import etree
#start函数是第一个爬虫版本，非常复杂繁琐，严格按照浏览次序抓取，效率低下，数据缺失
#主函数是在发现路径上的规律后直接爬课程信息的方法，简单粗暴，数据不可能缺失，缺点爬的时间很长
#所有的xxxxx建议先登录学校处取出

#某确定课程信息页面
headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "xxxxxxxxxxxx",
    "Host": "course.zstu.edu.cn",
    "Referer": "xxxxxxxxxxxxxxx",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}


url2 = "http://course.zstu.edu.cn/(mvy0wk55fnv23zuzn4m1i1ba)/xsxk.aspx?xh=xxxxxxx&xm=xxxxxxx&gnmkdm=N121101"
headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "xxxxxxxxxxxx",
    "Host": "xuanke.zstu.edu.cn",
    "Pragma": "no-cache",
    "Referer": "http://xuanke.zstu.edu.cn/(mvy0wk55fnv23zuzn4m1i1ba)/xsxk.aspx?xh=xxxxxxxxx&xm=xxxxxxxxx&gnmkdm=N121101",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}
data2 = {
    "__EVENTTARGET": "zymc",
    # kcmcgrid:_ctl14:_ctl1
    "__EVENTARGUMENT": "",
    "__VIEWSTATE": "dDw5OTg5NjUzMjk7dDxwPGw8enk7bmo7eG47eHE7enlkbTs+O2w85L+h5oGv55S15a2Q5a6e6aqM54+tOzIwMTc7MjAxOS0yMDIwOzE7Mzk2MDs+PjtsPGk8MT47PjtsPHQ8O2w8aTwwPjtpPDE+O2k8Mz47aTw0PjtpPDU+O2k8Nz47aTw4PjtpPDk+O2k8MTA+O2k8MTE+Oz47bDx0PHA8cDxsPFRleHQ7PjtsPOWtpuWPtzoyMDE3MzM5OTYwMDQxJm5ic3BcOyZuYnNwXDvlp5PlkI065p2O5bKx5bKpJm5ic3BcOyZuYnNwXDvlrabpmaI65ZCv5paw5a2m6ZmiJm5ic3BcOyZuYnNwXDvooYzmlL/nj60655S15L+h5a6e6aqM54+tMTcoMSk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPFw8Ylw+MjAxOS0yMDIwXDwvYlw+IOWtpuW5tOesrCBcPGJcPjFcPC9iXD47Pj47Pjs7Pjt0PHQ8cDxwPGw8RGF0YVRleHRGaWVsZDtEYXRhVmFsdWVGaWVsZDtFbmFibGVkOz47bDxuajtuajtvPGY+Oz4+Oz47dDxpPDIxPjtAPDE5OTk7MjAwMDsyMDAxOzIwMDI7MjAwMzsyMDA0OzIwMDU7MjAwNjsyMDA3OzIwMDg7MjAwOTsyMDEwOzIwMTE7MjAxMjsyMDEzOzIwMTQ7MjAxNTsyMDE2OzIwMTc7MjAxODsyMDE5Oz47QDwxOTk5OzIwMDA7MjAwMTsyMDAyOzIwMDM7MjAwNDsyMDA1OzIwMDY7MjAwNzsyMDA4OzIwMDk7MjAxMDsyMDExOzIwMTI7MjAxMzsyMDE0OzIwMTU7MjAxNjsyMDE3OzIwMTg7MjAxOTs+PjtsPGk8MTg+Oz4+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85LiT5Lia5ZCN56ew77yaOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcZTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8MjAxNzMzOTk2MDA0MTs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8MDExMTExMDE7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOWFsTfmnaHorrDlvZXvvIE7Pj47Pjs7Pjt0PEAwPHA8cDxsPEN1cnJlbnRQYWdlSW5kZXg7UGFnZUNvdW50O18hSXRlbUNvdW50O18hRGF0YVNvdXJjZUl0ZW1Db3VudDtEYXRhS2V5czs+O2w8aTwwPjtpPDE+O2k8Nz47aTw3PjtsPD47Pj47PjtAMDw7Ozs7Ozs7Ozs7QDA8cDxsPFZpc2libGU7PjtsPG88Zj47Pj47Ozs7PjtAMDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+Pjs7Ozs+OztAMDxwPGw8VmlzaWJsZTs+O2w8bzxmPjs+Pjs7Ozs+O0AwPHA8bDxWaXNpYmxlOz47bDxvPGY+Oz4+Ozs7Oz47Pjs7Ozs7Ozs7Oz47bDxpPDA+Oz47bDx0PDtsPGk8Mj47aTwzPjtpPDQ+O2k8NT47aTw2PjtpPDc+O2k8OD47PjtsPHQ8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+O2k8NT47aTw2PjtpPDc+O2k8OD47aTw5PjtpPDExPjtpPDEyPjtpPDEzPjtpPDE0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS0wNDUwMzIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPjA0NTAzXDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS0wNDUwMzIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPuiBjOS4muWPkeWxleS4juWwseS4muaMh+WvvFw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85b+F5L+u6K++Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwyLjA7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDIuMC0wLjA7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPFw8YSBocmVmPSdodG1sL2tjeHgvMDQ1MDMuaHRtbCcgIHRhcmdldD0nX2JsYW5rJ1w+5p+l55yL6K++56iL5LuL57uNXDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzmnKrpgIk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEoMjAxOS0yMDIwLTEpLTA0NTAzMjAxNzM5NjA7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzpgIDpgIk7bzxmPjs+Pjs+Ozs+Oz4+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+Oz4+O3Q8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+O2k8NT47aTw2PjtpPDc+O2k8OD47aTw5PjtpPDExPjtpPDEyPjtpPDEzPjtpPDE0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS02MjUwMzIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPjYyNTAzXDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS02MjUwMzIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPuaTjeS9nOezu+e7n0Eo5Y+M6K+tKVw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85b+F5L+u6K++Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwzLjA7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDMuMC0wLjE7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDIwMjDlubQx5pyIMuaXpSgxNDowMC0xNjowMCk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPFw8YSBocmVmPSdodG1sL2tjeHgvNjI1MDMuaHRtbCcgIHRhcmdldD0nX2JsYW5rJ1w+5p+l55yL6K++56iL5LuL57uNXDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzmnKrpgIk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEoMjAxOS0yMDIwLTEpLTYyNTAzMjAxNzM5NjA7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzpgIDpgIk7bzxmPjs+Pjs+Ozs+Oz4+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+Oz4+O3Q8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+O2k8NT47aTw2PjtpPDc+O2k8OD47aTw5PjtpPDExPjtpPDEyPjtpPDEzPjtpPDE0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS02MjUyOTIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPjYyNTI5XDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS02MjUyOTIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPui9r+S7tuW3peeoi0FcPC9hXD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOW/heS/ruivvjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8My4wOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwzLjAtMC4xOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwyMDE55bm0MTLmnIgzMeaXpSgxNDowMC0xNjowMCk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPFw8YSBocmVmPSdodG1sL2tjeHgvNjI1MjkuaHRtbCcgIHRhcmdldD0nX2JsYW5rJ1w+5p+l55yL6K++56iL5LuL57uNXDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzmnKrpgIk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEoMjAxOS0yMDIwLTEpLTYyNTI5MjAxNzM5NjA7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzpgIDpgIk7bzxmPjs+Pjs+Ozs+Oz4+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+Oz4+O3Q8O2w8aTwwPjtpPDE+O2k8Mj47aTwzPjtpPDQ+O2k8NT47aTw2PjtpPDc+O2k8OD47aTw5PjtpPDExPjtpPDEyPjtpPDEzPjtpPDE0Pjs+O2w8dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS02MjYwNzIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPjYyNjA3XDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0nIycgb25jbGljaz0id2luZG93Lm9wZW4oJ3hzeGpzLmFzcHg/eGtraD0xKDIwMTktMjAyMC0xKS02MjYwNzIwMTczOTYwMjAxNzMzOTk2MDA0MSZ4aD0yMDE3MzM5OTYwMDQxJywneHN4anMnLCd0b29sYmFyPTAsbG9jYXRpb249MCxkaXJlY3Rvcmllcz0wLHN0YXR1cz0wLG1lbnViYXI9MCxzY3JvbGxiYXJzPTEscmVzaXphYmxlPTEnKSJcPuaTjeS9nOezu+e7n+ivvueoi+iuvuiuoVw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85a6e6Le15b+F5L+uOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxLjA7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCsxOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0naHRtbC9rY3h4LzYyNjA3Lmh0bWwnICB0YXJnZXQ9J19ibGFuaydcPuafpeeci+ivvueoi+S7i+e7jVw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85pyq6YCJOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxKDIwMTktMjAyMC0xKS02MjYwNzIwMTczOTYwOz4+Oz47Oz47dDw7bDxpPDE+Oz47bDx0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w86YCA6YCJO288Zj47Pj47Pjs7Pjs+Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjs+Pjt0PDtsPGk8MD47aTwxPjtpPDI+O2k8Mz47aTw0PjtpPDU+O2k8Nj47aTw3PjtpPDg+O2k8OT47aTwxMT47aTwxMj47aTwxMz47aTwxND47PjtsPHQ8cDxwPGw8VGV4dDs+O2w8XDxhIGhyZWY9JyMnIG9uY2xpY2s9IndpbmRvdy5vcGVuKCd4c3hqcy5hc3B4P3hra2g9MSgyMDE5LTIwMjAtMSktNjI2MTMyMDE3Mzk2MDIwMTczMzk5NjAwNDEmeGg9MjAxNzMzOTk2MDA0MScsJ3hzeGpzJywndG9vbGJhcj0wLGxvY2F0aW9uPTAsZGlyZWN0b3JpZXM9MCxzdGF0dXM9MCxtZW51YmFyPTAsc2Nyb2xsYmFycz0xLHJlc2l6YWJsZT0xJykiXD42MjYxM1w8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8XDxhIGhyZWY9JyMnIG9uY2xpY2s9IndpbmRvdy5vcGVuKCd4c3hqcy5hc3B4P3hra2g9MSgyMDE5LTIwMjAtMSktNjI2MTMyMDE3Mzk2MDIwMTczMzk5NjAwNDEmeGg9MjAxNzMzOTk2MDA0MScsJ3hzeGpzJywndG9vbGJhcj0wLGxvY2F0aW9uPTAsZGlyZWN0b3JpZXM9MCxzdGF0dXM9MCxtZW51YmFyPTAsc2Nyb2xsYmFycz0xLHJlc2l6YWJsZT0xJykiXD7mlbDmja7lupPns7vnu5/kuI7lupTnlKjorr7orqFcPC9hXD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOW/heS/ruivvjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8My4wOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwzLjAtMC4xOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0naHRtbC9rY3h4LzYyNjEzLmh0bWwnICB0YXJnZXQ9J19ibGFuaydcPuafpeeci+ivvueoi+S7i+e7jVw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85pyq6YCJOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxKDIwMTktMjAyMC0xKS02MjYxMzIwMTczOTYwOz4+Oz47Oz47dDw7bDxpPDE+Oz47bDx0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w86YCA6YCJO288Zj47Pj47Pjs7Pjs+Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjs+Pjt0PDtsPGk8MD47aTwxPjtpPDI+O2k8Mz47aTw0PjtpPDU+O2k8Nj47aTw3PjtpPDg+O2k8OT47aTwxMT47aTwxMj47aTwxMz47aTwxND47PjtsPHQ8cDxwPGw8VGV4dDs+O2w8XDxhIGhyZWY9JyMnIG9uY2xpY2s9IndpbmRvdy5vcGVuKCd4c3hqcy5hc3B4P3hra2g9MSgyMDE5LTIwMjAtMSktNjI2MTgyMDE3Mzk2MDIwMTczMzk5NjAwNDEmeGg9MjAxNzMzOTk2MDA0MScsJ3hzeGpzJywndG9vbGJhcj0wLGxvY2F0aW9uPTAsZGlyZWN0b3JpZXM9MCxzdGF0dXM9MCxtZW51YmFyPTAsc2Nyb2xsYmFycz0xLHJlc2l6YWJsZT0xJykiXD42MjYxOFw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8XDxhIGhyZWY9JyMnIG9uY2xpY2s9IndpbmRvdy5vcGVuKCd4c3hqcy5hc3B4P3hra2g9MSgyMDE5LTIwMjAtMSktNjI2MTgyMDE3Mzk2MDIwMTczMzk5NjAwNDEmeGg9MjAxNzMzOTk2MDA0MScsJ3hzeGpzJywndG9vbGJhcj0wLGxvY2F0aW9uPTAsZGlyZWN0b3JpZXM9MCxzdGF0dXM9MCxtZW51YmFyPTAsc2Nyb2xsYmFycz0xLHJlc2l6YWJsZT0xJykiXD7nvZHnu5zns7vnu5/orr7orqHkuI7lt6XnqItcPC9hXD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOW/heS/ruivvjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8My4wOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwzLjAtMC4xOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwmbmJzcFw7Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDxcPGEgaHJlZj0naHRtbC9rY3h4LzYyNjE4Lmh0bWwnICB0YXJnZXQ9J19ibGFuaydcPuafpeeci+ivvueoi+S7i+e7jVw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w85pyq6YCJOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwxKDIwMTktMjAyMC0xKS02MjYxODIwMTczOTYwOz4+Oz47Oz47dDw7bDxpPDE+Oz47bDx0PHA8cDxsPFRleHQ7VmlzaWJsZTs+O2w86YCA6YCJO288Zj47Pj47Pjs7Pjs+Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPCZuYnNwXDs7Pj47Pjs7Pjs+Pjt0PDtsPGk8MD47aTwxPjtpPDI+O2k8Mz47aTw0PjtpPDU+O2k8Nj47aTw3PjtpPDg+O2k8OT47aTwxMT47aTwxMj47aTwxMz47aTwxND47PjtsPHQ8cDxwPGw8VGV4dDs+O2w8XDxhIGhyZWY9JyMnIG9uY2xpY2s9IndpbmRvdy5vcGVuKCd4c3hqcy5hc3B4P3hra2g9MSgyMDE5LTIwMjAtMSktNjI2NTIyMDE3Mzk2MDIwMTczMzk5NjAwNDEmeGg9MjAxNzMzOTk2MDA0MScsJ3hzeGpzJywndG9vbGJhcj0wLGxvY2F0aW9uPTAsZGlyZWN0b3JpZXM9MCxzdGF0dXM9MCxtZW51YmFyPTAsc2Nyb2xsYmFycz0xLHJlc2l6YWJsZT0xJykiXD42MjY1Mlw8L2FcPjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8XDxhIGhyZWY9JyMnIG9uY2xpY2s9IndpbmRvdy5vcGVuKCd4c3hqcy5hc3B4P3hra2g9MSgyMDE5LTIwMjAtMSktNjI2NTIyMDE3Mzk2MDIwMTczMzk5NjAwNDEmeGg9MjAxNzMzOTk2MDA0MScsJ3hzeGpzJywndG9vbGJhcj0wLGxvY2F0aW9uPTAsZGlyZWN0b3JpZXM9MCxzdGF0dXM9MCxtZW51YmFyPTAsc2Nyb2xsYmFycz0xLHJlc2l6YWJsZT0xJykiXD7mnI3liqHlpJbljIXmpoLorrpcPC9hXD47Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPOW/heS/ruivvjs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8My4wOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwzLjAtMC4xOz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDwyMDE55bm0MTLmnIgzMOaXpSgxNDowMC0xNjowMCk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPFw8YSBocmVmPSdodG1sL2tjeHgvNjI2NTIuaHRtbCcgIHRhcmdldD0nX2JsYW5rJ1w+5p+l55yL6K++56iL5LuL57uNXDwvYVw+Oz4+Oz47Oz47dDxwPHA8bDxUZXh0Oz47bDzmnKrpgIk7Pj47Pjs7Pjt0PHA8cDxsPFRleHQ7PjtsPDEoMjAxOS0yMDIwLTEpLTYyNjUyMjAxNzM5NjA7Pj47Pjs7Pjt0PDtsPGk8MT47PjtsPHQ8cDxwPGw8VGV4dDtWaXNpYmxlOz47bDzpgIDpgIk7bzxmPjs+Pjs+Ozs+Oz4+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+O3Q8cDxwPGw8VGV4dDs+O2w8Jm5ic3BcOzs+Pjs+Ozs+Oz4+Oz4+Oz4+O3Q8QDA8Ozs7Ozs7Ozs7Oz47Oz47Pj47Pj47Pp8mrIdXfV8gnprhLlwHNFRqQN/q",
    "__VIEWSTATEGENERATOR": "7AEF2E62",
    "zymc": "3620计算机科学与技术主修专业||2017",#测试数据
    "xx": ""
}


def start():
    # 这里是在跨专业选课小窗口保存下来的文件和文件夹，目的是获取每个学院特殊的信息
    list = os.listdir(r'D:/python_workspace/schedule/resources/')
    code = []
    for str in list:
        #过滤文件夹只保留文件
        if (str.find("files") == -1):
            str = 'resources//' + str
            html = etree.parse(str, etree.HTMLParser())
            list1 = html.xpath('//td/select[@name="ListBox1"]/option/text()')  # 得到专业
            list2 = html.xpath('//td/select[@name="ListBox1"]/option/@value')  # 得到专业标号
            # 制作data发送请求
            for i in range(0, len(list1)):
                for j in range(1999, 2019):
                    #在data信息里添加专业与年级信息
                    data2["zymc"] = list2[i] + list1[i] + '主修专业||' + '%d' % j
                    #此处得到的resp页面包含了该专业该年级可选的课程
                    resp = requests.post(url=url2, headers=headers2, data=data2)
                    #从这个页面中取出课程代码并放在code[]里
                    code += re.findall('(?<=>)\d\d\d\d\d(?=<)', resp.text)
                    # 查看有没有第二页的情况，如果有再请求第二次，一般没有第三页的吧
                    if (resp.text.find("doPostBack") != -1):
                        data2["__EVENTTARGET"] = "kcmcgrid:_ctl14:_ctl1"
                        resp = requests.post(url=url2, headers=headers2, data=data2)
                        code += re.findall('(?<=>)\d\d\d\d\d(?=<)', resp.text)
                    print(list2[i] + list1[i] + '主修专业||' + '%d' % j + 'ok')
                print('第%d次遍历完成' % i)
                print('列表长度为' + '%d' % len(code))
    print("列表已做好")
    for number in code:
        url1 = "http://course.zstu.edu.cn/(mvy0wk55fnv23zuzn4m1i1ba)/xsxjs.aspx?xkkh=1(2019-2020-1)-" + number + "xxxxxxxxx&xh=xxxxxxx"
        resp = requests.get(url=url1, headers=headers1)
        with open('src\\' + number + ".html", 'w') as f:
            f.write(resp.text)


if __name__ == '__main__':
    count = 0
    str = ""
    for i in range(88193, 100000):
        if (i > 999 and i < 10000):
            str = "0" + "%d" % i
        if (i > 9999 and i < 100000):
            str = "%d" % i

        url2 = "http://xuanke.zstu.edu.cn/(mvy0wk55fnv23zuzn4m1i1ba)/xsxjs.aspx?xkkh=1(2019-2020-1)-" + str + "xxxxxxxxx&xh=xxxxxxx"
        resp = requests.get(url=url2, headers=headers2)

        if (resp.text.find("该课程没有") == -1):
            with open('src1/' + str + ".html", 'w') as f:
                f.write(resp.text)
            count = count + 1
        print("code:" + str)
        print("the count is %d" % count)
