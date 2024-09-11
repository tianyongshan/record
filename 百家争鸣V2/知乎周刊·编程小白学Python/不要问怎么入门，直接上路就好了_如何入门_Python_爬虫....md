# 不要问怎么入门，直接上路就好了_如何入门_Python_爬虫...

知乎周刊 103

不要问怎么入门，直接上路就好了

如何入门 Python 爬虫？

谢科

「入门」是良好的动机，但是可能作用缓慢。如果你手里或者脑子里有一个项目，那么实践起来你会被目标驱动，而不会像学习模块一样慢慢学习。

另外如果说知识体系里的每一个知识点是图里的点，依赖关系是边的话，那么这个图一定不是一个有向无环图。因为学习 A 的经验可以帮助你学习 B。因此，你不需要学习怎么样「入门」，因为这样的「入门」点根本不存在！你需要学习的是怎么样做一个比较大的东西，在这个过程中，你会很快地学会需要学会的东西的。当然，你可以争论说需要先懂 Python，不然怎么学会 Python 做爬虫呢？但是事实上，你完全可以在做这个爬虫的过程中学习 Python :D

看到前面很多答案都讲的「术」——用什么软件怎么爬，那我就讲讲「道」和「术」吧——爬虫怎么工作以及怎么在 Python 实现。

先长话短说 summarize 一下：

你需要学习：

1. 基本的爬虫工作原理

2. 基本的 http 抓取工具，Scrapy

3. Bloom Filter:

http://billmill.org/bloomfilter-tutorial/

4. 如果需要大规模网页抓取，你需要学习分布式爬虫的概念。其实没那么玄乎，你只要学会怎样维护一个所有集群机器能够有效分享的分布式队列就好。最简单的实现是 python-rq:

https://github.com/nvie/rq

5. rq 和 Scrapy 的结合：

https://github.com/darkrho/scrapy-redis

6. 后续处理，网页析取(

https://github.com/grangier/python-goose

)，存储(Mongodb)

以下是短话长说：

说说当初写的一个集群爬下整个豆瓣的经验吧。

1）首先你要明白爬虫怎样工作。

想象你是一只蜘蛛，现在你被放到了互联「网」上。那么，你需要把所有的网页都看一遍。怎么办呢？没问题呀，你就随便从某个地方开始，比如说人民日报的首页，这个叫 initial pages，用$表示吧。

在人民日报的首页，你看到那个页面引向的各种链接。于是你很开心地爬到了「国内新闻」那个页面。太好了，这样你就已经爬完了两个页面（首页和国内新闻）！暂且不用管爬下来的页面怎么处理的，你就想象你把这个页面完完整整抄成了个 html 放到了你身上。

突然你发现，在国内新闻这个页面上，有一个链接链回「首页」。作为一只聪明的蜘蛛，你肯定知道你不用爬回去的吧，因为你已经看过了啊。所以，你需要用你的脑子，存下你已经看过的页面地址。这样，每次看到一个可能需要爬的新链接，你就先查查你脑子里是不是已经去过这个页面地址。如果去过，那就别去了。

好的，理论上如果所有的页面可以从 initial page 达到的话，那么可以证明你一定可以爬完所有的网页。

那么在 Python 里怎么实现呢？

很简单

import

Queue

initial_page = "http://www.renminribao.com"

url_queue = Queue.Queue()

seen = set()

seen.insert(initial_page)

url_queue.put(initial_page)

while

(True): #一直进行直到海枯石烂

if

url_queue.size()>0:

current_url = url_queue.get()

#拿出队列中第一个的 url

store(current_url)

#把这个 url 代表的网页存储好

for

next_url

in

extract_urls(current_url): #提取把这个 url 里链向的 url

if

next_url

not in

seen:

seen.put(next_url)

url_queue.put(next_url)

else:

break

写得已经很伪代码了。

所有的爬虫的 backbone 都在这里，下面分析一下为什么爬虫事实上是个非常复杂的东西——搜索引擎公司通常有一整个团队来维护和开发。

2）效率

如果你加工一下上面的代码直接运行的话，你需要一整年才能爬下整个豆瓣的内容。更别说 Google 这样的搜索引擎需要爬下全网的内容了。

问题出在哪呢？需要爬的网页实在太多太多了，而上面的代码太慢太慢了。设想全网有 N 个网站，那么分析一下判重的复杂度就是 N*log(N)，因为所有网页要遍历一次，而每次判重用 set 的话需要 log(N)的复杂度。OK，OK，我知道 Python 的 set 实现是 hash——不过这样还是太慢了，至少内存使用效率不高。

通常的判重做法是怎样呢？

Bloom Filter.

简单讲它仍然是一种 hash 的方法，但是它的特点是，它可以使用固定的内存（不随 url 的数量而增长）以 O(1)的效率判定 url 是否已经在 set 中。可惜天下没有白吃的午餐，它的唯一问题在于，如果这个 url 不在 set 中，BF 可以 100%确定这个 url 没有看过。但是如果这个 url 在 set 中，它会告诉你：这个 url 应该已经出现过，不过我有 2%的不确定性。注意这里的不确定性在你分配的内存足够大的时候，可以变得很小很少。一个简单的教程:Bloom Filters｜

http://billmill.org/bloomfilter-tutorial/

注意到这个特点，url 如果被看过，那么可能以小概率重复看一看（没关系，多看看不会累死）。但是如果没被看过，一定会被看一下（这个很重要，不然我们就要漏掉一些网页了！）。 [IMPORTANT: 此段有问题，请暂时略过]

好，现在已经接近处理判重最快的方法了。另外一个瓶颈——你只有一台机器。不管你的带宽有多大，只要你的机器下载网页的速度是瓶颈的话，那么你只有加快这个速度。用一台机子不够的话——用很多台吧！当然，我们假设每台机子都已经进了最大的效率——使用多线程（python 的话，多进程吧）。

3）集群化抓取

爬取豆瓣的时候，我总共用了 100 多台机器昼夜不停地运行了一个月。想象如果只用一台机子你就得运行 100 个月了……

那么，假设你现在有 100 台机器可以用，怎么用 Python 实现一个分布式的爬取算法呢？

我们把这 100 台中的 99 台运算能力较小的机器叫作 slave，另外一台较大的机器叫作 master，那么回顾上面代码中的 url_queue，如果我们能把这个 queue 放到这台 master 机器上，所有的 slave 都可以通过网络跟 master 联通，每当一个 slave 完成下载一个网页，就向 master 请求一个新的网页来抓取。而每次 slave 新抓到一个网页，就把这个网页上所有的链接送到 master 的 queue 里去。同样，bloom filter 也放到 master 上，但是现在 master 只发送确定没有被访问过的 url 给 slave。Bloom Filter 放到 master 的内存里，而被访问过的 url 放到运行在 master 上的 Redis 里，这样保证所有操作都是 O(1)。（至少平摊是 O(1)，Redis 的访问效率见：

http://redis.io/commands/linsert

)

考虑如何用 Python 实现：

在各台 slave 上装好 Scrapy，那么各台机子就变成了一台有抓取能力的 slave，在 master 上装好 Redis 和 rq 用作分布式队列。

代码于是写成

#slave.py

current_url = request_from_master()

to_send = []

for next_url in extract_urls(current_url):

to_send.append(next_url)

store(current_url).

send_to_master(to_send)

#master.py

distributed_queue = DistributedQueue()

bf = BloomFilter()

initial_pages = "www.renmingribao.com"

while(True):

if request == 'GET':

if distributed_queue.size()>0:

send(distributed_queue.get())

else:

break

elif request == 'POST':

bf.put(request.url)

好的，其实你能想到，有人已经给你写好了你需要的：

https://github.com/darkrho/scrapy-redis

4）展望及后处理

虽然上面用很多「简单」，但是真正要实现一个商业规模可用的爬虫并不是一件容易的事。上面的代码用来爬一个整体的网站几乎没有太大的问题。

但是如果附加上你需要这些后续处理，比如：

1. 有效地存储（数据库应该怎样安排）

2. 有效地判重（这里指网页判重，咱可不想把人民日报和抄袭它的大民日报都爬一遍）

3. 有效地信息抽取（比如怎么样抽取出网页上所有的地址，「朝阳区奋进路中华道」），搜索引擎通常不需要存储所有的信息，比如图片我存来干吗……

4. 及时更新（预测这个网页多久会更新一次）

如你所想，这里每一个点都可以供很多研究者十数年的研究。虽然如此，

「路漫漫其修远兮，吾将上下而求索。」

所以，不要问怎么入门，直接上路就好了：）

2014-05-19

学 Python 发现学一门编程语言很难，有哪些学好编程的方法或技巧？

王月

最难的编程语言是哪门？

不是 C++，不是 Lisp，而是

你的第一门语言。

这门语言哪里最难？

入门最难。

比如下述代码：

print

"hello world!"

新手可能的反应：

print 是什么？我的电脑没连打印机，能用吗？

hello world 是什么？这个 expression 很奇怪。很少见人这么用，究竟什么意思？

为什么 print 没有双引号？为什么 hello word 要用双引号？

etc.

作为新手应把这些疑问贴出来，或者问问周围的人。他们会针对性地给出几种回答：

这个先不用管，记住就好了。

比如 print 就不是入门阶段的重点。

能把 print 透彻解释清楚的程序员，不会超过 10%。

这个语法规则是 balabala

比如这里的字符串"hello world"。

这个是编程文化，约定俗成。有兴趣的话就去 Google 一下。

比如这里的 hello world。

所谓

入门

，就是遇到新疑问时你可以

通过阅读和实验

自己搞定。（or 搞定大部分）

加油！

2014-11-04

如何系统地自学 Python？

代霸天

从 Machine Learning 或者 Web 或者爬虫入手 Python，会比较有成就感，不枯燥。

天天 print，初学者学个几天就没动力了。

我推荐，Machine Learning in Action，一点点线性代数基础即可阅读此书。

Web 学习 flask，遇到不懂的语法查文档。

爬虫学习 Scrapy，同上，遇到不懂的语法查文档。

真的，用 Python 写个预测足球比赛结果的小程序或个人博客或抓取微博数据，比天天对着书上无聊的 print 好多了。

2015-03-31