---
layout: default
---

delete之后还需要置NULL吗？
=========================

1 问题
====

对指针变量进行delete操作后，还需要置NULL吗？如下面的常见操作：
{% highlight cpp %}
node* temp = tree.get_root();
.....

delete temp;
temp = NULL;
{% endhighlight %}

最后的一句`temp = NULL;`是否多余？


2 解答
====

2.1 这样的操作是必要的
-------------------

答案是，这样做是必要的。

2.2 实验
----

如下面的代码：
{% highlight cpp %}
ERIC_TEST(b_tree, delete_char_array)
{
	char *array = new char[10];
	snprintf(array,10,"hello");
	printf("%s\n", array);

	// delete
	delete array;

	// check
	if(array != NULL){
		printf("array != NULL\n");
	}
}
{% endhighlight %}

运行的结果是：
{% highlight bash %}
hello
array != NULL
{% endhighlight %}

2.3 为什么会这样？
--------------

这个与直觉相悖的。delete就意味着要将资源释放了，那么指向这块资源的变量，自然失去了意义。
置为NULL是个很自然的步骤。但是，**C++为什么没有实现呢？**

原因是，**有时候要置为NULL对象不存在**。考虑**右值**的例子。

如：
{% highlight cpp %}
int* f();
int* p;
//...
delete f(x);
delete p+1;
{% endhighlight %}

在上面的例子中，delete的操作对象(operand)是右值，右值的特征就是，过了所在行，
就不存在了。所以，直觉里delete的两个操作：

- 释放所指向的资源
- 将变量置为NULL（对右值无法实现）
第二个是无法实现的。

所以C++的标准里，并没有规定`delete`必须得将其`operand`置为NULL。具体到各家的编译器实现，如GCC/VC，也都没有置为NULL的操作。——“实验”一节的代码，在GCC与VC下编译，运行结果无差别。

[Stroustrup][1]也讲解了这个问题，并[抱怨][2]说，“对于左值还是很鼓励实现`置NULL`的，但是`implementers`都不怎么在意”。

2.4 一个使用场景
------------

在进行二叉树查找并删除时，会出现下面的代码:
{% highlight cpp %}
node* temp = tree.get_root()
while(temp != NULL){
	....
	delete temp;// 完成删除操作
	temp = NULL;// 置NULL，结束while
}
{% endhighlight %}

如果很确定被delete的指针变量，不会在别处被使用（如局部临时变量），那么少了置NULL的操作，也不会造成危害。——当然，这有自找麻烦的嫌疑。

3 结论
====

- 方便保险起见，delete之后，需要将指针变量置NULL。

[1]: http://en.wikipedia.org/wiki/Bjarne_Stroustrup
[2]: http://www.stroustrup.com/bs_faq2.html#delete-zero
