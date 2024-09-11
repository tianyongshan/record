# Belleve_,

Lisp 解释器？

Belleve

,

炼金术士

来，我现在就教你写一个。基于静态作用域和按值传递，有 lambda、let、letrec、cond 宏，已经比较完整了。另外

@冯东

，用 javascript 可以实现 call/cc，在解释前全文 CPS 就可以了。

var

runtimeScope

=

{}

// 基底作用域，放算符var

globalScope

=

Object.create(runtimeScope)

// 全局作用域，放各种普通函数function

Operator(g){

this.invoke

=

g.}function

interpret(form,

scope){

// 一个非常没技术含量的树解释型解释器

if(typeof

form

===

"string")

// form 是变量

return

scope[form]

// 从当前作用域读变量

else

if(form

instanceof

Array){

// form 是调用

var

fn

=

interpret(form[0],

scope)

// 计算调用表达式第一项

if

(fn

instanceof

Operator)

{

return

fn.invoke(scope,

form.slice(1))

// 算符调用，scope 要传否则没法实现 lambda，各参数不解释直接丢

}

else

{

var

args

=

[]

for(var

j

=

1.

j

<

form.length.

j++)

{

args[j

-

1]

=

interpret(form[j],

scope)// 计算诸参数，按值传递

}

return

fn.apply(null,

args)

}

}

else

{

return

form

}}// 现在我们来定义几个基本算符：lambda，let，letrec 和 cond// quote、quasiquote、unquote、eval 我就不做了runtimeScope.lambda

=

new

Operator(function(scope,

subforms){

// lambda 用来创建函数

// scope 为计算 (lambda ...) 时所在作用域，我们的 lambda 使用静态作用域。

// lambda 每次被调用时会创建子作用域 s，并将其中写入实际参数。

var

parameters

=

subforms[0]

// 形参表

var

body

=

subforms[1]

// 函数体

return

function(){

var

s

=

Object.create(scope)

// 创建衍生作用域放形参

for(var

j

=

0.

j

<

parameters.length.

j++){

s[parameters[j]]

=

arguments[j]

// 写初值

}

return

interpret(body,

s)

// 在衍生作用域中计算 body

}})runtimeScope['let']

=

new

Operator(function(scope,

subforms){

// let 表达式

var

assignments

=

subforms[0]

// let 表达式的诸赋值，['id', value]

var

s

=

Object.create(scope).

// 创建衍生作用域

for(var

j

=

0.

j

<

assignments.length.

j++){

// 在 scope 计算 value，存入 s 作用域内

s[assignments[j][0]]

=

interpret(assignments[j][1],

scope)

}

var

result.

for(var

j

=

1.

j

<

subforms.length.

j++){

result

=

interpret(subforms[j],

s)

// 在 s 内计算体表达式

}

return

result})runtimeScope.letrec

=

new

Operator(function(scope,

subforms){

// 递归 let

var

assignments

=

subforms[0]

// letrec 表达式的诸赋值，['id', value]

var

s

=

Object.create(scope).

// 创建衍生作用域

for(var

j

=

0.

j

<

assignments.length.

j++){

// letrec 中 value 各项的作用域在 s 内计算

s[assignments[j][0]]

=

interpret(assignments[j][1],

s)

}

var

result.

for(var

j

=

1.

j

<

subforms.length.

j++){

result

=

interpret(subforms[j],

s)

// 在 s 内计算体表达式

}

return

result})runtimeScope.cond

=

new

Operator(function(scope,

subforms){

// cond 表达式，多路分支

for(var

j

=

0.

j

<

subforms.length.

j++){

var

cond

=

interpret(subforms[j][0],

scope)// 计算前项

if(cond)

// 如果为真

return

interpret(subforms[j][1],

scope)

// 返回后项

}})runtimeScope['set!']

=

new

Operator(function(scope,

subforms){

// 赋值，我不想做的……

return

scope[subforms[0]]

=

interpret(subforms[1],

scope)})// 普通函数和普通值// 呃可能理论看多了点，没做 car，cdr 和 cons……// 不过这三个你应该写的出来吧globalScope.trace

=

console.log.bind(console).globalScope['true']

=

trueglobalScope['false']

=

falseglobalScope['+']

=

function(x,

y){

return

x

-

0

+

y

}globalScope['-']

=

function(x,

y){

return

x

-

y

}globalScope['*']

=

function(x,

y){

return

x

*

y

}globalScope['>']

=

function(x,

y){

return

x

>

y

}// 试试递归函数吧 :)interpret(['letrec',

[['fact',

['lambda',

['n'],

['cond',

[['>',

'n',

0],

['*',

'n',

['fact',

['-',

'n',

1]]]],

['true',

1]]]]],

['trace',

['fact',

5]]],

globalScope).// Y 组合子interpret(['let',

[['Y',

['lambda',

['f'],

[

['lambda',

['x'],

['f',

['lambda',

['y'],

[['x',

'x'],

'y']]]],

['lambda',

['x'],

['f',

['lambda',

['y'],

[['x',

'x'],

'y']]]]

]]]],

['trace',

[['Y',

['lambda',

['recurse'],

['lambda',

['n'],

['cond',

[['>',

'n',

0],

['*',

'n',

['recurse',

['-',

'n',

1]]]],

['true',

1]

]]]],

5]]],

globalScope)

另外你们这群叫我实现 call/cc 的都是啥心态……明确告诉你，call/cc 在 Lambda 演算中无法作为闭合函数居留。

赞同：26

评论：7

阿里巴巴有什么特别的公司文化？

匿名用户

请参看一实习生的阿里印象（09年的时候），真实性请自行判断：

在阿里实习了两个月了吧，在这期间我学到了很多，也见识了很多下面我来和大家一起分享一下我这两个月在阿里学到的阿里文化吧，希望对大家有帮助！

1、阿里的价值观：

首先我来说下，因为我刚到阿里时阿里就对我们上了阿里的价值观这课，阿里巴巴非常重视价值观，对员工的考核价值观占50%，业绩占50%。每个月阿里都要对每个员工进行一次考核，对我们实习生的考核主要有：1.对action的完成情况（action是每天组长给我们归定下来的任务任务可以是：比如让你每天中午去找人聊天，早上开一次早会，当着众人大声唱一首歌），对action考核很多都是看细节方面，不要忽视每一个细节，哪怕是很小的一个action都要认真的完成！2.平时业务讨论的发言情况（每天团队都会有大大小小的业务讨论，大家为了一个问题的细节讨论的面红耳赤，如果你在会上不发言的话，那么你就惨了，就要遭遇扣分的危险）3.溶入团队的情况，在阿里必须和你所在的团队打成一片，这样你才能被他们所认可。4.业绩的完成情况，每个月都有不固定的kpi但这完全是我们自己定的！并不是主管给我们下达的任务。

2、阿里的“Fun文化”：

在阿里巴巴有句口号是“work with fun”，因为阿里巴巴以年轻人为主，大家都比较有活力无时不刻都想搞些新鲜的东西。给我印象最深的是在我刚入职的时个在我们部门有一个规定就是要给新人来个破冰仪式-_-!!，什么是破冰呢就是团队的每个人把你围成一圈，然后一个一个地问你一些问题，问你的恋爱史，你的家庭，你喜欢什么不喜欢什么，但这些都是次要的，他们最感兴趣的是你的有关性方面的问题，对于还是一个学生的我来说他们问的我都觉得有点过了，但是没办法，这是规矩，每个新人都得这样，就这样阿里的“fun文化”又称为“骚文化”，据说每年的年终员工大会都要评选4大名骚和四大闷骚（连马云（阿里巴巴创吏人）的卫哲｛（阿里巴巴中文站）我们的老大的老大｝也不放过。此外不同的部门还有其他的文化。在有的部门还有“裸奔文化”就是当全部门的员工努力达到目标时，该部门的主管要脱的只剩内衣在公司各楼之间“裸奔”-_-!!，不过我并没有见过.在公司见到最多的颜色就是橙色，这也许和阿里骚文化有关吧！阿里的新公司每个地方都用武侠小说的地名命名，比如有桃花岛，枫林晚等等，很多阿里人喜欢在阿里工作的秘密因为阿里的天空特别明亮，阿里的世界是自由的世界在这家员工平均年龄不到26岁，30岁已经是“老人”的公司里，为何年轻的员工都由衷地爱她、喜欢她——甚至象喜欢恋人一样地喜欢自己的公司。其中有一个秘密，这个秘密不在阿里巴巴呆过的人是无法理解和体会的。在阿里有很多传统管理学无法解释的现象：譬如在工作时间公司的办公室， GGMM们在肆无忌惮地吃零食，聊天，甚至有人聊一些黄色笑话，但这些主管都不会管的或者一群人在大声喧哗，去楼下的超市买东西，甚至有人干脆去休闲吧休息一下，找人聊聊天， 这简直 “一点组织纪律性都没有！这哪象在上班？”但是令人惊奇的是：阿里的员工工作效率出奇的高，工作的积极性不可思议，工作业绩如神州火箭一样在穿升！每天晚上都有员工自动加班至深夜，却没有想到会要一分加班工资！多少人禁不住在哭是因为公司业绩到了一个新水平而抑制不住激动！多少员工都在为公司的发展而思考观察努力着这一切的一切，如此缤纷多彩、变化无穷，却又如此严谨致密、整洁有序总之公司的用意就是让大家在工作之余能有更多的欢笑。对阿里来说，“判断一个人是不是优秀，不要看他是不是哈佛、是不是斯坦福毕业的，马云说阿里不缺人才，缺的是看这帮人干活是不是像发疯一样干，看他们每天下班是不是笑眯眯回家。” 阿里坚持：“客户第一，员工第二，股东第三“的原则可见阿里对员工是多么的好，在阿里巴巴，员工可以穿旱冰鞋上班，也可以随时来去马云卫哲的办公室，总之阿里一定要让员工感觉爽。”

3、阿里注重个人发展：

在阿里巴巴有很多业务可供人发展包括销售、客服、后台研发等，你如果不满意你当前的部门完全可以向 你的hr申请去你自己想去的部门。只要你在当前岗位上工作满一年考评合格就有资格参加内部招聘。这里的内部招聘包括淘宝、支付宝、雅虎中国、阿里巴巴等各个子公司的部门。由于我是在阿里巴巴商情发展部这是一个比较新的部门，我可以为大家多介绍一下。阿里巴巴技术部包括淘宝、支付宝、雅虎中国三个子公司的技术部门以及阿里巴巴中文站、阿里巴巴国际站、阿里软件、阿里研究院、数据库运维部等。业务上有贸易通开发、淘宝旺旺开发、搜索引擎、框架研究、网站设计、数据库设计、安全应对等等。在阿里巴巴工程技术部有测试工程师、C++工程师、Java工程师、DBA等很多职位，有很多方向可供选择。每个新员工入职后都会有一个专门的导师（我们一般都叫师父），带着熟悉业务传授知识。

4、阿里分享和倾听：

在阿里巴巴提倡分享和倾听，你可以同别人分享你的经验、挫折，在这阿里看不到竞争，因为大家都处在同一水平线上，你如果有好的东西，就要和大家分享，完全没有必要自己保留在自己的“私囊“在公司的内网上有“畅所欲言”论坛和高管的Open信箱，我们部门每周会不定期的组织几次“百科讲坛”的分享，大家有什么才艺，爱好，工作小技巧都可以拿出来和大家一起分享，有时我们分享的时间都是几个小时，但这完全和我们的工作没有冲突，因为很多分享都是和业务的联系的，在业务上面很有用。

5、阿里的使命感:

在阿里，“同学”是一种统称同事与同事之间都叫“同学“，这也是一种精神事实。在阿里，我感觉，是一个老师（马云以前是一位优秀的老师，现在还是一位优秀的老师）在带领一群学生，为了一个使命，一个理想，在不计得失地奋斗着，在朝着一个目标向前推进着，仿佛夸父追日一般，着实催人泪下，令人感动。马老师说，我们要创建一个世界一流的至少存在102年的公司，我们公司的目的不是为了在公司里面产生多少百万富翁，而是要在中国的中小企业群体中为他们产生千千万万百万富翁！在阿里的十周年庆，记得那句卫哲喊的口号 “亲爱的我愿意！你愿意吗！”台下的同学们大声回应“我愿意”，当时的场面是多么震撼多很的感人。这确确实实是一个创业型的团队，马云在这次十周年庆上说“我们要给创业的年轻人们提供一个创业的平台，在阿里实现自己的创业梦想”因为我们是在创造一个历史，在创造一个事业。当前的中国企业千千万万，请问真正是为了一个理想一种使命在奋斗的企业有几个？在阿里你真的可以感受到你是阿里的一份子，你为你在阿里而骄傲，而自豪！

来源链接：百度搜索

http://hi.baidu.com/kaoaka/blog/item/ae516c2380a429f9d7cae2de.html

赞同：26

评论：14

程序员如何提高阅读理解代码的速度和能力？

王子亭

,

http://jysperm.me

首先要对这门语言有足够的了解，比如语法，运算符优先级结合性，内存管理(默认传值还是传引用)，代码重用的机制(面向对象，或是原型链)，作用域的规则等等。虽然这些都可以用到的时候现查，但是如果你每分钟都遇到一个需要查文档才能看懂的东西，你阅读代码的速度就会很慢。

了解这门语言/技术的通用规范，例如 Node.js 用回调函数的第一个参数表示错误(而不是使用异常), Web 框架一般使用『中间件』的方式过滤请求等等。

了解你所阅读的项目，一般项目都有一个关于如何阅读代码的文档，上面会推荐你阅读代码的顺序，会介绍一些全局性质的工具的用法，例如 C 语言的项目通常会定义很多工具性质的宏。还要了解这个项目的代码是以可读性优先，还是性能优先，或者是兼容性优先，这会有助于你理解代码作者的意图。

可以先从一个经典的路径来了解项目的结构，比如对于一个 Web 框架，可以从它如何处理一个简单的请求出发，了解这个过程中经历了哪些过程，进而对这个项目的结构有一个大致的了解。

还要有合适的工具，比如一个好用的 IDE, 可以很方便地查找一个标识符的定义，以及所有用到这个标识符的地方.能够清晰地展示项目中所包含的元素(类，函数等), 以及它们的层次关系.如果能够设置断点，单步调试，就更好了。

最后要给自己设置一个目标，比如要向这个项目中添加一项功能，再或者是希望写一篇日志来介绍这个项目的结构/工作原理。没有目标的话，读起来会很迷茫。

赞同：23

评论：7

Medium.com 的前端技术基于什么，有怎样的特点？

长天之云

,

head, body { content : '' }

Medium 用了三个和知乎同样在使用的 Closure 相关工具，不得不说在 Google 之外很少见：

Closure Library

：提供定义和引用模块的方式，以及一些 UI 组件（比如编辑器，Medium 在此之上做成了无形的，真是引人注目）。

Closure Compiler

：前端代码进行优化压缩的工具。

Plovr

：Closure Library 专用的模块分组打包工具。

顾鹏

说的渲染方式有点不对，pjax 和 SPA 的技术几乎是对立的。Medium 是一个采用了 RESTful API 的 web app，它没有直接替换 HTML，而是用 JSON + 模板来生成 HTML。我认为 Medium 在服务器端和客户端共用了模板，因此它能进行一致的渲染。当首屏加载时使用服务器端渲染，之后的浏览使用客户端渲染。这样做的优点是对 SEO 友好，加载速度更快——首屏内容里面有个 embedded 字段，包含了文章的 JSON 表示，这节省了一个 HTTP 请求。文章对象里面有个有趣的地方是， HTML 的结构化内容全部用被 JavaScript 化了——精确到任何块级或内联元素—— 这样每个段落都可以由用户添加注释。

Medium 还有一篇文章分享了许多技术细节：

Just a web page?

纠正，感谢

顾鹏

提供的文章链接，观察了一些请求之后，发现 Medium 在文章页面点击左侧菜单中的 Home 链接时，使用了 pjax 加载首页的文章列表：

Request URL:https://medium.com/?format=fragmentRequest Method:GETX-Response-Type:html-body

补充文章加载过程：

# 加载主资源，文章内容：Request URL: https://medium.com/p/:postidRequest Method: GETAccept: application/json# 加载次级资源，此时文章内容已经提前显示，没有 side-loading：GET https://medium.com/p/:postid/follow-upsGET https://medium.com/p/:postid/upvotesGET https://medium.com/p/:postid/notes# 中途滚动，记录当前正在阅读的章节：PUT https://medium.com/p/:postid/state/locationRequest Payload: {paragraphName: "f169", sectionName: "0c50"}# 滚动到页面底端，标记为已读：PUT https://medium.com/p/:postid/state/read# 鼠标经过（不需要点击）在底端的导航推荐文章链接之上时，预载其内容，并渲染成 DOM：GET https://medium.com/:collection/:postidAccept: application/json

最后一步预载内容就是出现多个 surface div 的原因，Medium 做的优化，以方便快速地切换页面。

附上 DOM 断点截图（含 post 对象和模板）：

赞同：19

评论：8

成熟的Web开发团队开发、测试、上线的环境和流程是怎样的？

付强

,

www.tuer.me

1年前的问题，阿大的ppt还是12年的。。。现在我帮你回答一下吧。

先简单说下你贴的一淘那个工作环境，由于之前我也在taobao干过，知道那个daily的作用，简单说下，其实就是一套仿真的线上测试环境，包括数据，是上线前测试的最后一关，当然上daily还是需要在测试环境全测好才上的，那是最后一道关卡。

环境和流程，你贴的ppt是一种方法，细节涉及了很多，比如git和svn的操作，高级特性的使用之类。期间还介绍了一些打包的流程，目录管理的规范，命名规则之类，个人感觉不存在通用性。至少在你现在的项目中没有什么实际的借鉴价值。

现在来回答你的问题。

总结一下：

1，你需要一个可以模拟线上的开发环境。

2，你需要一个可以模拟线上的测试环境。

3，你需要一个可连调的测试环境。

4，你需要一个自动化的上线系统。

5，一个开发流程适合前后端的。

1，本地反向代理线上真实环境开发即可。（apache，nginx，nodejs均可实现）

2，模拟线上的测试环境，其实就是你需要一台有真实数据的测试机么，我建议没条件搭daily的，就直接用线上数据测好了，只不过程序部分走你们的测试环境而已，有条件搭daily当然最好咯。

3，可连调的测试环境，分为2种。一种是你们开发测试都在一个局域网段，直接绑hosts就完了，不在一个网段，就一人给一台虚拟的测试机，放在大家都可以访问到的公司内网，代码直接往上布即可。

4，自动化的上线系统，如果你们运维不给你们做，我猜你们都是直接ftp往线上扔？那么你可以自己做一个简易的上线系统。原理不复杂，每次上线时都抽取最新的trunk或master，做一个tag，再打一个时间戳的标记，然后分发到cdn就行了。界面里就2个功能，打tag，回滚到某tag，部署【够简易了吧，而且是全自动的】。

5，开发流程就是看项目了还有所用到的工具，构建，框架了。简单来说，原则就是分散独立开发，互相不干扰，连调时有hosts可绑即可。

回答了你的问题之后，我说下我自己的项目是怎么个开发流程。

灰常简单，代码管理工具是svn，起新需求就起新分支，独立开发，开发完合并到trunk，trunk不做任何开发工作，只负责merge。

上线有上线系统，你可以理解为我上面说的那个简易功能的加强版。我们是自带build的功能的。

自己编写build脚本，ant，grunt随便了。做好连到发布系统，一键集成，本地只关心源码开发。

本地环境，我拿nodejs写了一个自带rewrite，反向代理的server，超级仿真线上，一个hosts组管理的工具，一套适合自己部门的grunt插件库【就是很多很多grunt插件。。】。完全适合开发各种独立项目了。

当然如果你的测试，文档都集成在build那一步，是最棒的了。

协同合作我们是每个人开发都有一台自己的测试机，linux的，我本地也有工具可以完成自动build+push的功能。方便快捷。

可能全看下来挺复杂，不过前端工程化确实就是这个样子。帮你脱离之前的手忙脚乱，专注于业务的开发。

各位大神轻喷。我只是分享自己的经验。。

赞同：18

评论：2

如何写好技术文档？

梁涛

,

模仿是恭维最危险的形式

宣传一下自己写的东西，虽然感觉一点也不完美。

1. 一图胜千言（

http://www.ituring.com.cn/article/17520

）：

2. 大声朗读自己写的每一行字，不爽的、不通的，改之。

3. “最好的文字来自经常的修改。”

赞同：17

评论：10

面向对象中的依赖注入概念本质上是否与面向过程中的模块导入一致的？

蓝色

泻药，两者不同。

依赖注入(Dependency Injection，简称DI）体现着控制反转(Inversion of Control, 简称IoC）范式，其与你谈的#include具有着本质区别，#include以后，其主动权依然在你的手中，只是#include的东西为你提供了你可以call的东西，然而DI却不是，而是让你很舒服的使用，控制权不在你的手中。举一个简单通俗的说法（我也忘记这个说法是哪里看到的了），当你使用#include这样的方式时，如同你去青楼，做任何事情都是需要主动的，包括付钱什么的。但是，DI或者IoC这样的却不是，你只需要翻一下牌子，然后太监就用轿子把你想要的送到你的卧榻了，然后完事以后，太监就又把那位姑娘抬走。

OK，下面我也举一些简单例子来说（代码的例子来源于：Patterns of Enterprise Application Architecture这本书籍，书籍有点儿老，但是引用垠神博客的一句话来说，great ideas never die）。

class

MyMovieListener

{

public

Movie[]

moviesActedBy(String

arg)

{

List

allMovies

=

finder.findAll().

for

(Iterator

it

=

allMovies.iterator().

it.hasNext().)

{

Movie

movie

=

(Movie)

it.next().

if

(!movie.getDirector().equals(arg))

{

it.remove().

}

}

return

(Movie[])

allMovies.toArray(new

Movie[allMovies.size()]).

}}

比如这里有一个MyMovieListener类，含有一个由谁扮演的的方法moviesActedBy。而这些电影的查找核心在于了finder，由它去调用findAll方法。

好了，现在你想将finder独立出来，那么你就设计了一个MovieFinder的接口

public

interface

MovieFinder

{

List

findAll().}

代码变为了

class

MyMovieListener

{

public

MyMovieListener()

{

finder

=

new

ColonDelimitedMovieFinder("moviestest.txt").

}

private

MovieFinder

finder.}

一切都很完美，使用Colon符号分割这个movietest的文本，从而找到我需要的东西。然后突然有一天，你想使用XML来做这件事情，或者换了一个符号进行分割，那么怎么办呢？那么这样的具体实例化，显然不是一件好事，而应该由外面的东西（Assembler，如XML文件等)来负责提供必要信息后，我程序里面自动选择做什么事情，至于怎么做的，你就别管了，你只管翻牌子。这样以后，将会达到不同的图例：

通过DI，就变为这样了

而要完成这样的DI具有多种方式，比如constructor DI, setter DI, interface DI等。如果我的记忆没错的话，你说的spring就是settert DI.（很久没有做Java EE了，所以spring具体方式忘记了，不过DI和IoC的思想让我记忆颇深）。

那么，代码变为这样了：

class

MyMovieLister

{

public

void

setFinder(MovieFinder

finder)

{

this.finder

=

finder.

}

private

MovieFinder

finder.}

class

ColonMovieFinder

implements

MovieFinder

{

public

void

setFilename(String

filename)

{

this.filename

=

filename.

}

// .......}

然后，通过这样的方式，你可以在XML文件里面进行配置

<beans>

<bean id = "MyMovieListener” class = "..."

<property>

<ref ....

</property>

</bean>

<bean id = "ColonMovieFinder" class="....">

<property>

.....

</bean>

</beans>

spring快忘光了，应该大致框架如上所示，具体代码你应该比我熟，即通过这样的xml进行插件一样的插入。

那么你所需要做的就是去利用ApplicationContext载入这个XML，随后，通过getBean等方式来做（翻牌子即可，别管框架与容器怎么来做等）。

而#include则大大不同，如你#include “MyClass.h"，而MyClass.h有很多方法，如DI之前的图例一般，要做什么，调用MyClass里面的方法，请自己动手，一切主动权在你手中。

赞同：16

评论：11

豆瓣的书影音评分是如何计算的？

VeryCB

,

来知乎学习

豆瓣的评分应该用了不只一个算法，显然不可能只是按LZ所说的通过累加打分星数乘以百分比来算，那样未免太过简单。

阿北在《豆瓣电影的分数和排序是怎么算出来的？》[1] 中是这样回答的：

豆瓣250里排序是综合分数和人数产生的，这个和IMDB总的想法类似。

每一部电影的分数，确实主要是平均分数，但不简简单单是。因为偶然要和影托或者其他非正常个人意见PK，算法考虑了很多因素，包括时间和打分者自身的情况。细节不便公开，而且经常在细调。原则是尽算法范畴的所有能力去接近和还原普通观众最原汁原味的平均观影意见。

有一个因素从来没有考虑过，就是商业合作。只要我在豆瓣，商业合作和分数不会有任何关系。

前两天陈皓也在他的博文《腾讯，竞争力 和 用户体验》[2] 中提到：

对于豆瓣来说，豆瓣的每个用户都有个权威值，这个值通过用户的在线时间，发贴数量，访问次数，有没有高质量的文章，有没有参加社区活动，等等等因素，得出一个权威值。刚注册的用户权威值为0，如果有了一些负面的东西还有可能是负数，有些被社区所推崇的牛人级的用户的权威可能高达几千几万。这样，当水军和五毛们对一本书或是一个电影投票的时候，就算是数量大，但基本上没有什么作用。这就是为什么豆瓣里有的电影有70%的人投了三分或四分，但那个电影还是在快5分的样子。这就是为了维护社区的权威和质量的体现。淘宝的好评差评也是一样，但是如果可以被水军去冲的话，那就很没有意思了。看看大众点评网里的那些评论，很多都完全失去了权威。因为他们没有vote的机制。

虽然他们都没有谈到（当然也不可能谈到）算法的具体实现，但应该能在一定程度上解决LZ的困惑。推荐系统是个相当复杂的东西，它要考虑的因素非常多。当然豆瓣评分算法的目的就是保证评分的准确与公平性。

[1]

《豆瓣电影的分数和排序是怎么算出来的？》

，

http://www.zhihu.com/question/19627832

[2]

《腾讯，竞争力 和 用户体验》

，陈皓，

http://coolshell.cn/articles/5901.html

[3]

《三个评分算法》

，

http://left-uestc.com/2011/05/14/three-scoring-algorithms/

[4]

《窥视豆瓣的算法》

，

http://chungle.iteye.com/blog/542749

[5]

《从豆瓣电影的打分规则想到的》

，

http://left-uestc.com/2011/04/17/thoughts-from-scoring-rules-of-douban/

赞同：14

评论：1

如何高效地实现函数式数据结构？

vczh

,

专业造轮子 www.gaclib.net

《Purely Functional Data Structure》看完它

赞同：13

评论：0

一名合格的前端工程师的知识结构是怎样的？

徐迅

,

爱回收网小前端，2货吃货坑爹货……

引用两位大神的图：

http://www.flickr.com/photos/kejun/3114605967/

http://weibo.com/1700082927/xC029u1n8

赞同：12

评论：2

如何通过 GitHub 加入开源项目？

猫杀

,

自由开发者

有三种参与形式：

贡献代码，协作流程总是：Fork->创建分支->修改->发Pull Request

贡献文档，补充、翻译文档

报告用户体验，实际使用项目后，发issue，报告bug，提交feature请求。

贡献代码无外乎三种目的：

加feature

修bug

重构

加feature之前要寻找相关文档，一般会有文档说明design goal & concept，什么样的feature才能接受，如果不确定，总是先提交issue或者直接联系原作者讨论。

Bug的来源，自己发现的，别人提交的issue，但总是要先提交issue并告知你已经着手在做，避免没必要的重复劳动，同理，你也应该先确认有没有人已经在做。

重构是在不变更功能的情况下，改变代码架构，一般diff的足迹都较大，一定要注意沟通。

最重要的是，

一定要先看看commit log、pull request list和issue list，如果项目管理者万年没更新、不merge、不回应，就绝对不要去浪费这个时间。

对于新手

对自己能力没把握就先自己做吧，git版本控制流程、协作流程都不熟，merge conflict都没解决过就不要给人添乱了。

寻找那种有插件、扩展机制的项目，先尝试贡献插件，上手难度低，易出成果。

赞同：11

评论：0

Online Judge 是如何解决判题端安全性问题的？

时国怀

,

操作系统开发

曾经在我们学校里做过online judge，用的好像是POJ当时的一个demo，在Windows上弄的。

当时做法也没考虑太多，先是建立一个guest账户，用guest账户运行代码，所有权限全限制在某一个盘里，大不了就废了一个盘，也无所谓。

反对匿名用户说的不危险，实际上OJ这种东西太危险了，允许上传+执行权限，危险特别大。

把网页部分和代码分开，我忘记当时我们是用一个账户还是两个账户，反正网页的路径是一个很古怪的路径，这样入侵者也不太好在页面上挂马，我记得页面好像是PHP或者JSP之类的。

在编译器和连接器上做了点手脚，一共有几层防御：

第一层是把标准库里的头文件先都注释掉，包括文件操作、还有system、网络操作等等，对于一般的菜鸟就足够了，大多数菜鸟没了头文件都不知道该怎么办。

第二层是彻底干掉C++，我记得当时我们用的是MinGW，直接不安装G++组件，因为G++的库太复杂了，像cin/cout这些不好控制

第三层是修改链接库，当时在大学时候技术也很一般，我记得方法很糙，就是找到lib文件，用winhex之类的工具打开，找到fopen这些直接把所有敏感的字符串全换掉。实际上允许用的就string库和stdlib这些，这样连接器也找不到符号。

这样下来入侵者要是想通过标准库的话基本就很困难了。

在上传页面上也要做限制，比如，禁用汇编内联，直接通过过滤字符串asm实现，必要的时候做一个WindowsAPI的过滤表，在上传代码的时候就过滤掉所有WindowsAPI，但这个很困难，因为代码里可以不用字符串。

这样折腾下来，基本上把主要的入口都封死了。然后关键的一步：服务器网卡上关掉所有的端口，仅限于某几个端口开放（80/8080之类的）。

但是现在想想，并不是特别的安全，比如上传代码如果自己实现一套LoadLibrary然后直接调用WindowsAPI的话，还是可以入侵的。

至于说限制运行时间的，这个太困难了，1秒钟够执行很多指令了，没意义。

更稳妥的方法是限制注册，但这已经不是技术范畴了。

我能记得的就这些了。

赞同：10

评论：5

书上说C++是面对对象语言，这是什么意思？能举个好懂的例子吗

陈硕

,

Linux C++程序员，muduo 网络库作者

http://www.stroustrup.com/whatis.pdf

http://www.stroustrup.com/oopsla.pdf

赞同：10

评论：1

怎样看待下一代 ASP.NET 将全部开源，并同时支持 Windows，Linux 和 Mac？

赵冬毓

,

真的勇士敢于用自己的摘要算法生成自己毕设的摘要，所以我是个懦夫……

忽然发现这个问题好像刚刚答过的问题

ASP.NET开源以后会有更多的网站选择这个平台么？

#的答案就能答……

以前整个

ASP.NET

技术栈就是开源的，从Web Form到SignalR都是开源的，我在最近两年的工作中随时需要自己为

ASP.NET

扩展接口的时候就去CodePlex上看

ASP.NET

的源代码，照着改就可以了，现在唯一的改变是，微软的开源技术栈现在接受非微软代码在经过审核后被合并进官方分支，并且，

ASP.NET

入驻了被码农界认可的GitHub，而不是继续在CodePlex上，因为开源界对CodePlex一直敌视，认为这是微软分化开源界的阴谋，而且对于连“开源都不肯跟我们公用一个平台”的开源项目，开源界总会有各种说辞。微软在过去的市场表现可以证明，微软在相当长时间里并不具备良好的舆论形象，恶劣的舆论形象被华尔街、财团和竞争对手稍加利用就可以对业绩形成明显打击。

当然以后估计很多人会因为审核问题骂微软不诚意，所以先说一句，按照微软Code Review的尿性，你的代码多半是不会被接受的，想我一个学长，去年7月15号入职STC，起初参与IE项目，直到11月初，才被主分支接受了130行代码，这几行代码被中国大叔大妈、美国大叔大妈、日本大叔大妈、印度大叔大妈、澳大利亚大叔大妈轮流Review，曾经有过10天103条待修复Comments的记录，今年代码的被接受数量才逐渐上来，最近推送的设备健康助手就是出自这家伙之手的……我一个同级同学计划毕业后入职微软苏州，他实习时是在微软上海的产品部门，他到那里的头两个月，代码几乎不被接受，被打回重构是家常便饭，你的代码想进微软官方分支，如果写不出微软官方的整洁风格，是不被认可的。查阅任何公开发布的产品的源代码（研究院出的代码就……那纯粹是大神们为了吓唬小朋友），你会有一种这么多代码是一个人写的的错觉，这样微软的目的就达到了。

另外说，MVC、Web API和SignalR不再依赖System.Web，转而全部继承自Own，这不是说运行时改变了，而是说MVC、Web API和SignalR这三个使用方式本来就是接近Web开发本源的框架终于不再是基于System.Web这个将Web Server、OS、Request、Response、Context、Session等等与Web有关或无关的都整合在一起的，原始结构是为Web Form设计的基础框架，而是基于OData标准直接构造一个从协议栈到Web Application的简单明了的框架。也使得移植变得容易很多，原来需要改造Web Server使其能够提供System.Web需要的各种附加信息才能进行的移植，现在只要支持OData，就可以移植了。

所以总结起来：

1.这次发布是将

ASP.NET

的源代码从CodePlex转移到GitHub，因为CodePlex开源平台一直以来不被开源界认可，微软高调宣布进驻GitHub表明微软意识到舆论形象是个重要的资产，甚至影响到自身业绩，这个动作的象征意义更大。

2.按照微软的质量标准，接受第三方代码并不容易。

3.跨平台变得更加容易，整个框架的结构也更加清晰。

4.Mono和Xamarin的春天到了，也有可能，微软在计划着收购Mono和Xamarin了……

5.尝试打消开源界的固有偏见，赢得部分宗教式的开发者，对自己大有好处。

6.网站的话，可能会吸引新兴开发者，而已经发展到具有一定规模的互联网企业，短时间内是不会换平台的。

赞同：8

评论：6

如何面试前端工程师？

助你软件工作室

所谓：闻道有先后，要了解他的学习能力，一个东西他努力一周就能上手干事，一月能有自己的独到意见，半年能有独挡一面的能力，以“闻道先”去判断一个人的能力往往是有问题的

赞同：8

评论：1

Summly 是怎么将一大段文本自动转换成摘要的？

崇慕

,

游戏蛮牛创始人

如果我做的话,尝试思路如下:

简单画一个图.

具体算法很细节,例如:

加重关键词数量,

是否有重复,

有叹号的语句数量.

.....

赞同：6

评论：0

学习编程能帮助提高逻辑思维能力么？

vczh

,

专业造轮子 www.gaclib.net

如果你就是冲着提高逻辑思维能力去的，那应该去学数学分析。如果你还喜欢编程的话，那还可以学Haskell。Haskell程序，只要编译过了基本没有运行时的问题，但是要把一个错误的Haskell程序弄到可以编译，跟你debug一个错的程序难度差不多。

赞同：5

评论：17

国外，前端领域有什么出名的论坛或者社区？

尤雨溪

,

不会搞艺术的程序员不是好设计师

jsconf 系列的视频 youtube 上有很多，翻墙上去看还是值得的，不过可能对英语听力有些要求。

社区的话：

- Twitter，多 follow 些前端界人士，follow 的人够多了一般最新的东西出来都能跟到。我的 JavaScript list:

https://twitter.com/youyuxi/lists/javascript

- GitHub（看看各大知名项目的 issue 讨论，可以了解项目的走向）

- 用户自主发布新闻的，比如 Reddit 的 javascript 频道，EchoJS

- StackOverflow 算不算...

赞同：5

评论：1

新浪微博授权为什么要设置时效？

Dylan

,

金融行业挨踢人士

-

因为目前新浪微博开放平台用户身份鉴权使用OAuth2.0协议（不单单新浪，腾讯、网易、人人...）

在OAuth2.0协议中

用户授权应用之后，开放平台会给应用一个用户的AccessToken

AccessToken中除了携带用户授权给应用的操作范围，还会带有ExpiredTime

这就是为什么新浪微博授权带有时效的原因

参看：

授权机制说明

OAuth2协议参看：

RFC 6749 - The OAuth 2.0 Authorization Framework

-

赞同：3

评论：11