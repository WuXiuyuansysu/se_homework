import os, subprocess, urllib.request
from PIL import Image

OUTPUT_DIR = "./pictures"
OUTPUT_FORMAT = "png"
PLANTUML_JAR = "./documents/umls_utils/plantuml.jar"


def setup_plantuml():
    """
    检查并下载 PlantUML JAR 文件，如果本地不存在则自动下载。

    此函数用于确保生成 UML 图所需的 PlantUML JAR 文件已就绪。
    若文件路径 `PLANTUML_JAR` 所指向的 JAR 文件不存在，将从 GitHub 官方地址下载并保存到指定位置。

    返回:
        str: 本地 PlantUML JAR 文件的绝对路径。
    """
    if not os.path.exists(PLANTUML_JAR):
        os.makedirs(os.path.dirname(PLANTUML_JAR), exist_ok=True)
        urllib.request.urlretrieve(
            "https://github.com/plantuml/plantuml/releases/download/v1.2023.12/plantuml-1.2023.12.jar",
            PLANTUML_JAR
        )
    return os.path.abspath(PLANTUML_JAR)


def make_puml(recipe, path):
    """
    将菜谱步骤信息转换为 PlantUML 顺序图的代码，并写入指定路径的 `.puml` 文件。

    此函数会遍历菜谱中的每个步骤，按顺序生成 PlantUML 语法描述，
    模拟厨师（Chef）与厨房（Kitchen）之间的交互流程，最终形成完整的顺序图描述文本。

    参数:
        recipe (dict): 包含菜谱信息的字典，要求包含 "steps" 键，
                       每个步骤应为字典，包含 "description" 和 "duration" 字段。
        path (str): `.puml` 文件的保存路径。

    例子:
        recipe = {
            "steps": [
                {"description": "洗菜", "duration": "2分钟"},
                {"description": "切菜", "duration": "3分钟"}
            ]
        }
        make_puml(recipe, "output/recipe.puml")
    """
    lines = [
        "@startuml",
        'skinparam defaultFontName "Microsoft YaHei"',
        "participant Chef",
        "participant Kitchen"
    ]
    for step in recipe["steps"]:
        lines.append(f"Chef -> Kitchen : {step['description']}")
        lines.append(f"return {step['duration']}")
    lines.append("@enduml")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def build_sequence(recipe):
    """
    根据给定的菜谱描述生成 UML 顺序图，并返回图像对象。

    此函数会：
    1. 创建输出目录（如果尚不存在）；
    2. 将菜谱内容转换为 PlantUML 格式并保存为 `.puml` 文件；
    3. 调用本地 PlantUML 工具渲染为图像（如 PNG 或 SVG）；
    4. 返回生成的图像对象。

    参数:
        recipe (str): 菜谱的结构化描述信息，用于生成顺序图。

    返回:
        PIL.Image.Image: 返回生成的顺序图图像对象，可用于展示或保存。

    异常:
        subprocess.CalledProcessError: 如果 PlantUML 渲染失败。
        FileNotFoundError: 如果渲染后未找到输出图像文件。
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    base = "recipe"
    puml_path = os.path.join(OUTPUT_DIR, f"{base}.puml")
    make_puml(recipe, puml_path)
    jar_path = setup_plantuml()
    cmd = [
        "java", "-Dfile.encoding=UTF-8", "-jar", jar_path,
        f"-t{OUTPUT_FORMAT}", f"-o{os.path.abspath(OUTPUT_DIR)}",
        os.path.abspath(puml_path)
    ]
    subprocess.run(cmd, check=True)
    return Image.open(os.path.join(OUTPUT_DIR, f"{base}.{OUTPUT_FORMAT}"))


# 示例调用
recipe_example = {
    "name": "经典意大利面",
    "ingredients": [
        {"name": "意大利面", "quantity": "200克"},
        {"name": "橄榄油", "quantity": "2汤匙"},
        {"name": "大蒜", "quantity": "3瓣"},
        {"name": "番茄酱", "quantity": "150克"},
        {"name": "盐", "quantity": "适量"},
        {"name": "黑胡椒", "quantity": "适量"},
        {"name": "罗勒叶", "quantity": "适量"}
    ],
    "steps": [
        {"step": 1, "description": "煮沸一锅盐水，放入意大利面煮约8-10分钟至熟", "duration": "10分钟"},
        {"step": 2, "description": "锅中加热橄榄油，爆香切片大蒜", "duration": "2分钟"},
        {"step": 3, "description": "加入番茄酱煮沸，调入盐和黑胡椒", "duration": "5分钟"},
        {"step": 4, "description": "将煮熟的意大利面沥水后加入锅中拌匀", "duration": "1分钟"},
        {"step": 5, "description": "撒上新鲜罗勒叶装饰，盛盘", "duration": "1分钟"}
    ],
    "total_time": "20分钟"
}

if __name__ == "__main__":
    img = build_sequence(recipe_example)
    img.show()          # 在默认图片查看器中打开
