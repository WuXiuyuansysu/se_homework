# 个性化食谱生成器 AI Recipe Generator

> 基于自然语言处理与图像生成模型，支持用户根据食材、口味偏好与菜系风格快速生成个性化菜谱，并可自动生成图文并茂的步骤指导、营养分析建议与成品图。

---
&emsp;
&emsp;
&emsp;
## 🔧 开发要求

- Python 3.8+
- 推荐 IDE: VSCode
- 所有操作建议在 `app/` 目录下进行（即将此目录设为项目根目录）
- 所有路径说明均以 `./` 为当前目录标识

---
&emsp;
&emsp;
&emsp;
## 📁 项目结构与文件说明

```text
.
├── app.py                          # 项目主入口，运行即启动服务/测试生成
├── test.py                         # 用于单元测试、接口测试等
│
├── documents/                      # 项目文档目录
│   ├── requirements.txt            # 所有依赖库说明
│   ├── *.png                       # 所有 UML 图（use_case.png, class.png 等）
│   ├── *.md                        # 项目相关报告（测试、建模、说明书等）
│   └── umls_utils/                 # PlantUML 图生成工具脚本
│
├── classes/                        # 所有核心类
│   ├── class_login.py              # 用户认证、注册模块
│   ├── class_recipe.py             # Recipe 类（结构体定义）
│   ├── class_user.py               # 用户类（历史、偏好、收藏）
│   └── RecipeGeneratePipline.py    # 菜谱生成主流程管理类
│
├── utils/                          # 各功能模块函数实现
│   ├── generate_recipe.py          # 文本生成模型生成菜谱步骤
│   ├── generate_dish_image.py      # 根据描述生成成品图片
│   ├── generate_image_description.py # 生成菜肴外观图像描述
│   ├── generate_steps_image.py     # 每一步生成示意图
│   └── nutrition_analysis.py       # 分析营养成分（如有）
│
├── pictures/                       # 所有图像文件输出目录
│   ├── dish_image.png              # 最终生成的菜肴主图
│   └── 1.png, 2.png...             # 每步示意图
│
└── README.md                       # 当前项目说明文件
```
&emsp;
&emsp;
&emsp;
## 🚀 运行方式

### 本地运行主程序

```bash
cd app
python app.py
```
程序会根据示例输入生成菜谱、成品图、步骤图等。

运行测试
```bash
python test.py
```
测试文件内可自定义输入、查看输出格式、验证路径是否正确。

&emsp;
&emsp;
&emsp;
## 🔍 各模块功能详解

### 1. 主入口模块 `app.py`

- 接收前端或 CLI 输入（如 `ingredients`, `cuisine_type`）
- 调用 `RecipeGenerationPipeline` 启动整个生成流程
- 返回完整 `Recipe` 对象，包括所有生成信息与图片路径

---

### 2. 类定义模块（`./classes`）

#### `class_login.py`

- 类 `login`：
  - `authenticate()`：验证用户密码
  - `register()`：新建用户并创建文件夹结构
  - `load_user()`：读取用户数据

#### `class_user.py`

- 类 `User`：
  - 收藏管理：
    - `save_recipe_to_likes()`
    - `load_recipe_from_likes()`
  - 历史记录管理：
    - `save_recipe_to_history()`
    - `load_recipe_from_history()`
  - 偏好分析：
    - `generate_preferences()`
    - `update_preferences_file()`

#### `class_recipe.py`

- 类 `Recipe`：
  - 属性包括：
    - 菜谱名称
    - 步骤图
    - 主图
    - 营养字典
    - UML 图
  - 方法：
    - `to_dict()`：转换为 JSON，便于保存与传输

#### `RecipeGeneratePipline.py`

- 类 `RecipeGenerationPipeline`：
  - `execute()`：整合各步骤生成完整菜谱对象
  - 功能包括：
    - 调用文本生成
    - 图片生成
    - UML 图生成等子模块
  - 最终输出结构良好的 `Recipe` 对象

---

### 3. 工具函数模块（`./utils`）

#### `generate_recipe.py`

- 根据用户输入的原料和菜系风格生成菜谱 JSON 对象（步骤、食材）

#### `generate_image_description.py`

- 提取生成菜肴图像所需的外观描述（如 style、光泽、构图等）

#### `generate_dish_image.py`

- 使用 AI 图像合成模型（如 DALL·E、Stable Diffusion）
- 输入描述字典，输出并保存为 `dish_image.png`

#### `generate_steps_image.py`

- 对每一步制作过程生成示意图
- 图片保存为 `1.png`, `2.png` 等至 `./pictures/`

#### `nutrition_analysis.py`（如启用）

- 对生成的菜谱内容进行营养成分分析（热量、蛋白质、脂肪等）

---

### 4. 图像与输出

- 最终输出包括：
  - 主图：`./pictures/dish_image.png`
  - 步骤图：`./pictures/1.png`, `2.png` 等
- 所有输出路径会在 Flask 返回或 CLI 打印中明确标出


&emsp;
&emsp;
&emsp;
## 🖼️ UML 图与系统建模

### 详见 ./documents/ 下：

    user_case.png：展示用户行为与系统的主要交互流程

    class.png：展示主要类之间的关系（User、Recipe、login等）

    state.png：展示系统生成食谱过程中的状态流转

    sequence.png：展示主流程中模块间的函数调用与数据传递

### 相关建模报告见：

    系统建模报告.md

    软件测试与质量保证报告.md

&emsp;
&emsp;
&emsp;
## 🖼️ UML 图与系统建模

### 🔹 UML 图位置（位于 `./documents/` 目录）：

- `user_case.png`  
  展示用户行为与系统的主要交互流程

- `class.png`  
  展示主要类之间的关系（如 `User`、`Recipe`、`login` 等）

- `state.png`  
  展示系统在生成食谱过程中的状态流转

- `sequence.png`  
  展示主流程中模块间的函数调用与数据传递

---

### 📄 相关建模报告

- `系统建模报告.md`  
- `软件测试与质量保证报告.md`

---
&emsp;
&emsp;
&emsp;
## ✅ 项目依赖（`requirements.txt`）

请使用以下命令安装项目依赖：

```bash
pip install -r documents/requirements.txt
```
&emsp;
&emsp;
&emsp;
## 🧪 测试与质量保障

测试说明详见 [`软件测试与质量保证报告.md`](./documents/软件测试与质量保证报告.md)，主要涵盖以下内容：

- **单元测试**  
  各类与函数是否具备预期功能，例如 `login.authenticate()`、`Recipe.to_dict()` 等方法的准确性。

- **集成测试**  
  生成流程中多个模块组合是否协同正常工作，例如从原料输入到菜谱、图像输出的完整流程测试。

- **异常测试**  
  输入不合理时（如空字符串、非法字符、缺失字段等）的处理能力，是否能给出合理提示或容错机制。

- **图像输出测试**  
  测试是否能够成功保存图片至指定路径，图片是否符合格式要求（如 `.png`、RGB 模式、清晰度等）。

---
&emsp;
&emsp;
&emsp;
## 📌 注意事项

- 所有图片默认保存至 `./pictures/`，请确保该目录存在。
- 所有用户数据将保存至 `./user_data/<username>/`，系统将自动创建所需文件夹。
- 建议避免使用特殊字符作为用户名、菜谱名等输入项，以防止路径异常。
- 若图像生成失败，请检查：
  - API 是否配置正确（如 OpenAI Key、模型服务 URL）
  - 模型服务状态是否在线

---
&emsp;
&emsp;
&emsp;
## 📫 联系与反馈

- 本项目用于课程设计、AI 应用原型研究或小型定制系统开发。
- 若希望扩展支持更多图像模型（如 Stable Diffusion、SDXL）、引入数据库存储、前端界面等，可基于当前结构扩展开发。
- 欢迎提交 issue 或 PR 参与改进与功能增强！

