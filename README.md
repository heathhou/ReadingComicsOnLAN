# 局域网漫画阅读器

这是一个简单的Web应用程序，允许您可以使用手机通过浏览器阅读存储在局域网内的电脑上的漫画（按序排好的图片格式的漫画）。

## 功能

- **文件浏览器**: 浏览您的漫画文件夹。
- **两种阅读模式**:
  - **垂直阅读**: 所有图片在单个页面上垂直排列，适合滚动阅读。
  - **水平阅读**: 一次显示一张图片，可通过点击、键盘方向键或在触摸屏上滑动来翻页。
- **子文件夹支持**: 可选是否在阅读时加载子文件夹中的图片。
- **响应式设计**: 在桌面和移动设备上均可使用。
- **进度条设置**：可以点击进度条来调整进度，也可以点击页数直接进行输入更改当前页数

## 如何使用

### 1. 准备工作

- 您的电脑上需要安装 [Python](https://www.python.org/downloads/)。
- 您的漫画文件（JPG, PNG, GIF, WebP等格式）需要存放在文件夹中。

### 2. 安装

a. 打开您电脑的终端（命令提示符或PowerShell）。

b. 克隆或下载此项目到您的电脑上。

c. 进入项目目录:
   ```bash
   cd path/to/ReadingComicsOnLAN
   ```

d. 安装所需的Python包:
   ```bash
   pip install -r requirements.txt
   ```

### 3. 放入漫画

找到你的漫画所在的文件夹，没有什么严格要求的格式。

例如:
```
ReadingComicsOnLAN/
    ├── 我的第一部漫画/
    │   ├── 01.jpg
    │   ├── 02.jpg
    │   └── ...
    └── 另一部漫画/
       ├── 第1章/
       │   ├── 001.png
       │   └── 002.png
       └── 第2章/
           └── ...
```

### 4. 运行服务器

在项目根目录下，运行以下命令:
```shell
python app.py
```
服务器会从当前文件夹（运行命令的位置）加载漫画。

**指定自定义漫画目录:**

如果您想使用其他位置的漫画文件夹，可以使用 `--path` 参数来指定路径。

例如:
```bash
# Windows
python app.py --path "D:\我的漫画"

# macOS / Linux
python app.py --path "/home/user/comics"
```

服务器启动后，您会看到类似以下的输出，其中会显示正在服务的漫画目录:
```
Serving comics from: D:\我的漫画
 * Serving Flask app 'app'
 * Debug mode: on
Serving comics from: D:\我的漫画
```

或：

```shell
Serving comics from: D:\我的漫画
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.7:5000
Press CTRL+C to quit
 * Restarting with stat
Serving comics from: D:\我的漫画
 * Debugger is active!
```

**默认不打印请求日志，如果需要打印请求日志，需要增加一个参数**：

```shell
python app.py --request-log
```

**对于Windows平台，已经打包好了一个exe文件，直接双击就可以运行**,等同于在当前目录运行命令：

```shell
python app.py
```

也可以在终端加参数：

```cmd
ReadingComicsOnLAN.exe --path D:\comic --request-log
```



### 5. 开始阅读

a. **在您的电脑上**: 打开浏览器并访问 `http://localhost:5000` 或 `http://127.0.0.1:5000`。

b. **在手机或同一局域网的其他设备上**:
   - 首先，获取您电脑的局域网IP地址。
     - **Windows**: 在终端中运行 `ipconfig`，查找"IPv4 地址"。
     - **macOS/Linux**: 在终端中运行 `ifconfig` 或 `ip a`，查找 `inet` 地址。
   - 假设您电脑的IP地址是 `192.168.1.100`，那么就在手机的浏览器中访问 `http://192.168.1.100:5000`。

c. **浏览和阅读**:
   - 点击文件夹可以进入。
   - 点击文件夹下方的"垂直阅读"或"水平阅读"按钮开始看漫画。
   - 在主页右上角勾选"加载子文件夹内容"，可以在阅读时一并加载所有子文件夹里的图片。
     - 关闭状态：只能查看直接在当前文件夹里面的图片。
     - 开启状态：查看完直接在当前文件夹里面的图片后，自动加载当前文件夹的子文件夹里的图片。


## 注意

- 请确保运行此应用的电脑和您的阅读设备（手机、平板）连接到同一个Wi-Fi或局域网中。
- 如果无法访问，请检查电脑的防火墙设置，确保端口 `5000` 是开放的。
- 此项目仅为本地使用设计，请勿将其暴露在公共互联网上。 