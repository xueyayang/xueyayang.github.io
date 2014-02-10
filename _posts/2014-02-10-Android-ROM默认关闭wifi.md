---
layout: default
---

Android-ROM默认关闭WIFI
========================

1 问题
====
定制ROM，希望开机时，WIFI默认是关闭的。

2 方法
====
修改文件
>frameworks/base/packages/SettingsProvider/src/com/android/providers/settings/DatabaseHelper.java

的如下代码：

```java
public void checkAndStartWifi() {  
    mAirplaneModeOn.set(isAirplaneModeOn());  
    mPersistWifiState.set(getPersistedWifiState());  
    /* Start if Wi-Fi should be enabled or the saved state indicates Wi-Fi was on */  
    boolean wifiEnabled = shouldWifiBeEnabled() || testAndClearWifiSavedState();  
	//Added by Eric. Force to cloese \{\{--------------
	wifiEnabled = false;
	//Added by Eric end.---------------\}\}
    Slog.i(TAG, "WifiService starting up with Wi-Fi " +  
            (wifiEnabled ? "enabled" : "disabled"));  
    setWifiEnabled(wifiEnabled); //强制设置为true  
  
    mWifiWatchdogStateMachine = WifiWatchdogStateMachine.  
           makeWifiWatchdogStateMachine(mContext);  
  
}  
```

3 结论
====
1. WIFI的打开与关闭，虽然也在设置里，但是不能简单地通过[修改SettingsProvider的默认值][1]
来实现。

2. 关于WIFI模块更深入的了解，可以参考这篇博客:[Android WiFi--系统架构][2]。


[1]: http://xueyayang.github.io/2014/01/26/ROM%E5%85%81%E8%AE%B8%E5%AE%89%E8%A3%85%E6%9C%AA%E7%9F%A5%E6%BA%90%E7%A8%8B%E5%BA%8F.html
[2]: http://blog.csdn.net/myarrow/article/details/8129607
