---
layout: default
---

Convert 1 Int to 4 char in Java
================================

问题
====
一个int类型，转换成4个char。比如v4l2中的图像格式，是个整型。这个整型是
由4个char排列开来组成的，共计32位。

得到了图像格式，一个整型，自然想转回去看看。


方法
=====
{% highlight java%}
int cur = 842094169;
byte[] fourcc = ByteBuffer.allocate(4).putInt(cur).array();
String str = new String(fourcc,"UTF-8");
String str_reverse = new StringBuilder(str).reverse().toString();
Log.i(TAG, str_reverse);
{% endhighlight %}

总结
====
- 这个程序价值不大。主要认识Java中的类型。
- Java编程的风格，可见一斑。

