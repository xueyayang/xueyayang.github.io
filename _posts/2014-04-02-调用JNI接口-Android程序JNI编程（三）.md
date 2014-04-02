---
layout: default
---

编写JNI代码-Android程序JNI编程（二）
===============

问题
====
[声明][]并[实现][]JNI接口后，如何在JAVA层调用？


方法
====

加载生成的so库。
{% highlight java %}
static {
		System.loadLibrary("native_process_preview");
}
public static native int  n_native_process_preview(byte[] preview_data);
{% endhighlight %}

注意库的名字，是去掉了`lib`前缀，与`.so`后缀的。


总结
===
- 正在补充中...

[1]:
[2]:
