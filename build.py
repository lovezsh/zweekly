import os
import httpx
import re
import urllib.parse
import datetime

def fetch_ci_time(filePath):
    entries = httpx.get("https://api.github.com/repos/lovezsh/zweekly/commits?path=" + filePath + "&page=1&per_page=1")
    ciTime= entries.json()[0]["commit"]["committer"]["date"].split("T")[0]
    return ciTime
    # return datetime.datetime.strptime(ciTime,"%Y-%m-%d")

if __name__ == "__main__":
  readmefile=open('README.md','w')
  readmefile.write("# zweekly\n\n> 记录子舒的周刊，欢迎订阅，也欢迎[推荐](https://github.com/lovezsh/zweekly/issues/)你的好东西。模板来自潮流周刊。\n\n 网站：https://zweekly.vercel.app/ \n\n\n")
  recentfile=open('RECENT.md','w')

  for root, dirs, filenames in os.walk('./src/pages/posts'):
    filenames = sorted(filenames, key=lambda x:float(re.findall("(\d+)",x)[0]), reverse=True)

  for index, name in enumerate(filenames):
      if name.endswith('.md'):
        filepath = urllib.parse.quote(name)
        oldTitle = name.split('.md')[0]
        url   = 'https://zweekly.vercel.app/posts/' + oldTitle
        title = '第 ' + oldTitle.split('-')[0] + ' 期 - ' + oldTitle.split('-')[1]
        readmeMd= '* [{}]({})\n'.format(title, url)
        dateList = ["2022-10-10","2022-09-26","2022-09-12","2022-09-05","2022-08-29"]
        num = int(oldTitle.split('-')[0])
        if index < 5 :
          modified = fetch_ci_time('/src/pages/posts/' + filepath)

          recentMd= '* [{}]({}) - {}\n'.format(title, url, modified)
          recentfile.write(recentMd)
        readmefile.write(readmeMd)

  recentfile.close()
  readmefile.close()
