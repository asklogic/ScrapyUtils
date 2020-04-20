import sys
from base.command import cli

if __name__ == '__main__':
    cli()

from base.libs import FireFoxScraper
from wordcloud import WordCloud
import jieba

fox = FireFoxScraper()

content = fox.get('https://www.zhihu.com/question/29372574')
words = jieba.lcut(content)

wc = WordCloud().generate(content)
wc.to_file('词云图.png')