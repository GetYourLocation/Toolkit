# Tools

Tools for processing training/testing data.

## 数据格式

`data` 目录下的每个目录表示一个数据集，每个数据集包含如下几个文件：

```
data/
  some-data-set/
    frames      // 帧图片目录
    pos.csv     // 录制时站立位置
    sensor.csv  // 每一帧的传感器数据
```

## 工具包

### 提取数据集中的部分数据

用法:

```
python3 select_frames.py <数据集目录名> <起始帧序号> <结束帧序号>
```

示例:

```
# 提取shops数据集的第2、3帧以及对应的传感器数据
python3 select_frames.py shops 2 3
```

运行成功后将生成 `shops-selected` 目录，包含如下几个文件：

```
data/
  shops-selected/
    frames      // 帧图片目录
    pos.csv     // 录制时站立位置
    sensor.csv  // 每一帧的传感器数据
    config.txt  // 配置文件，存放数据集中帧的个数
```

`frames` 和 `config.txt` 可以作为[视频跟踪算法](https://github.com/GetYourLocation/KCFcpp)的输入。

## License

See the [LICENSE](./LICENSE) file for license rights and limitations.
