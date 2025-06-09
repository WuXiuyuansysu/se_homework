import os
import subprocess
import glob  # 用于文件查找

# 使用标准路径风格
OUTPUT_DIR = "./documents"
OUTPUT_FORMAT = "png"
PLANTUML_JAR = "./documents/umls_utils/plantuml.jar"

def setup_plantuml():
    if not os.path.exists(PLANTUML_JAR):
        print("Downloading plantuml.jar...")
        import urllib.request
        urllib.request.urlretrieve(
            "https://github.com/plantuml/plantuml/releases/download/v1.2023.12/plantuml-1.2023.12.jar",
            PLANTUML_JAR
        )
    return os.path.abspath(PLANTUML_JAR)

def generate_diagrams():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    puml_dir = os.path.join("documents", "umls_utils")
    puml_files = glob.glob(os.path.join(puml_dir, "*.puml"))
    
    print(f"Find:")
    for file_path in puml_files:
        print(f" -{os.path.basename(file_path)}")
    
    jar_path = setup_plantuml()
    
    for puml_file in puml_files:
        # 构建输出路径
        file_name = os.path.splitext(os.path.basename(puml_file))[0]
        output_file = os.path.join(OUTPUT_DIR, f"{file_name}.{OUTPUT_FORMAT}")
        
        # 执行PlantUML命令
        cmd = [
            "java", "-jar", jar_path,
            f"-t{OUTPUT_FORMAT}",
            f"-o{os.path.abspath(OUTPUT_DIR)}",  # 使用绝对路径确保正确
            os.path.abspath(puml_file)  # 使用绝对路径
        ]
        subprocess.run(cmd, check=True)
        print(f"Generated: {output_file}")

if __name__ == "__main__":
    generate_diagrams()
    print("Done")