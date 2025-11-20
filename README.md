# image-captcha-generator
批量生成验证码图片

## 简介
一个基于 captcha 与 Pillow 的批量生成验证码图片的 Python 小工具

很多时候因为项目很小，我们并不需要一个真正实时生成验证码的模块，只要提前准备验证码图片就可以了。

## 用法

1. 拉取项目 `git clone https://github.com/tjsky/image-captcha-generator.git`
2. 进入项目 `cd image-captcha-generator`
3. 根据需求修改`media_bot.py`文件配置区域内参数
4. 执行 `python media_bot.py`
5. 查看 `imgs` 文件夹会出现本次生成的验证码图片

## 参数

```python
    "batch_size": 100, # 验证码生成数量
    "char_length": 5, # 验证码长度（5位）
    "width": 160, # 验证码图片宽度
    "height": 60, # 验证码图片高度
    "charset": "23456789ABCDEFGHJKLMNPQRSTUVWXYZ", # 验证码使用字符集，留空使用去混淆字符集（没有数字1、字母l、I之类的字符）
    "font_paths": ["C:/Windows/Fonts/comic.ttf", "C:/Windows/Fonts/CHILLER.ttf"],  # 验证码使用自定义字体路径，留空使用系统默认字体, 建议找一些手写，行书，隶书字体，避免使用系统自带字体
    "output_dir": "imgs", # 验证码图片保存位置
    "enable_interference": True, #是否开启下方高级干扰措施。以下全部为范围（最小值, 最大值）
    # 噪点：取值范围 (0.0 ~ 1.0) 【建议：(0.2, 0.5) 】越大越难识别，不建议大于0.8
    "noise_range": (0.2, 0.3),  
    # 高斯模糊：取值范围(0.0, 2.0)【建议：(0.5, 1.5) 】越大越难识别，不建议大于2.0
    "blur_range": (0.8, 1.2),  
    # 对比度：取值范围(0.0, 1.0)【建议：(0.5, 0.9) 】 越小越难识别，不建议小于0.4
    "contrast_range": (0.8, 0.9)
```
