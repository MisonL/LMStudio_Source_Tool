from PIL import Image, ImageDraw
import os

# 创建图标目录
if not os.path.exists('icons'):
    os.makedirs('icons')

# 创建一个简单的图标
img = Image.new('RGB', (64, 64), color=(73, 109, 137))
d = ImageDraw.Draw(img)

# 绘制一个简单的图案
d.ellipse([10, 10, 54, 54], fill=(255, 255, 255))
d.ellipse([20, 20, 44, 44], fill=(73, 109, 137))
d.ellipse([25, 25, 39, 39], fill=(255, 255, 255))

# 保存为PNG
img.save('icons/app.png')

# 转换为ICO
img.save('icons/app.ico')

print("图标已创建: icons/app.ico")