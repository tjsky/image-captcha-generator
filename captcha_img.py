import os
import random
import string
from captcha.image import ImageCaptcha
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

# ==========================================
# 配置区域
# ==========================================
USER_CONFIG = {
    "batch_size": 100, # 验证码生成数量
    "char_length": 5, # 验证码长度（5位）
    "width": 160, # 验证码图片宽度
    "height": 60, # 验证码图片高度
    "charset": "23456789ABCDEFGHJKLMNPQRSTUVWXYZ", # 验证码使用字符集，留空使用去混淆字符集（没有数字1、字母l、I之类的字符）
    "font_paths": ["Fonts/comic.ttf", "Fonts/CHILLER.ttf"],  # 验证码使用自定义字体路径，留空使用系统默认字体, 建议找一些手写，行书，隶书字体，避免使用系统自带字体
    "output_dir": "imgs", # 验证码图片保存位置
    "enable_interference": True, #是否开启下方高级干扰措施。以下全部为范围（最小值, 最大值）
    # 噪点：取值范围 (0.0 ~ 1.0) 【建议：(0.2, 0.5) 】越大越难识别，不建议大于0.8
    "noise_range": (0.2, 0.3),  
    # 高斯模糊：取值范围(0.0, 2.0)【建议：(0.5, 1.5) 】越大越难识别，不建议大于2.0
    "blur_range": (0.8, 1.2),  
    # 对比度：取值范围(0.0, 1.0)【建议：(0.5, 0.9) 】 越小越难识别，不建议小于0.4
    "contrast_range": (0.8, 0.9)
}

# 默认值
DEFAULTS = {
    "batch_size": 20,
    "char_length": 5,
    "width": 160,
    "height": 60,
    "charset": "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ",
    "output_dir": "img",
    "noise_range": (0.05, 0.05), 
    "blur_range": (0.5, 0.5),
    "contrast_range": (1.0, 1.0)
}

class RandomCaptchaTool:
    def __init__(self, config=None):
        self.config = config if config else {}
        self._init_settings()
        self._prepare_directory()
        
        valid_fonts = [f for f in self.font_paths if os.path.exists(f)]
        if self.font_paths and not valid_fonts:
            print("[警告] 字体文件未找到，使用默认字体。")
            
        self.image_generator = ImageCaptcha(
            width=self.width, 
            height=self.height,
            fonts=valid_fonts if valid_fonts else None
        )

    def _init_settings(self):
        self.batch_size = self.config.get("batch_size") or DEFAULTS["batch_size"]
        self.char_length = self.config.get("char_length") or DEFAULTS["char_length"]
        self.width = self.config.get("width") or DEFAULTS["width"]
        self.height = self.config.get("height") or DEFAULTS["height"]
        self.charset = self.config.get("charset") or DEFAULTS["charset"]
        self.output_dir = self.config.get("output_dir") or DEFAULTS["output_dir"]
        self.font_paths = self.config.get("font_paths", [])    
        self.enable_interference = self.config.get("enable_interference", False)
        self.noise_range = self.config.get("noise_range") or DEFAULTS["noise_range"]
        self.blur_range = self.config.get("blur_range") or DEFAULTS["blur_range"]
        self.contrast_range = self.config.get("contrast_range") or DEFAULTS["contrast_range"]

    def _prepare_directory(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_random_text(self):
        return ''.join(random.choice(self.charset) for _ in range(self.char_length))

    def _get_random_value(self, config_val):
        if isinstance(config_val, (tuple, list)) and len(config_val) >= 2:
            return random.uniform(config_val[0], config_val[1])
        elif isinstance(config_val, (int, float)):
            return float(config_val)
        return 0.0

    def _apply_dynamic_interference(self, image):
        
        current_noise_rate = self._get_random_value(self.noise_range)
        current_blur_radius = self._get_random_value(self.blur_range)
        current_contrast = self._get_random_value(self.contrast_range)
        
        # 噪点
        if current_noise_rate > 0:
            draw = ImageDraw.Draw(image)
            w, h = image.size
            noise_count = int(w * h * current_noise_rate)
            for _ in range(noise_count):
                xy = (random.randrange(0, w), random.randrange(0, h))
                gray = random.randint(0, 255)
                fill_color = (gray, gray, gray) 
                draw.point(xy, fill=fill_color)

        # 高斯模糊
        if current_blur_radius > 0.1:
            image = image.filter(ImageFilter.GaussianBlur(radius=current_blur_radius))

        # 对比度
        if current_contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(current_contrast)
            
        return image

    def run(self):
        print(f"--- 开始生成随机高防验证码 ---")
        print(f"干扰参数将在以下范围波动:")
        print(f"  - 噪点: {self.noise_range}")
        print(f"  - 模糊: {self.blur_range}")
        print(f"  - 对比度: {self.contrast_range}")
        
        success_count = 0
        
        for i in range(self.batch_size):
            text = self.get_random_text()
            filename = f"image_{text}.png"
            file_path = os.path.join(self.output_dir, filename)
            
            while os.path.exists(file_path):
                text = self.get_random_text()
                filename = f"image_{text}.png"
                file_path = os.path.join(self.output_dir, filename)

            try:
                image = self.image_generator.generate_image(text)
                
                if self.enable_interference:
                    image = self._apply_dynamic_interference(image)
                
                image.save(file_path)
                success_count += 1
            except Exception as e:
                print(f"[错误] {e}")

        print(f"--- 任务完成: 生成了 {success_count} 张验证码图片 ---")
        print(f"目录: {os.path.abspath(self.output_dir)}")

if __name__ == "__main__":
    tool = RandomCaptchaTool(USER_CONFIG)
    tool.run()