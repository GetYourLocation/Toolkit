# Toolkit

处理数据集的工具包。

<!-- MarkdownTOC -->

- [数据格式说明](#数据格式说明)
- [工具包](#工具包)
    - [提取子集](#提取子集)
    - [统一帧图片名](#统一帧图片名)
- [License](#license)

<!-- /MarkdownTOC -->

<a name="数据格式说明"></a>
## 数据格式说明

`data` 目录下的每个目录表示一个数据集，每个数据集包含如下几个文件：

```
data/
  some-data-set/
    frames      // 帧图片目录
    pos.csv     // 录制时站立位置
    sensor.csv  // 每一帧的传感器数据
```

<a name="工具包"></a>
## 工具包

<a name="提取子集"></a>
### 提取子集

用法:

```
python subset.py <数据集目录名> <起始帧序号> <结束帧序号> <分类标签名>
```

示例:

```
# 提取shops数据集的第2、3帧以及对应的传感器数据
python subset.py shops 2 3 shop
```

运行成功后将生成 `shops-subset` 目录，包含如下几个文件：

```
data/
  shops-subset/
    frames      // 帧图片目录（子集）
    pos.csv     // 录制时站立位置，与原数据集一致
    sensor.csv  // 每一帧的传感器数据（子集）
    config.txt  // 配置文件，存放数据集中帧的个数以及分类标签名
```

`frames` 和 `config.txt` 可以作为 [KCF][KCF] 的输入。

<a name="统一帧图片名"></a>
### 统一帧图片名

如果帧图像的名字是这种形式：“0001.jpg”，“02.jpg” 或 “0100.jpg” （比如来自 [Visual Tracker Benchmark][VTB] 的数据集）, 可以用以下命令将图片名统一成 “1.jpg”，“2.jpg” 和 “100.jpg”，作为 [KCF][KCF] 的输入。

```
$ python norm.py <数据集目录名>
```

<a name="license"></a>
## License

See the [LICENSE](./LICENSE) file for license rights and limitations.

[VTB]: http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html
[KCF]: https://github.com/GetYourLocation/KCFcpp