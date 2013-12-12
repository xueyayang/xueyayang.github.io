---
layout: default
---

Android编译过程中build.prop文件的生成
========================================

build.prop文件的介绍
---------------------

###位置
build.prop文件位于:
>$A20\_SRC/android/out/target/product/sugar-xbh\_fjb/system

其中 sugar-xbh_fjb 是产品代号，根据实际开发情况来切换。

###作用
该文件主要用于定义ROM的一些属性，如：

* 设定ROM的Locale,如默认语言、地区等。
* [设定ROM的默认Launcher](https://xueyayang.github.io/2013/12/04/A20%E8%AE%BE%E5%AE%9A%E9%BB%98%E8%AE%A4Launcher.html)
* 设定dalvkik虚拟机的堆大小(dalvik.vm.heapsize)。

初步推测，凡是Android系统中用XX.YY.ZZ定义的属性，都可以在这里更改。

###内容
选取该文件的一部分来看：
>ro.build.display.id=sugar\_xbh\_fjb-eng 4.2.2 JDQ39 20131211 test-keys  
>ro.build.version.incremental=20131211  
>ro.build.version.sdk=17  
>ro.build.version.codename=REL  
>ro.build.version.release=4.2.2  
>ro.build.date=Wed Dec 11 19:16:02 CST 2013  
>
>....
>
>ro.sw.defaultlauncherpackage=com.luxtone.tuzi3  
>ro.sw.defaultlauncherclass=com.luxtone.tuzi3.activity.Main  
>ro.product.locale.language=zh  
>ro.product.locale.region=CN  

信息分两种：

1. 说明信息
    * 产品名字。（sugar\_xbh\_fjb-eng）
    * Build 时间。 （Wed Dec 11 19:16:02 CST 2013）
2. ROM属性信息
    * 设置默认的Launcher 
    * 设置默认语言与地区

build.prop文件的生成？
------------------------

###从 PRODUCT\_PROPERTY\_OVERRIDES 变量谈起
[如何替换默认Launcher](https://xueyayang.github.io/2013/12/04/A20%E8%AE%BE%E5%AE%9A%E9%BB%98%E8%AE%A4Launcher.html)一文里，我提到:
在sugar\_xbh\_fjb.mk文件中，为PRODUCT\_PROPERTY\_OVERRIDES增加两项属性，即可替换默认Launcher。结合上面谈到的build.prop的作用，可以推测：为该变量增加的值，势必经过一些机制，而最终被写到了build.prop里。因为那里才是真正起作用的地方。这个机制是什么？变量值如何从.mk文件流动到了build.prop？正是本文试图说明的。

###谁包含了build.prop?
全目录搜索:
{% highlight bash %}
grep -rn "build.prop" .
{% endhighlight %}
发现包含文件名的，都是一些.mk文件。结合搜索来的信息，除去一些平台相关的mk文件，最后锁定：
>$A20\_SRC/android/build/core/Makefile  

##Makefile文件里写了什么？
打开上面提到的Makefile文件，有这么一段：
{% highlight Makefile %}
# -----------------------------------------------------------------
# default.prop
INSTALLED_DEFAULT_PROP_TARGET := $(TARGET_ROOT_OUT)/default.prop
ALL_DEFAULT_INSTALLED_MODULES += $(INSTALLED_DEFAULT_PROP_TARGET)
ADDITIONAL_DEFAULT_PROPERTIES := \
    $(call collapse-pairs, $(ADDITIONAL_DEFAULT_PROPERTIES))
ADDITIONAL_DEFAULT_PROPERTIES += \
    $(call collapse-pairs, $(PRODUCT_DEFAULT_PROPERTY_OVERRIDES))
ADDITIONAL_DEFAULT_PROPERTIES := $(call uniq-pairs-by-first-component, \
    $(ADDITIONAL_DEFAULT_PROPERTIES),=)

#以下为写入操作

$(INSTALLED_DEFAULT_PROP_TARGET):
    @echo Target buildinfo: $@
    @mkdir -p $(dir $@)
    $(hide) echo "#" > $@; \
            echo "# ADDITIONAL_DEFAULT_PROPERTIES" >> $@; \
            echo "#" >> $@;
    $(hide) $(foreach line,$(ADDITIONAL_DEFAULT_PROPERTIES), \
        echo "$(line)" >> $@;)
    build/tools/post_process_props.py $@
# -----------------------------------------------------------------


# -----------------------------------------------------------------
# build.prop
...
# -----------------------------------------------------------------
{% endhighlight%}

从注释可以看出，该文件在生成我们的目标：build.prop前，先生成了一个叫default.prop的文件,
    只用了十几行。Makefile的语法本身古老晦涩，难以理解，加之生成build.prop的代码又很长，直接看难度很大。他山之石，可以攻玉。不如先研究如何生成default.prop文件,毕竟软柿子好捏。(事实证明，看懂了default.prop的生成过程，build.prop的生成代码不攻自破，大同小异。)

##先看看default.prop的生成代码
代码我加了注释，分成两部分:先是变量定义与赋值，然后是真正的写入动作。
我们关心写文件操作，逐行分析。

####第一句：
{% highlight Makefile%}
@echo Target buildinfo: $@ 
{% endhighlight %}

这句代码输出一句信息,信息中: Target buildinfo原封不动，$@会被替换成目标文件的名字。在这里呢，目标文件的名字就是由
{% highlight Makefile%}
INSTALLED_DEFAULT_PROP_TARGET := $(TARGET_ROOT_OUT)/default.prop  
{% endhighlight %}
来确定的，即目录$(TARGET_ROOT_OUT)下的default.prop文件。 **$@**符号是Makefile中常见的变量，用来指代本次MAKE的目标。算是一个内置的变量名(关键字)。

####第二句：
{% highlight Makefile %}
@mkdir -p $(dir $@)
{% endhighlight %}

这是调用 mkdir 命令来为default.prop创建目录，如果不存在的话。其中 mkdir 与 echo
一样，是 bash 命令，而 dir 命令是Make系统提供的命令。假如“$@”的真正内容是
>$A20\_Src/out/target/product/sugar-xbh\_fjb/root/default.prop

那么$(dir $@)取得内容就应该是：
>$A20\_Src/out/target/product/sugar-xbh\_fjb/root

####第三句
这一句比较长，但非常简单，重点在重定向符号 “>” 和 “>>”:
{% highlight Makefile %}
    $(hide) echo "#" > $@; \
            echo "# ADDITIONAL_DEFAULT_PROPERTIES" >> $@; \
            echo "#" >> $@;
{% endhighlight %}

其中，
$(hide)变量无具体影响，意思是以下命令悄悄的执行，不在屏幕回显了。类似上面echo 和 mkdir 命令前面的@符号。DOS的批处理中也有类似的用法。

{% highlight Bash %}
echo "#" > $@ 
{% endhighlight %}

这一句与上面的
{% highlight Bash %}
echo Target buildinfo: $@ 
{% endhighlight %}
的区别在于，多了一个
">"。这是bash命令中常见的重定向符号，即把左边的输出，写到右边(通常是个文件)去。这里表示把"#"写进了
$@。即目标文件，xxx/xxx/default.prop.
结合对default.prop文件的观察，这句话的意思显然是代码未动，注释先行。非常好的linux风格。 

下面的 “>>” 经测试，是"append"的意思，类似c语言中的fopen("file","w+")函数中的"w+"模式。如果继续使用 “>”,则会将上一行写入的“#”号给覆盖掉。

####第四句
直接跳到下一个$(hide)：
{% highlight Makefile%}
$(hide) $(foreach line,$(ADDITIONAL_DEFAULT_PROPERTIES), \
        echo "$(line)" >> $@;)
{% endhighlight %}

结合上面对">>"的解释，可以看出这句是继续往
"$@"中写内容。到底写了什么呢？

使用过 foreach 函数(如PHP或者C#或者python中的for x in y)的人，很容易看出来，这是将变量
$(ADDITIONAL\_DEFAULT\_PROPERTIES)中的内容逐行读出，然后依次写入到
"$@"。更准确的说，是“追加”到原有内容后面。

foreach的语法与for类似,区别在于提供智能递增与智能取值功能，通常用来遍历。for 通常用整型变量来自增来控制循环次数，如：
{% highlight C%}
for (size_t i = 0; i < count; ++i)
{
    /* code */
}
{% endhighlight%}

foreach则无需指定自增变量，可以自动识别变量本身的**类型**与**长度**，并
依次取出每一个内容，赋给指定变量。在这里，即将变量$(ADDITIONAL\_DEFAULT\_PROPERTIES)
中的内容，以行为单位自动递增，同时依次取出赋给变量 "line"，然后下面
引用该变量，$(line), 结合重定向符号“>>”,将line的内容追加到$@。

####第五句
这句调用了一个python脚本,入参为前面一直在写入的 "$@":
{% highlight bash%}
build/tools/post_process_props.py $@
{% endhighlight %}

从名字可以看出，这是对prop文件的事后处理(post
        process)。是对上面重定向操作的补充。应该也是因为python在处理文本方面的巨大优势吧，写Makefile人的实在受不了了，只好祭出大杀器。

打开该python脚本，发现内容如下
{% highlight Python%}
def main(argv):
  filename = argv[1]
  f = open(filename)
  lines = f.readlines()
  f.close()

  properties = PropFile(lines)
  if filename.endswith("/build.prop"):
    mangle_build_prop(properties)
  elif filename.endswith("/default.prop"):
    mangle_default_prop(properties)     #这句是针对default.prop的操作
  else:
    sys.stderr.write("bad command line: " + str(argv) + "\n")
    sys.exit(1)

  f = open(filename, 'w+')  #熟悉的"w+"，将内容追加到default.prop后面
  properties.write(f)
  f.close()



def mangle_default_prop(prop):
  # If ro.debuggable is 1, then enable adb on USB by default
  # (this is for userdebug builds)
  if prop.get("ro.debuggable") == "1":
    val = prop.get("persist.sys.usb.config")
    if val == "":
      val = "adb"
    else:
      val = val + ",adb"
    prop.put("persist.sys.usb.config", val)
  # UsbDeviceManager expects a value here.  If it doesn't get it, it will
  # default to "adb". That might not the right policy there, but it's better
  # to be explicit.
  if not prop.get("persist.sys.usb.config"):
    prop.put("persist.sys.usb.config", "none");
{% endhighlight%}

结合代码中加的两句中文注释，可以看出，该脚本是根据 "ro.debuggable"的值，来对"persist.sys.usb.config"进行处理。具体含义属于USB模块，不做探究。

## 现在转到build.prop

### 生成build.prop的代码
经过一路泥泞，分析了default.prop的生成，终于可以回到正题，关心build.prop了。Makefile中关于生成build.prop的代码，关键部分如下：

{% highlight Makefile%}
BUILDINFO_SH := build/tools/buildinfo.sh
$(INSTALLED_BUILD_PROP_TARGET): $(BUILDINFO_SH) $(INTERNAL_BUILD_ID_MAKEFILE) $(BUILD_SYSTEM)/version_defaults.mk $(wildcard $(TARGET_DEVICE_DIR)/system.prop)
    @echo Target buildinfo: $@
    @mkdir -p $(dir $@)
    $(hide) TARGET_BUILD_TYPE="$(TARGET_BUILD_VARIANT)" \

            ...
            
            TARGET_AAPT_CHARACTERISTICS="$(TARGET_AAPT_CHARACTERISTICS)" \
            bash $(BUILDINFO_SH) > $@
    $(hide) if [ -f $(TARGET_DEVICE_DIR)/system.prop ]; then \
              cat $(TARGET_DEVICE_DIR)/system.prop >> $@; \
            fi
    $(if $(ADDITIONAL_BUILD_PROPERTIES), \
        $(hide) echo >> $@; \
                echo "#" >> $@; \
                echo "# ADDITIONAL_BUILD_PROPERTIES" >> $@; \
                echo "#" >> $@; )
    $(hide) $(foreach line,$(ADDITIONAL_BUILD_PROPERTIES), \
        echo "$(line)" >> $@;)
    $(hide) build/tools/post_process_props.py $@

{% endhighlight %}

可以看到，往build.prop文件写入的包括四部分：

* 调用buildinfo.sh脚本，往"$@"写入。
* 将system.prop中的内容，调用cat命令，往"$@"写入。
* 从ADDITIONAL\_BUILD\_PROPERTIES变量中读取内容，往"$@"写入。
* 调用post\_process\_props.py脚本，往"$@"写入。

但其中并没有发现 PRODUCT\_PROPERTY\_OVERRIDES 这个变量的身影。

###哪里包含了PRODUCT\_PROPERTY\_OVERRIDES？
由于.mk文件也可以像C语言的.h文件一样被包含,所以推测PRODUCT\_PROPERTY\_OVERRIDES变量的内容，在别的文件里被读取了。

与Makefile同级有相当多的.mk文件，不如就在这里搜索吧：
{% highlight bash %}
grep -rn "PRODUCT_PROPERTY_OVERRIDES" .
{% endhighlight %}

很幸运，找到了这个文件：
>$A20\_SRC/android/build/core/product\_config.mk

其中包含PRODUCT\_PROPERTY\_OVERRIDES的部分为：
{% highlight Makefile%}
# Add the product-defined properties to the build properties.
ADDITIONAL_BUILD_PROPERTIES := \
    $(ADDITIONAL_BUILD_PROPERTIES) \
    $(PRODUCT_PROPERTY_OVERRIDES)
{% endhighlight%}

可以看到，PRODUCT\_PROPERTY\_OVERRIDES这个变量的值，被赋给ADDITIONAL\_DEFAULT\_PROPERTIES。而后者则正是往build.prop写入的四部分中的第三个。

至此搞清楚了在sugar\_xbh\_fjb.mk中定义的变量值，是如何被写入到build.prop文件中。

仍然需要注意的
----------------
在测试过程中，发现当改变sugar\_xbh\_fjb.mk中的PRODUCT\_PROPERTY\_OVERRIDES的值后，再次编译前，需要手动将build.prop文件删除掉，否则不会更新。证据就是build.prop文件中的
ro.build.date不会改变。

一点技巧
-----------------
由于之前也没有真正使用过Makefile，对其语法及规则不甚了了。但这次发现，虽然语法看起来佶屈聱牙,晦涩难懂，却相当好运行。
为了弄明白上面提到的代码是干什么的，我直接把其复制出来，新建一个"Makefile",然后直接运行make命令。竟然"基本"可以执行。——“基本”指的是，改掉一些路径就可以了。比如将
{% highlight Makefile%}
INSTALLED_BUILD_PROP_TARGET := $(TARGET_OUT)/build.prop
{% endhighlight%}
改为：
{% highlight Makefile%}
INSTALLED_BUILD_PROP_TARGET := build.prop
{% endhighlight%}
就强行将生成的build.prop指定到与新建的Makefile同级目录。

未尽事宜
--------------------
还有链条没有完全显现，如:

* product\_config.mk文件是如何被包进到Makefile中去的？
* 文件中各变量的具体含义？
* Makefile中，冒号的作用？
{% highlight Makefile%}
$(INSTALLED_BUILD_PROP_TARGET): $(BUILDINFO_SH) $(INTERNAL_BUILD_ID_MAKEFILE) $(BUILD_SYSTEM)/version_defaults.mk $(wildcard $(TARGET_DEVICE_DIR)/system.prop)
{% endhighlight%}


随后有需要的话，再研究补上。

##简要概括
记的这么长,是因为自己对Makefile非常不熟悉。对于熟悉的人，可能需要是更简明的概述。
build.prop文件的生成过程：

1. 通过Makefile来生成
2. 写入的内容来自于四个部分，手段各不相同
    * 通过脚本buildinfo.sh脚本写入
    * 通过cat命令，从system.prop里读取
    * 通过echo命令，从变量PRODUCT\_PROPERTY\_OVERRIDES里读取
    * 通过脚本post\_process\_props.py写入
