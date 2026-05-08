# 聊天记录分析 · 操作指南

> 只需要 2 步，约 10 分钟。全程在你自己电脑上完成，数据不会上传到任何地方。

---

## 第一步：安装 Python

1. 打开这个链接：https://www.python.org/downloads/
2. 点击黄色的 **Download Python 3.x.x** 按钮
3. 下载完成后双击安装包
4. **重要：安装界面底部，勾选 ✅ Add Python to PATH**（不勾这个后面会报错）
5. 点 Install Now，等它装完

> 装完后不用打开 Python，继续下一步。

---

## 第二步：运行分析

1. **确认微信已打开并登录**

2. 桌面新建一个文件夹，名字随便起（比如 `temp`）

3. 在这个文件夹里，新建一个文本文件，把下面这段内容粘贴进去，保存，然后把文件名改成 `start.bat`（注意后缀是 `.bat` 不是 `.txt`）：

```bat
@echo off
chcp 65001 >nul 2>&1
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请右键此文件，选「以管理员身份运行」
    pause
    exit /b 1
)
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo 未检测到 Python，请先安装
    start https://www.python.org/downloads/
    pause
    exit /b 1
)
git clone https://github.com/863401402/she-love-me.git
cd she-love-me
python scripts\one_click.py
pause
```

4. **右键点击** `start.bat` → 选择 **「以管理员身份运行」**

5. 如果弹出安全提示，点「更多信息」→「仍要运行」

6. 脚本会自动下载项目并开始分析，按提示操作：
   - 看到联系人列表后，输入要分析的人的**序号**（比如输入 `1` 选第一个）
   - 等它跑完，看到「数据提取完成」就行

7. 进入 `she-love-me` → `data` 文件夹

8. 把里面的 3 个文件发给分析者：
   - `messages.json`
   - `stats.json`
   - `chat_history.txt`

---

## 常见问题

**Q: 提示「未检测到 Python」怎么办？**
A: 说明安装时没勾 Add to PATH。重新安装 Python，记得勾选底部的 Add Python to PATH。

**Q: 提示「未检测到 Git」怎么办？**
A: 去 https://git-scm.com/download/win 下载安装 Git，安装过程全部点下一步即可。装完后重新运行 start.bat。

**Q: 提示「需要管理员权限」怎么办？**
A: 右键点击 start.bat，选「以管理员身份运行」。

**Q: 解密失败怎么办？**
A: 确认微信已打开并登录。如果还不行，把错误信息截图发给分析者。

**Q: 这个工具安全吗？**
A: 所有数据处理都在你电脑上完成，不联网、不上传。分析完成后你可以删除整个文件夹。

---

## 分析完成后

分析者会把 HTML 报告发给你。你可以删除桌面上的临时文件夹，不会影响你的微信。
