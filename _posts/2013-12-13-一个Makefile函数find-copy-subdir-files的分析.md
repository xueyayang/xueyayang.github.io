---
layout: default
---

一个Makefile函数find-copy-subdir-files的分析
=============================================

出处
-------------------------
`find-copy-subdir-files`函数是Android源码
>A20-Homlet-V1.0_ss/android/build/core/product_config.mk

中，定义如下：

{% highlight Makefile%}
# TODO: push this into the combo files; unfortunately, we don't even
# know HOST_OS at this point.
trysed := $(shell echo a | sed -E -e 's/a/b/' 2>/dev/null)
ifeq ($(trysed),b)
  SED_EXTENDED := sed -E
else
  trysed := $(shell echo c | sed -r -e 's/c/d/' 2>/dev/null)
  ifeq ($(trysed),d)
    SED_EXTENDED := sed -r
  else
    $(error Unknown sed version)
  endif
endif

###########################################################
## List all of the files in a subdirectory in a format
## suitable for PRODUCT_COPY_FILES and
## PRODUCT_SDK_ADDON_COPY_FILES
##
## $(1): Glob to match file name
## $(2): Source directory
## $(3): Target base directory
###########################################################

define find-copy-subdir-files
$(shell find $(2) -name "$(1)" | $(SED_EXTENDED) "s:($(2)/?(.*)):\\1\\:$(3)/\\2:" | sed "s://:/:g")
endef
{% endhighlight%}

作用
-----------------------------------
这个函数根据指定的文件通配符(如`*.apk`)，扫描指定目录下所有符合要求的文件，再根据指定的目标路径，生成一个字符串。这个字符的形式是`src:dst`。使用实例参见[Android预装APK][]


将函数体分成几部分
-------------------------------
函数体由管道符号`|`分成3部分：

* 先执行一个`find`命令，找到符合条件的文件名
* 交给`sed`程序处理，由第一个正则表达式处理
* 再交给`sed`程序处理，由第二个正则表达式处理


###最外层
{% highlight Makefile%}
$(···)
{% endhighlight%}
是Makefile定义函数固有的形式。里面的内容才是真正的函数体。

### shell 关键字
{% highlight bash%}
shell ···
{% endhighlight%}
这表示调用shell来执行后面的 shell 命令。类似于在终端于输入：
{% highlight bash%}
bash xxxx
{% endhighlight%}
来执行命令。
推测在别的地方有一个选择机制，用来确定shell到底调用的是`bash`还是`sh`命令。暂时没研究。

### find 命令
{% highlight Makefile%}
find $(2) -name "$(1)"
{% endhighlight%}

find命令的经典用法。在某目录下，根据 名字，即`name`来查找文件。
其中`$(2)`指的是该函数的第二个入参数，`$(1)`指的是第一个入参。Makefile的语法还真是简单(丑陋)。

### $(SED_EXTENDED)
这个变量，实际是一个带参数的命令：`sed -r`，对find的结果进行一次处理。其生成过程另起一节单独分析。

### 第二次


SED_EXTENDED变量的生成过程
-------------------------------
代码里也给出来了。在我的环境里，走的第二条分支：
{% highlight Bash%}
...
else
  trysed := $(shell echo c | sed -r -e 's/c/d/' 2>/dev/null)
  ifeq ($(trysed),d)
    SED_EXTENDED := sed -r
{% endhighlight%}

1. 用`echo c`往标准输出里输出一个字母`c`。
2. 接着通过重定向符号`|`交给`sed`程序
3. `sed -r -e 's/c/d'`表示：
	* `-r`，使用扩展的正则表达式，而不是基本的表达式。(两者区别水很深，勿自扰)。
	* `-e`，表明后面跟的是个可执行的脚本表达式(Expression)。相对的，可以是`-f`,表明跟了个脚本文件。
	* `s/c/d/`，服务于上面的`-e`，即要执行的正则表达式。这个表达式的意思是：将“流”中间的字母“c”替换为字母“d”。起始的“s”是“substitute”的缩写，表示替换。编译器VIM中的正则替换也是这样用。接下来用斜杠分隔，依次给出“原有的文字”和“替换后的文字”。形成`s/src/dst/`的格式,将src替换成dst。显然这里面的字母“c”是前面`echo c`命令发出的。
4. `2>/dev/null`表示将整条命令执行完后，**丢弃所有的标准错误输出**。
	* `2`表示bash命令执行后的标准错误输出。类似的，`1`表示执行后的标准输出。(这些古老的语法真是要了命。)
	* `>` 也是管理重定向符号，表示将前面的内容写到后面。
	* `/dev/null`，这不是一个文件，写到这里跟没写一样。“丢弃”的动作就是这样产生的。
5. `trysed := ···`，整条命令执行完后，将结果赋给`trysed`变量
6. `ifeq ($(trysed),d)`，比较`$(trysed)`的值是否为`d`。这是种操作符前置的写法，`ifeq`表示比较动作，后面是两个参数。貌似近几年炒的很火的“函数式编程”里很推崇。《黑客与画家》里，Paul Graham大加推崇的Lisp就是这么一种语言。
7. 显然如果3里面`sed -r -e '/s/c/d'`命令如果行的通的话，$(trysed)的值就应该是d。这样，`SED_EXTENDED`变量的值就被赋成了`sed -r`。

####补充
标准输出与标准错误输出。在我的机子上，如果执行第二条分支里的sed命令：
{% highlight Bash%}
echo c | sed -r -e 's/c/d/' 2>/dev/null
{% endhighlight %}
正确执行，则是标准输出，如下：
>

执行第二条分支里的sed命令，
{% highlight Bash%}
echo a | sed -E -e 's/a/b/' 2>/dev/null 
{% endhighlight %}
是标准错误输出，如下：
>


sed是一个古老的流处理编译器(Stream EDitor)。可以简单理解为一个正则表达式解释器，对指定“流”里的内容执行正则替换、编辑等(可选：神乎其技的)操作。所谓“流”，上面echo出来的字母`c`，输入管道重定向就是一种简单的“流”。

正则表达式的(sed脚本)的解释
-------------------------------
{% highlight bash%}
"s:($(2)/?(.*)):\\1\\:$(3)/\\2:"  
{% endhighlight%}
先给出结论：这个正表达式通过**替换**与**拼接**，由旧字符串`src_string`，生成一个新字符串`src_string:dst_string`。。新字符串由两部分组成，由冒号分隔隔开。第一部分是是旧字符串保持不变，第二部分由旧字符串替换前缀生成。

理解起来很难，说起来也难以摹状，不如先写个测试脚本，看看直观的效果。代码如下：
{% highlight bash%}
#sed_command.sh
name="*.apk"  	    #$(1)
src="./apk"		    #$(2)
dst="system/app"    #$(3)

SED_EXTENDED="sed -r" 

echo "$name"
echo $src			
echo $dst

#find 命令的输出
find $src -name "$name" > 01.txt 
#上一步结果经过第一个sed 脚本的输出。
find $src -name "$name" | $SED_EXTENDED "s:($src/?(.*)):\\1\\:$dst/\\2:" > 02.txt 
#上一步结果继续经过第二个sed 脚本的输出
find $src -name "$name" | $SED_EXTENDED "s:($src/?(.*)):\\1\\:$dst/\\2:" | sed "s://:/:g" > 03.txt
{% endhighlight%}

测试意图在注释里体现。思路为将函数`find-copy-subdir-files`的定义人肉编译成可执行的shell命令，执行并查看结果。
在sed_command.sh脚本同级目录新建一个`apk`文件夹，放入两个apk文件。执行后，输出如下：
>########01.txt内容##########  
>./apk/iFlyIME_v4.0.1437.apk  
>./apk/hd3-315-arm-b13034-generic.apk  

>########02.txt内容##########  
>./apk/iFlyIME_v4.0.1437.apk:system/app/iFlyIME_v4.0.1437.apk  
>./apk/hd3-315-arm-b13034-generic.apk:system/app/hd3-315-arm-b13034-generic.apk  

>########03.txt内容##########  
>./apk/iFlyIME_v4.0.1437.apk:system/app/iFlyIME_v4.0.1437.apk  
>./apk/hd3-315-arm-b13034-generic.apk:system/app/hd3-315-arm-b13034-generic.apk  


现在先看前两步的输出:

* `01.txt`文件中，`find`命令找到了两个apk文件 
* `02.txt`文件，第一个sed脚本将结果处理成了`src_string:dst_string`的形式
	* 由一个字符串变成两个字符串，与前面结论相符。
	* 旧字符串的`./apk`与被换成了`system/app` ，前缀替换，与前面结论相符。

对照正则表达理解：
{% highlight bash%}
"s:($(2)/?(.*)):\\1\\:$(3)/\\2:"  
{% endhighlight%}

以冒号为分隔开，即为`substitute:Src_String:Dst_String:`

1. 开头的`s`表示替换
2. 第二部分是重点：`($(2)/?(.*))`，对应于源字符串。
	*先把`$(2)`替换成`$src`，变成`($src/?(.*))`
	*以小括号为单位，变成`(···(···))`,
		*外层的小括号包括的内容，以标号`1`被后面引用，
		*内层的小括号包括的内容，以标号`2`被后面引用，
	*关注非小括号的内容`$src/?(.*)`，这表示以`$src`开头的字符串都符合要求, 即`./apk/···`
		* `?`重复零次或一次，这里对`/`起作用。重复1次好理解，表示`$src`后有子目录。重复0次，表示`$src`为空的情况。
		*`.`匹配除换行符以外的任意字符
		* `*`重复零次或更多次， 这里对`.`起作用
3. 第三部分是目标字符串，虽然长，不难理解：`\\1\\:$(3)/\\2`	
	* 双反斜杠`\\`，第一个用于转义
	* `\\1`实际上最后是`\1`，在正则表达式里，表示2里的外层小括号包括的所有内容。即源字符串。
	* `\\:`实际上最后是`\:`，在正则表达式里，表示的是一个冒号`:`。即`02.txt`中，两个字符串中的冒号。
	* `$(3)/\\2`，即`02.txt`中冒号后的一部分，目标字符串。
		* 将$(3)替换成$dst
		* `\\2`实际上最后是`\2`,在正则表达里，表示2里的内层小号包括的所有内容，即找到的apk文件名。
		* 最终匹配的字符串，即 `system/app/···`

理解第一个正则表达式，第二个正则表达式就很好理解了。
{% highlight Bash %}
sed "s://:/:g"
{% endhighlight %}
将双斜杠`//`替换为单斜杠`/`。

结论
-------------------------------
* Makefile语法怪异。
* 正则表达式水深，勿自扰。

[APK2ROM]: 

