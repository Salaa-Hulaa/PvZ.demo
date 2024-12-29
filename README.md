# Plants vs. Zombies Clone

这是一个使用 Python 和 Pygame 开发的植物大战僵尸克隆版游戏。游戏保留了原版的核心玩法，同时加入了一些新的特性。

## 游戏特性

- 经典的植物大战僵尸游戏玩法
- 流畅的游戏动画和音效
- 多种植物和僵尸类型
- 阳光收集系统
- 生命值显示系统
- 游戏暂停功能
- 自定义游戏图标
- 
## 游戏未实现必要内容

- 植物卡的CD
- 小铲子
- 推车
- 参数设置面板（现在在setting.py中，封装成exe以后没有）

  
## 安装说明

### 运行已打包版本

1. 下载最新的发布版本
2. 解压缩文件
3. 运行 `Plants vs Zombies.exe`

### 从源码运行
（非常抱歉，我手滑把整个项目传上来了，所以只用git然后激活环境）

1. 确保已安装 Python 3.8 或更高版本（bushi）
2. 克隆此仓库
3. 创建并激活虚拟环境：
   ```bash
   python -m venv venv ##不用，因为我已经有一个环境大礼包了
   venv\Scripts\activate
   ```
4. 安装依赖：
   ```bash
   pip install -r requirements.txt ##不用，在lib里了
   ```
5. 运行游戏：
   ```bash
   python main.py
   ```
## 游戏页面

### 启动页
![图片](https://github.com/user-attachments/assets/59b31bac-33eb-4c4a-9b0e-ff4e25aed6fc)

### 游戏页
![图片](https://github.com/user-attachments/assets/229bfcae-8450-44f2-b31f-afd417fa64f0)
![图片](https://github.com/user-attachments/assets/0b7ac487-a36b-43cd-8f40-56d54cc79df2)


## 游戏控制

- 鼠标左键：选择和放置植物
- ESC：暂停游戏
- 数字键 1-5：选择不同的植物
- M：切换音乐开关
- S：切换音效开关

## 开发环境

- Python 3.12.6
- Pygame 2.6.1
- Numpy 2.2.1
- Pillow 11.0.0

## 项目结构

```
pVz/
├── main.py              # 游戏入口
├── game.py             # 游戏主逻辑
├── settings.py         # 游戏配置
├── sound_manager.py    # 音效管理
├── sprites/            # 游戏精灵
│   ├── plant.py       # 植物基类
│   ├── sunflower.py   # 向日葵
│   ├── peashooter.py  # 豌豆射手
│   ├── zombie.py      # 僵尸
│   └── bullet.py      # 子弹
├── sounds/            # 音效文件
├── images/            # 图片资源
└── build.py          # 打包脚本
```

## 开发指南

### 游戏设置

游戏的主要设置都在 `settings.py` 文件中，你可以修改以下参数：

1. 屏幕设置
```python
SCREEN_WIDTH = 800  # 游戏窗口宽度
SCREEN_HEIGHT = 600  # 游戏窗口高度
FPS = 60  # 游戏帧率
```

2. 游戏参数
```python
SUNLIGHT_SPEED = 2  # 阳光下落速度
ZOMBIE_SPAWN_RATE = 0.005  # 僵尸生成概率
STARTING_SUNLIGHT = 50  # 初始阳光数量
```

3. 植物属性
```python
PLANT_COSTS = {
    'sunflower': 50,
    'peashooter': 100,
    # 添加新植物的成本
}

PLANT_HEALTH = {
    'sunflower': 100,
    'peashooter': 100,
    # 添加新植物的生命值
}
```

### 添加新植物

1. 在 `sprites` 目录下创建新的植物类文件（例如 `wallnut.py`）
2. 继承 `plant.py` 中的基类：
```python
from .plant import Plant

class WallNut(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 200  # 更高的生命值
        self.cost = 50
        self.name = 'wallnut'
        self.load_images()  # 加载图片
        
    def load_images(self):
        # 加载植物图片
        self.images = []  # 添加动画帧
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        # 实现植物的特殊行为
        super().update()
```

3. 在 `settings.py` 中添加新植物的配置
4. 在 `game.py` 中注册新植物

### 添加新僵尸

1. 在 `sprites` 目录下创建新的僵尸类文件（例如 `cone_zombie.py`）
2. 继承 `zombie.py` 中的基类：
```python
from .zombie import Zombie

class ConeZombie(Zombie):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 200  # 更高的生命值
        self.damage = 20  # 更高的攻击力
        self.speed = 1  # 移动速度
        self.name = 'cone_zombie'
        self.load_images()
        
    def load_images(self):
        # 加载僵尸图片
        self.images = []  # 添加动画帧
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        # 实现僵尸的特殊行为
        super().update()
```

3. 在 `settings.py` 中添加新僵尸的配置
4. 在 `game.py` 中添加新僵尸的生成逻辑

### 添加新音效

1. 将新的音效文件（.wav 格式）放入 `sounds` 目录
2. 在 `sound_manager.py` 中注册新音效：
```python
sound_files = {
    'new_sound': 'new_sound.wav',
    # 其他音效
}
```


```

## 构建说明

要构建独立的可执行文件：

```bash
python build.py
```

生成的可执行文件将在 `dist` 目录中。



## 贡献

欢迎提交fork

## 许可

还没选
