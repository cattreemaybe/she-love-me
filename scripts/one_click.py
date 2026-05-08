#!/usr/bin/env python3
"""
one_click.py - 一键聊天记录分析（数据提取阶段）

运行此脚本将自动完成：
  1. 环境检查 + 安装解密器依赖
  2. 解密微信数据库
  3. 列出联系人供选择
  4. 提取消息 + 统计分析 + 生成采样

最终在 data/ 目录生成：
  - messages.json   （聊天记录）
  - stats.json      （统计数据）
  - chat_history.txt （分层采样）

将这三个文件发给分析者即可。
"""
import argparse
import json
import os
import platform
import subprocess
import sys

# ─── 工具函数 ───

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)


def python_cmd():
    """返回当前 Python 解释器路径"""
    return sys.executable


def run_step(description, cmd, cwd=None, check=True):
    """运行一个步骤，打印描述，返回成功/失败"""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}")
    try:
        result = subprocess.run(
            cmd, cwd=cwd or PROJECT_DIR,
            capture_output=False,
            text=True,
        )
        if result.returncode != 0:
            print(f"\n[!] 步骤失败（退出码 {result.returncode}）")
            if check:
                return False
        return True
    except FileNotFoundError:
        print(f"\n[!] 找不到命令: {cmd[0]}")
        print("    请确认已安装 Python 3.9+ 并添加到 PATH")
        return False
    except Exception as e:
        print(f"\n[!] 执行出错: {e}")
        return False


def run_step_capture(cmd, cwd=None):
    """运行并捕获输出，返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, cwd=cwd or PROJECT_DIR,
            capture_output=True, text=True,
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def wait_confirm(msg="按回车继续..."):
    """等待用户确认"""
    print(f"\n{msg}", end="", flush=True)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


# ─── 主流程 ───

def main():
    parser = argparse.ArgumentParser(
        description="一键聊天记录分析（数据提取阶段）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--decrypted-dir",
        default=None,
        help="已解密的数据库目录（跳过解密步骤，直接进入联系人选择）",
    )
    parser.add_argument(
        "--contact",
        default=None,
        help="直接指定联系人名字（跳过选择步骤）",
    )
    parser.add_argument(
        "--skip-decrypt",
        action="store_true",
        help="跳过解密步骤（用于已解密的情况）",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="输出目录（默认 data/）",
    )
    args = parser.parse_args()

    py = python_cmd()
    is_windows = platform.system() == "Windows"
    decrypted_dir = args.decrypted_dir or os.path.join(
        PROJECT_DIR, "vendor", "wechat-decrypt", "decrypted"
    )
    output_dir = os.path.join(PROJECT_DIR, args.output_dir)

    # ─── 开始 ───
    print("""
╔══════════════════════════════════════════════╗
║         她不一样 · 一键分析工具              ║
║         数据提取阶段                         ║
╚══════════════════════════════════════════════╝

本工具将自动完成以下步骤：
  1. 环境检查 + 安装依赖
  2. 解密微信数据库
  3. 选择联系人
  4. 提取消息 + 统计 + 采样

最终生成 3 个文件，发给分析者即可。
""")

    if is_windows:
        print("  [提示] 检测到 Windows 系统，请确认已以管理员身份运行此终端。")
    else:
        print("  [提示] 检测到 macOS/Linux 系统。")

    wait_confirm("按回车开始...")

    # ─── Step 1: 环境检查 ───
    ok = run_step(
        "Step 1/5: 环境检查 + 安装依赖",
        [py, os.path.join(SCRIPT_DIR, "setup_check.py"), "--ensure-decryptor"],
    )
    if not ok:
        print("\n[!] 环境检查失败。请检查：")
        print("    - 微信是否已打开并登录")
        print("    - Python 版本是否 >= 3.9")
        print("    - Windows 用户请以管理员身份运行")
        sys.exit(1)

    # ─── Step 2: 解密 ───
    if not args.skip_decrypt:
        # 检查是否已解密
        if os.path.isdir(decrypted_dir) and any(
            f.endswith(".db") for f in os.listdir(decrypted_dir)
        ):
            print(f"\n[*] 检测到已解密的数据库: {decrypted_dir}")
            answer = input("    是否跳过解密？(Y/n): ").strip().lower()
            if answer != "n":
                print("[*] 跳过解密步骤")
            else:
                ok = run_step(
                    "Step 2/5: 解密微信数据库",
                    [py, os.path.join(SCRIPT_DIR, "decrypt_wechat.py")],
                )
                if not ok:
                    print("\n[!] 解密失败。请检查：")
                    if is_windows:
                        print("    - 是否以管理员身份运行终端")
                        print("    - 微信是否处于登录状态")
                    else:
                        print("    - 是否已对微信做 ad-hoc 重签名")
                        print("    - 是否以 sudo 运行此脚本")
                    sys.exit(1)
        else:
            ok = run_step(
                "Step 2/5: 解密微信数据库",
                [py, os.path.join(SCRIPT_DIR, "decrypt_wechat.py")],
            )
            if not ok:
                print("\n[!] 解密失败。请检查：")
                if is_windows:
                    print("    - 是否以管理员身份运行终端")
                    print("    - 微信是否处于登录状态")
                else:
                    print("    - 是否已对微信做 ad-hoc 重签名")
                    print("    - 是否以 sudo 运行此脚本")
                sys.exit(1)

    # ─── Step 3: 选择联系人 ───
    print(f"\n{'='*50}")
    print("  Step 3/5: 选择联系人")
    print(f"{'='*50}")

    contact_name = args.contact
    if not contact_name:
        # 列出联系人
        retcode, stdout, stderr = run_step_capture(
            [py, os.path.join(SCRIPT_DIR, "list_contacts.py"),
             "--decrypted-dir", decrypted_dir]
        )
        if retcode != 0:
            print(f"[!] 列出联系人失败: {stderr}")
            sys.exit(1)

        try:
            contacts = json.loads(stdout)
        except json.JSONDecodeError:
            # stdout 可能包含非 JSON 的进度信息，尝试提取 JSON 部分
            lines = stdout.strip().split("\n")
            for i, line in enumerate(lines):
                if line.strip().startswith("["):
                    try:
                        contacts = json.loads("\n".join(lines[i:]))
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                print("[!] 无法解析联系人列表")
                sys.exit(1)

        # 显示前 30 个
        top = contacts[:30]
        print(f"\n找到 {len(contacts)} 个联系人，显示消息最多的前 {len(top)} 个：\n")
        for i, c in enumerate(top, 1):
            name = c.get("display_name", c.get("nick_name", c.get("username", "?")))
            count = c.get("message_count", 0)
            print(f"  {i:2d}. {name}  ({count:,} 条)")

        # 选择
        while True:
            print()
            choice = input("请输入序号或名字: ").strip()
            if not choice:
                continue

            # 尝试按序号
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(top):
                    contact_name = top[idx]["display_name"]
                    break
                else:
                    print(f"[!] 序号超出范围，请输入 1-{len(top)}")
                    continue
            except ValueError:
                pass

            # 按名字匹配
            matched = [c for c in contacts if choice in (
                c.get("display_name", ""),
                c.get("nick_name", ""),
                c.get("remark", ""),
                c.get("username", ""),
            )]
            if len(matched) == 1:
                contact_name = matched[0]["display_name"]
                break
            elif len(matched) > 1:
                print(f"[!] 找到 {len(matched)} 个匹配，请更精确地输入：")
                for m in matched[:5]:
                    print(f"    - {m.get('display_name', '?')} ({m.get('message_count', 0):,} 条)")
                continue
            else:
                print(f"[!] 找不到名为「{choice}」的联系人，请重新输入")
                continue

    print(f"\n[*] 已选择: {contact_name}")

    # ─── Step 4: 提取 + 统计 + 采样 ───
    os.makedirs(output_dir, exist_ok=True)

    messages_path = os.path.join(output_dir, "messages.json")
    stats_path = os.path.join(output_dir, "stats.json")
    history_path = os.path.join(output_dir, "chat_history.txt")

    # 4a: 提取消息
    ok = run_step(
        "Step 4/5: 提取消息",
        [py, os.path.join(SCRIPT_DIR, "extract_messages.py"),
         "--decrypted-dir", decrypted_dir,
         "--contact", contact_name,
         "--output", messages_path],
    )
    if not ok:
        print("\n[!] 提取消息失败")
        sys.exit(1)

    # 4b: 统计分析
    ok = run_step(
        "统计分析",
        [py, os.path.join(SCRIPT_DIR, "stats_analyzer.py"),
         "--input", messages_path,
         "--output", stats_path],
    )
    if not ok:
        print("\n[!] 统计分析失败")
        sys.exit(1)

    # 4c: 生成采样
    ok = run_step(
        "生成分层采样",
        [py, os.path.join(SCRIPT_DIR, "build_chat_history.py"),
         "--input", messages_path,
         "--output", history_path],
    )
    if not ok:
        print("\n[!] 采样生成失败")
        sys.exit(1)

    # ─── 完成 ───
    print(f"""
╔══════════════════════════════════════════════╗
║              数据提取完成！                  ║
╚══════════════════════════════════════════════╝

联系人: {contact_name}
输出目录: {output_dir}

生成的文件:
  1. messages.json     （聊天记录）
  2. stats.json        （统计数据）
  3. chat_history.txt  （分层采样）

请将 {output_dir} 目录下的这 3 个文件发给分析者。

完成后可删除整个项目文件夹。
""")

    # 列出文件大小
    for fname in ["messages.json", "stats.json", "chat_history.txt"]:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            if size > 1024 * 1024:
                print(f"  {fname}: {size / 1024 / 1024:.1f} MB")
            else:
                print(f"  {fname}: {size / 1024:.0f} KB")

    print()


if __name__ == "__main__":
    main()
