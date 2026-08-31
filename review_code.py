import os
import sys

# 定义需要检查的敏感词
FORBIDDEN_WORDS = ["password =", "secret_key =", "TODO_URGENT"]

def review_files():
    has_error = False
    print("🔍 开始运行自定义 Python 代码审核...")

    # 遍历项目中的文件（排除不需要检查的目录）
    for root, dirs, files in os.walk("."):
        # 排除隐藏目录（如 .git）和虚拟环境
        if any(ignored in root for ignored in [".git", ".github", "venv", "__pycache__"]):
            continue
            
        for file in files:
            if file.endswith(".py"):  # 只检查 Python 文件
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    for word in FORBIDDEN_WORDS:
                        if word in line:
                            print(f"❌ 错误: 在 {file_path} 第 {line_num} 行发现了禁止的内容: '{word}'")
                            has_error = True

    # 如果有错误，以状态码 1 退出，这会让 GitHub Actions 标记为失败
    if has_error:
        print("\n🚨 代码审核未通过，请修改后重新提交！")
        sys.exit(1)
    else:
        print("\n✅ 代码审核通过！")
        sys.exit(0)

if __name__ == "__main__":
    review_files()
