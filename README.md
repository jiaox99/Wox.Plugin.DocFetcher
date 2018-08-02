# Wox.Plugin.DocFetcher

从 Wox 中查询 DocFetcher 的插件

## 安装说明

1. 自己安装 [DocFetcher](http://docfetcher.sourceforge.net/de/download.html)
2. 从设置->高级设置手动开启 `PythonApiEnabled` 选项

    打开配置文件，滚动到最下面，修改如下选项
    ```ini
    PythonApiEnabled = true
    ```
3. 在 Wox 中安装本插件

## 使用说明

在 Wox 中输入 `df querystr>` 进行查询

### 特别说明

Wox 是即时查询的，即一边输入一遍就会显示命中的结果

DocFetcher 中单次查询一般是很快的，但如果索引的文件太多，或查询结果太多的，频繁查询 DocFetcher 还是不能承受的

所以需要明确输入一个 `>` 以确认触发查询