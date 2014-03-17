---
layout: default
---

Ubuntu下开启SSH服务
===================

问题
====
开启SSH服务，使别的机子可以通过SSH登录。也可以clone本机的git库。


方法
====
SSH服务与WEB服务一样，首先得下载个具体的软件，比如Apache。就是实现。然后安装，启动。
LINUX下比较好的实现，应该是OpenSSL了吧。

安装
-----
{% highlight bash%}
sudo apt-get install openssh-server
{% endhighlight %}

启动
----

{% highlight bash%}
sudo /etc/init.d/ssh restart
{% endhighlight %}

测试
----
在有客户端的机器上，运行。这个测试例子来自于[github 的帮助文档][1]。写的非常漂亮。如果是需要操作git库，才用到SSH。这篇帮助一定要看。
{% highlight bash %}
ssh -T user@192.168.xxx.yyy
{% endhighlight %}

结论
====
非常简单的过程。适用于对SSH缺乏认识，又需要使用库的情况。如：

- 远程登录
- git clone


[1]:  https://help.github.com/articles/generating-ssh-keys
