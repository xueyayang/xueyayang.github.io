---
layout: default
---

编写JNI代码-Android程序JNI编程（二）
===============

问题
====
[声明][1]并[实现][2]JNI接口后，如何在JAVA层调用？


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

[1]: http://xueyayang.github.io/2014/01/15/%E7%94%9F%E6%88%90JNI%E6%8E%A5%E5%8F%A3-Android%E7%A8%8B%E5%BA%8FJNI%E7%BC%96%E7%A8%8B%EF%BC%88%E4%B8%80%EF%BC%89.html
[2]: http://xueyayang.github.io/2014/04/02/%E7%BC%96%E5%86%99JNI%E4%BB%A3%E7%A0%81-Android%E7%A8%8B%E5%BA%8FJNI%E7%BC%96%E7%A8%8B%EF%BC%88%E4%BA%8C%EF%BC%89.html
