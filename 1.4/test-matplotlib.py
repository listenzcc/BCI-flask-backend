import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties


# 注册字体
font_path = './asset/msyh.ttc'  # 替换为你的字体文件路径
font_prop = fm.FontProperties(fname=font_path)
fm.fontManager.addfont(font_path)  # 注册字体到字体管理器

# 获取字体名称
font_name = font_prop.get_name()

# 配置全局字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = [font_name]
plt.rcParams['axes.unicode_minus'] = False
font = FontProperties(fname='./asset/msyh.ttc', size=14)
# plt.title('中文标题', fontproperties=font)
plt.title('中文标题')  # , fontproperties=font)
plt.show()

# for k, v in plt.rcParams.items():
#     print(k, v)

print(font.get_name())
