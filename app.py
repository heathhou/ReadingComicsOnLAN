import os
import argparse
import sys
import re
import logging
from flask import Flask, jsonify, render_template, request, send_from_directory

# --- 用户配置 ---
# 在这里修改默认的漫画目录路径。
# 您可以使用绝对路径 (例如 "E:/Comics") 或相对路径 (例如 "comics")。
# 命令行通过 --path 参数指定的路径会覆盖此设置。
# 
# python app.py
# python app.py --request-log
# python app.py --path E:\comic2
# DEFAULT_COMICS_PATH = r"comics"
DEFAULT_COMICS_PATH = r"."

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description='一个简单的局域网漫画阅读器。')
parser.add_argument('--path', type=str, default=None,
                    help=f'您的漫画目录的路径。覆盖脚本中设置的默认路径（当前默认路径："{DEFAULT_COMICS_PATH}"）')
parser.add_argument('--request-log', action='store_true', help='打开终端的Flask请求日志（默认为关闭）。')
args = parser.parse_args()

# 根据参数显式设置 Werkzeug 的日志级别
log = logging.getLogger('werkzeug')
if not args.request_log:
    log.setLevel(logging.ERROR)
else:
    log.setLevel(logging.INFO)


app = Flask(__name__)

# --- Path Configuration ---
# 决定最终的漫画根目录
# 优先使用命令行参数，其次使用代码中定义的路径
final_path = args.path if args.path is not None else DEFAULT_COMICS_PATH
COMICS_ROOT = os.path.abspath(final_path)

# 检查路径是否存在
if not os.path.isdir(COMICS_ROOT):
    # 仅当路径是 'comics' (原始默认值) 且不存在时，才自动创建
    if final_path == "comics":
        print(f"Default comics directory not found. Creating it at: {COMICS_ROOT}")
        os.makedirs(COMICS_ROOT)
    else:
        print(f"Error: The specified comics directory does not exist: {COMICS_ROOT}", file=sys.stderr)
        sys.exit(1)

print(f"Serving comics from: {COMICS_ROOT}")

# Natural sort helper
def natural_sort_key(s):
    """A key for natural sorting. e.g. 'item10' comes after 'item2'"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def get_folder_contents(folder_path):
    """获取指定文件夹的内容，区分文件夹和图片文件"""
    items = sorted(os.listdir(folder_path), key=natural_sort_key)
    folders = []
    images = []
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    for item in items:
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            folders.append(item)
        elif os.path.splitext(item)[1].lower() in supported_formats:
            images.append(item)
    return folders, images

@app.route('/')
def index():
    """主页，显示根目录下的内容"""
    return render_template('index.html')

@app.route('/api/list')
def list_files():
    """API接口，列出指定子目录的内容"""
    relative_path = request.args.get('path', '')
    
    # 安全性检查，防止路径遍历攻击
    if '..' in relative_path or relative_path.startswith('/'):
        return jsonify({"error": "Invalid path"}), 400

    current_path = os.path.join(COMICS_ROOT, relative_path)

    if not os.path.exists(current_path) or not os.path.isdir(current_path):
        return jsonify({"error": "Directory not found"}), 404

    folders, images = get_folder_contents(current_path)
    
    return jsonify({
        "path": relative_path,
        "folders": folders,
        "images": images
    })

@app.route('/reader')
def reader():
    """渲染阅读器页面"""
    return render_template('reader.html')

@app.route('/api/images')
def get_images():
    """API接口，获取指定路径下的所有图片"""
    relative_path = request.args.get('path', '')
    include_subfolders = request.args.get('subfolders', 'false').lower() == 'true'

    # 安全性检查
    if '..' in relative_path or relative_path.startswith('/'):
        return jsonify({"error": "Invalid path"}), 400

    folder_path = os.path.join(COMICS_ROOT, relative_path)

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return jsonify({"error": "Directory not found"}), 404

    image_files = []
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

    if include_subfolders:
        for root, _, files in os.walk(folder_path):
            for file in sorted(files, key=natural_sort_key):
                if os.path.splitext(file)[1].lower() in supported_formats:
                    # 构建相对于COMICS_ROOT的路径
                    full_path = os.path.join(root, file)
                    image_path = os.path.relpath(full_path, COMICS_ROOT)
                    image_files.append(image_path.replace('\\', '/'))
    else:
        for item in sorted(os.listdir(folder_path), key=natural_sort_key):
            if os.path.isfile(os.path.join(folder_path, item)) and os.path.splitext(item)[1].lower() in supported_formats:
                image_files.append(os.path.join(relative_path, item).replace('\\', '/'))

    return jsonify(image_files)

@app.route('/comics/<path:filepath>')
def serve_comic_file(filepath):
    """提供漫画图片文件"""
    return send_from_directory(COMICS_ROOT, filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
