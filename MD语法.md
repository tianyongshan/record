# Heading level 1  
## Heading level 2  
### Heading level 3  
#### Heading level 4  
##### Heading level 5  
###### Heading level 6  
  
  
I just love **bold text**.  
Italicized text is the *cat's meow*.  
> Dorothy followed her through many of the beautiful rooms in her castle.  
  
> Dorothy followed her through many of the beautiful rooms in her castle.  
>  
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.  
  
> Dorothy followed her through many of the beautiful rooms in her castle.  
>  
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.  
  
  
> #### The quarterly results look great!  
>  
> - Revenue was off the chart.  
> - Profits were higher than ever.  
>  
>  *Everything* is going according to **plan**.  
  
1. First item  
2. Second item  
3. Third item  
    1. Indented item  
    2. Indented item  
4. Fourth item  
  
  
- First item  
- Second item  
- Third item  
- Fourth item  
  
* First item  
* Second item  
* Third item  
* Fourth item  
  
+ First item  
+ Second item  
+ Third item  
+ Fourth item  
  
- First item  
- Second item  
- Third item  
    - Indented item  
    - Indented item  
- Fourth item  
  
  
***  
  
---  
  
_________________  
  
  
  
`Hello Word`  
  
  
```javascript  
	// An highlighted block  
	var foo = 'bar';  
```  
  
  
 [访问CSDN](https://wuwufq.blog.csdn.net/)  
 <https://wuwufq.blog.csdn.net/>  
  
  
- 无序列表  
  * 项目  
    + 项目  
  
1. 有序列表  
2. 项目2  
3. 项目3  
  
- [ ] 计划任务  
- [x] 完成任务  
  
  
Markdown  
:  Text-to-HTML conversion tool  
  
Authors  
:  John  
:  Luke  
  
  
学生 | 成绩  
 -- | --  
张三  | 80  
李四  | 90  
王二  | 95  
  
| Column 1 | Column 2 | Column 2    
|:--|:--:| --:|  
|  文本居左 |  文本居中 |  文本居右 |  
  
  
  
一个具有注脚的文本。[^1]  
  
[^1]: 注脚的解释  
  
  
  
```mermaid   
	sequenceDiagram  
	张三 ->> 李四: 你好！李四, 最近怎么样?  
	李四-->>王五: 你最近怎么样，王五？  
	李四--x 张三: 我很好，谢谢!  
	李四-x 王五: 我很好，谢谢!  
	Note right of 王五: 李四想了很长时间, 文字太长了<br/>不适合放在一行.  
  
	李四-->>张三: 打量着王五...  
	张三->>王五: 很好... 王五, 你怎么样?  
```  
  
```mermaid  
	gantt  
       	 dateFormat  YYYY-MM-DD  
       	 title Adding GANTT diagram functionality to mermaid  
       	 section 现有任务  
       	 已完成               :done,    des1, 2014-01-06,2014-01-08  
       	 进行中               :active,  des2, 2014-01-09, 3d  
         计划中               :des3, after des2, 5d  
```  
  
```mermaid  
	graph LR  
	A[长方形] -- 链接 --> B((圆))  
	A --> C(圆角长方形)  
	B --> D{菱形}  
	C --> D  
```  
  
```mermaid  
	flowchat  
	st=>start: 开始  
	e=>end: 结束  
	op=>operation: 我的操作  
	cond=>condition: 确认？  
  
	st->op->cond  
	cond(yes)->e  
	cond(no)->op  
```  
  
```mermaid  
	classDiagram  
    	Class01 <|-- AveryLongClass : Cool  
    	<<interface>> Class01  
    	Class09 --> C2 : Where am i?  
   	 	Class09 --* C3  
    	Class09 --|> Class07  
    	Class07 : equals()  
    	Class07 : Object[] elementData  
    	Class01 : size()  
    	Class01 : int chimp  
    	Class01 : int gorilla  
    	class Class10 {  
        	>>service>>  
        	int id  
        	size()  
    	}  
```  
  
**文本加粗**   
\*\* 正常显示星号 \*\*  
  
  
  
  
  
  
  
图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png)  
  
带尺寸的图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png =60x60)  
  
宽度确定高度等比例的图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png =60x)  
  
高度确定宽度等比例的图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png =x60)  
  
居中的图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png#pic_center)  
  
居中并且带尺寸的图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png#pic_center =60x60)  
  
居右的图片: ![Alt](https://i-blog.csdnimg.cn/blog_migrate/8f1b213356ed81d5a706d52c6ab7cb6d.png#pic_right)  
  
  
  
