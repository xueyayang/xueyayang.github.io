---
layout: default
tag: svn,config
---

svn配置diff-tool为meld
=====

1 问题
====

svn diff 的工具换成meld。

2 解决
====

2.1 配置文件所在的路径
------------------

> ~/.subversion/.config

2.2 svn 中的对应选项
----------------
svn提供了默认的配置模板，所以找到其中对应项，放开即可：
{% highlight bash %}	
# key: diff.external
# value: /home/eric/svn-diff-meld.sh
editor-cmd = vim
diff-cmd = svn-diff-meld.sh
{% endhighlight %}

2.3 给meld传正确的参数
------------------
要将待比较文件作为参数传给meld。这个需要参考svn的手册，看diff命令是如何将被比较项传出来的。

{% highlight bash %}
# filename: svn-diff-meld.sh
#!/bin/sh
DIFF="meld"
LEFT=${6}
RIGHT=${7}

$DIFF $LEFT $RIGHT
{% endhighlight %}

可见svn传出的参数很多，但是之用到了`${6}`与`${7}`。

注意这里取参数是加了大括号的。

别忘了:
> chmod +x svn-diff-meld.sh

3 总结
====

- 琐碎的东西，记录下来是为了新环境中节省时间。
- git对应的配置在[这里][1]

[1]: http://xueyayang.github.io/2014/06/22/git%E9%85%8D%E7%BD%AEdiff-tool%E4%B8%BAmeld.html

