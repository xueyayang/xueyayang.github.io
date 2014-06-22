---
layout: default
tag: git
---

git配置diff-tool为meld
=====

问题
====

git diff 的工具换成meld。

解决
====

配置文件所在的路径
------------------

> ~/.gitconfig

git 中的对应选项
----------------

git提供的key与value如下，来修改选用的diff工具。
{% highlight bash %}	
# key: diff.external
# value: /home/eric/git_diff_meld.sh
[diff]
	external = /home/eric/git_diff_meld.sh
{% endhighlight %}

给meld传正确的参数
------------------
要将带比较的两个文件传给meld。这个需要参考git的手册，看diff命令是如何将被比较项传出来的。

{% highlight bash %}
# filename: git_diff_meld
#!/bin/bash
meld $2 $5
{% endhighlight %}

可见git传出的命令很多，但是之用到了`$2`与`$5`。

别忘了:
> chmod +x git_diff_meld.sh

总结
====

- 琐碎的东西，记录下来是为了新环境中节省时间。
- 随后记录配置svn的diff-tool为meld

