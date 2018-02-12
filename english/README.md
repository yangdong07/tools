
## for english study

最初想法是为了将pdf的所有单词，抽取出来，集中学习一下不认识的单词，然后再读pdf。

1. 将pdf所有单词提取出来，并统计频次： bag of words
2. ~~去掉一些 stop word~~
3. 按使用频次排序。设置频次阈值：去掉常用词，学习不认识的单词。

记住目的：
1. 读pdf前，先熟悉不认识的单词
2. 了解单词的频次分布。设置学习频次阈值： 频次大于这个阈值的，认为是常用词，可以砍掉。 按频次从高到低学习不认识的单词。

这些单词可以存到数据库中。


使用库：
 
- [textract](http://textract.readthedocs.io/en/latest/installation.html)，抽取text的库
- [pyenchant](http://pythonhosted.org/pyenchant/)，识别是否英语单词的库

### 安装 textract

参考：http://textract.readthedocs.io/en/latest/installation.html

- brew cask install xquartz
- brew install poppler antiword unrtf tesseract swig
- pip install textract

遇到的错误：

https://github.com/bambocher/pocketsphinx-python/issues/28

1. git clone --recursive https://github.com/bambocher/pocketsphinx-python
2. cd pocketsphinx-python
3. Edit file pocketsphinx-python/deps/sphinxbase/src/libsphinxad/ad_openal.c
4. Change
