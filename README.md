[VTB]: http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html
[KCF]: https://github.com/GetYourLocation/KCFcpp
[blog_make_train]: http://blog.csdn.net/sinat_30071459/article/details/50723212

# Toolkit

处理数据集的工具包。

<!-- MarkdownTOC -->

- [数据格式说明](#数据格式说明)
- [工具包](#工具包)
    - [提取子集](#提取子集)
    - [制作训练集](#制作训练集)
    - [统一帧图片名](#统一帧图片名)
- [License](#license)

<!-- /MarkdownTOC -->

<a name="数据格式说明"></a>
## 数据格式说明

`data` 目录下的每个目录表示一个数据集，每个数据集包含如下几个文件：

```
data/
  some-data-set/
    JPEGImages  // 帧图片目录
    pos.csv     // 录制时站立位置
    sensor.csv  // 每一帧的传感器数据
```

<a name="工具包"></a>
## 工具包

<a name="提取子集"></a>
### 提取子集

一个店铺招牌很可能只会在数据集（帧序列）中的一个子集（一小段）出现，为了完成对该店铺标签的训练我们需要把这个子集单独提取出来，这可以用以下脚本完成：

```
python3 subset.py <数据集目录名> <起始帧序号> <结束帧序号> <分类标签名>
```

示例:

```
# 提取shops数据集的第2、3帧以及对应的传感器数据
python3 subset.py shops 2 3 shop
```

运行成功后将生成 `shops-subset` 目录，包含如下几个文件：

```
data/
  shops-subset/
    JPEGImages  // 帧图片目录（子集）
    pos.csv     // 录制时站立位置，与原数据集一致
    sensor.csv  // 每一帧的传感器数据（子集）
    config.txt  // 配置文件，存放数据集中帧的个数以及分类标签名
```

<a name="制作训练集"></a>
### 制作训练集

假设我们想在数据集 human 的基础上生成训练集，这个数据集至少需要包含如下目录及文件：

```
data/
  human/
    JPEGImages  // 帧图片目录
    config.txt  // KCF 配置文件
```

脚本用法如下：

```bash
$ python3 make_train.py <数据集目录名> <作者名> [-s]
```

该脚本首先用 [KCF][KCF] 对每一帧进行标注，接着按照[此博客][blog_make_train]的方式生成符合 VOC 2007 规范的数据集。最后一个参数 `-s` 为可选参数，如果加上此参数，那么在运行 KCF 时每帧的标注结果将会以图片的方式显示出来。

示例：

```bash
$ python3 make_train.py human GYL -s
```

运行结束后，目录 `JPEGImages` 下所有帧图片的文件名会加上 “作者名_时间戳_” 的前缀，并且会生成一个 `Annotations` 文件夹，里面存放着每一张图片对应的 XML 文件。

<a name="统一帧图片名"></a>
### 统一帧图片名

如果帧图像的名字是这种形式：“0001.jpg”，“02.jpg” 或 “0100.jpg” （比如来自 [Visual Tracker Benchmark][VTB] 的数据集）, 可以用以下命令将图片名统一成 “1.jpg”，“2.jpg” 和 “100.jpg”：

```
$ python3 norm.py <数据集目录名>
```

<a name="license"></a>
## License

See the [LICENSE](./LICENSE) file for license rights and limitations.
