import os, subprocess, urllib.request
from PIL import Image

OUTPUT_DIR = "./pictures"
OUTPUT_FORMAT = "png"
PLANTUML_JAR = "./documents/umls_utils/plantuml.jar"


def setup_plantuml():
    if not os.path.exists(PLANTUML_JAR):
        os.makedirs(os.path.dirname(PLANTUML_JAR), exist_ok=True)
        urllib.request.urlretrieve(
            "https://github.com/plantuml/plantuml/releases/download/v1.2023.12/plantuml-1.2023.12.jar",
            PLANTUML_JAR
        )
    return os.path.abspath(PLANTUML_JAR)


def make_puml(recipe, path):
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
