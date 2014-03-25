---
layout: default
---

How to Install Jekyll 
=====================



1 问题
====
换了台机子，得重新安装jekyll。以方便在本地查看博客效果。
上次折腾了好久配置成功后，觉得没有记录的必要。现在脑子
空空，不知从何做起。看来，事无巨细，还是要记录。

2 方法
====
到jekyll[官网][1]，参照首页说明：
{% highlight bash %}
gem install jekyll
{% endhighlight %}

2.1 卡住了
------
通常由于国内的网络环境，运行这个命令后就卡住了。由于对Ruby和Gem一无所知，
上网搜索一番，才知道可以加个`-V`。
{% highlight bash %}
gem install jekyll -V
{% endhighlight %}

但看看也只是看看，毫无办法。换个时间再试试吧。——顺利的时候十分钟左右就安装完毕，不顺的时候，等一下午也无果。千万别叫劲。

2.2 其他依赖
--------
如果上述命令不成功，很可能是缺乏依赖库。好在这个依赖好像不多。
{% highlight bash %}
sudo yum install gem
sudo yum install ruby-devel
{% endhighlight %}

3 总结
====
- 最近总在怀疑，折腾这些配置与安装到底值不值得。因为花掉了太多时间。而用这些，初衷却是为了节省时间，高效。
- 现在安装Jekyll好像方便很多了。一条命令搞定。还能创建个模板。自己当初照着阮一峰的博客折腾的啊。那个惶恐。
- 这些软件虽然很酷，但是入门成本偏高。得不停掌握新知识，比如对我来说，Ruby就是。何况非程序员乎？

[1]: http://jekyllrb.com/
