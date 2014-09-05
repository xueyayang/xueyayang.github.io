---
layout: default
tag: grub2, linux, system, 
---

修复Grub2找回Fedora20
=====================


1 问题
====

机子是双系统，Win7 + Fedora。重装Win7后，无法启动Fedora。


2 方法
====

2.1 准备LiveUSB
----------
我手头只有一个Fedora17的iso，够用。下载[Universal USB
Installer][1]，制作一个U盘启动盘。(UUI真的很好用)。


2.2 查看分区
----------

切换到root，使用`fdisk -l`命令查看分区情况:

{% highlight bash %}
[root@localhost liveuser]# fdisk -l

Disk /dev/sda: 69.8 GB, 69793218560 bytes, 136314880 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0xfdcd0a7c

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *          63    32772599    16386268+   7  HPFS/NTFS/exFAT
/dev/sda2        32772600   136311524    51769462+   f  W95 Ext'd (LBA)
/dev/sda5        32772663    57352049    12289693+   7  HPFS/NTFS/exFAT
/dev/sda6        57354240    58378239      512000   83  Linux
/dev/sda7        58380288   136310783    38965248   8e  Linux LVM

Disk /dev/mapper/live-rw: 8589 MB, 8589934592 bytes, 16777216 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk /dev/mapper/live-osimg-min: 8589 MB, 8589934592 bytes, 16777216 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk /dev/mapper/fedora-root: 37.7 GB, 37731958784 bytes, 73695232 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

Disk /dev/mapper/fedora-swap: 2164 MB, 2164260864 bytes, 4227072 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
{% endhighlight %}

2.3 挂载所需分区
-------------
这一步是将硬盘上的系统，挂载正在运行的LiveUSB系统的目录下。
{% highlight bash %}
# root 分区 '/'
mount /dev/mapper/fedora-root /mnt/ 
# boot 分区
mount /dev/sda6 /mnt/boot
# dev 分区
mount --bind /dev /mnt/dev
{% endhighlight %}

2.4 chroot后安装grub2
-----------------

chroot命令的用途：
> `chroots` runs a command with a specified root directory.

> Ordinarily, file name are looked up starting at the root of the 
> directory structure, i.e., '/'. 'chroot' changes the root to the 
> directory NEWROOT (which must exist) and then run COMMAND with
> optional ARGS.

切换到`/mnt`目录下，经过`mount`，现在该目录上实际是原Fedora的根目录：
{% highlight bash %}
chroot /mnt
{% endhighlight %}

然后运行grub2的安装命令。
{% highlight bash %}
grub2-install /dev/sda
grub2-install --recheck /dev/sda
{% endhighlight %}

2.5 没有Win7?
----------
上面一步，如果只找到了Fedora，没有Win7，莫慌。开机从硬盘启动，进入到找回的Fedora，把上面grub2安装命令重新运行一遍即可。

2.6 调整默认
--------
主力系统是Win7的话，调整grub2默认启动项：

###2.6.1  找到win7在grub2的启动项
{% highlight bash %}
cat /boot/grub2/grub.cfg |grep Windows
{% endhighlight %}
输出：
> menuentry "Windows 7 (loader) (on /dev/sda1)" --class windows --class os {

需要的是引号中的字符串。

###2.6.2  设置为默认
{% highlight bash %}
grub2-set-default "Windows 7 (loader) (on /dev/sda1)"
{% endhighlight %}

3 总结
=====
- 通过LiveUSB启动
- 查看、并挂载原Fedora所在分区
- 通过`chroot`，将运行环境切换到原Fedora的根目录。
- 在原Fedora环境下，安装grub2。
- 全文参考了[这篇博客][2]，非常感谢

[1]:  http://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/
[2]:  http://blog.chinaunix.net/uid-12326395-id-3832378.html
