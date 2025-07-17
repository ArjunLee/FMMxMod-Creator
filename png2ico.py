# 使用Python脚本转换图标
from PIL import Image

img = Image.open('app/Resources/FMMxModCreator_Icon_512.png')
img.save('app/Resources/FMMxModCreator_Icon.ico', format='ICO', sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)])