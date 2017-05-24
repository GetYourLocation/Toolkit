[VTB]: http://cvlab.hanyang.ac.kr/tracker_benchmark/datasets.html
[KCF]: https://github.com/GetYourLocation/KCFcpp
[blog_make_train]: http://blog.csdn.net/sinat_30071459/article/details/50723212

# Toolkit

处理数据集的工具包。

<!-- MarkdownTOC -->

- [依赖库安装](#依赖库安装)
- [数据格式说明](#数据格式说明)
- [工具包](#工具包)
    - [提取子集](#提取子集)
    - [制作训练集](#制作训练集)
    - [检验训练集](#检验训练集)
    - [重命名帧图片目录](#重命名帧图片目录)
    - [统一帧图片名](#统一帧图片名)
- [License](#license)

<!-- /MarkdownTOC -->

<a name="依赖库安装"></a>
## 依赖库安装

所有脚本均使用 Python 3 运行，使用以下命令安装依赖库：

```
$ pip3 install --user -r requirements.txt
```

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
$ python3 make_train.py <数据集目录名> <作者名> [-t]
```

该脚本首先用 [KCF][KCF] 对每一帧进行标注，接着按照[此博客][blog_make_train]的方式生成符合 VOC 2007 规范的数据集，在使用此脚本之前请先确定数据集目录下的 `config.txt` 是否编写正确。

**注**：脚本的最后一个参数 `-t` 为可选参数，如果加上此参数，那么脚本只会运行 KCF，不会生成 XML 文件，并且会把 KCF 每一帧的计算结果显示在图片上。（建议先加上此参数确定 `config.txt` 的编写是否合理，然后再关掉此参数制作训练集）

示例：

```bash
$ python3 make_train.py human GYL
```

运行结束后，目录 `JPEGImages` 下所有帧图片的文件名会加上 “作者名_时间戳_” 的前缀，并且会生成一个 `Annotations` 文件夹，里面存放着每一张图片对应的 XML 文件。

<a name="检验训练集"></a>
### 检验训练集

训练集生成之后，数据集目录下会产生如下两个目录：

```
data/
  some-data-set/
    Annotations  // XML 文件目录
    JPEGImages   // 帧图片目录
    ...          // 其它文件、目录等
```

为了检查训练集生成是否合理，可以用以下脚本：

```bash
$ python3 draw_box.py <数据集目录名>
```

运行后该脚本会逐一的读取 `Annotations` 中的 XML 文件，然后显示对应的图片并且把 XML 中指定的矩形区域标注在图片上，便于检查矩形区域是否框住了目标物体。每张图片显示之后会暂停，在命令行按下回车键即可显示下一张图片。

<a name="重命名帧图片目录"></a>
### 重命名帧图片目录

Android 端采集到的帧图片目录名是 `frames`，制作训练集时需要将其改名为 `JPEGImages`，使用以下脚本完成：

```bash
$ python3 rename_frames.py <目录名>
```

这里传入的目录中包含若干需要重命名的数据集：

```
some-directory/
  3-xxx-20170516150458/
    frames/
    pos.csv
    sensor.csv
  3-xxx-20170516151147/
    frames/
    pos.csv
    sensor.csv
  ...
```

示例：

```bash
$ python3 rename_frames.py some-directory
```

运行结束后，上述目录结构将变为：

```
some-directory/
  3-xxx-20170516150458/
    JPEGImages/  # 重命名完成
    pos.csv
    sensor.csv
  3-xxx-20170516151147/
    JPEGImages/  # 重命名完成
    pos.csv
    sensor.csv
  ...
```

<a name="统一帧图片名"></a>
### 统一帧图片名

如果帧图像的名字是这种形式：“0001.jpg”，“02.jpg” 或 “0100.jpg” （比如来自 [Visual Tracker Benchmark][VTB] 的数据集）, 可以用以下命令将图片名统一成 “1.jpg”，“2.jpg” 和 “100.jpg”：

```
$ python3 norm.py <数据集目录名>
```

<a name="license"></a>
## License

See the [LICENSE](./LICENSE) file for license rights and limitations.
