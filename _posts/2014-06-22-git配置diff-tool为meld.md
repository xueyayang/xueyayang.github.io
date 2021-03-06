---
layout: default
tag: git
---

git配置diff-tool为meld
=====

1 问题
====

git diff 的工具换成meld。

2 解决
====

2.1 配置文件所在的路径
------------------

> ~/.gitconfig

2.2 git 中的对应选项
----------------

git提供的key与value如下，来修改选用的diff工具。
{% highlight bash %}	
# key: diff.external
# value: /home/eric/git_diff_meld.sh
[diff]
	external = /home/eric/git_diff_meld.sh
{% endhighlight %}

2.3 给meld传正确的参数
------------------
要将待比较文件作为参数传给meld。这个需要参考git的手册，看diff命令是如何将被比较项传出来的。

{% highlight bash %}
# filename: git_diff_meld
#!/bin/bash
meld $2 $5
{% endhighlight %}

可见git传出的参数很多，但是之用到了`$2`与`$5`。

别忘了:
> chmod +x git\_diff\_meld.sh

3 总结
====

- 琐碎的东西，记录下来是为了新环境中节省时间。
- svn对应的配置在[这里][1]。


[1]: http://xueyayang.github.io/2014/06/23/svn%E9%85%8D%E7%BD%AEdiff-tool%E4%B8%BAmeld.html

