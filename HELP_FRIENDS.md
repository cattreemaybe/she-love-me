# 帮朋友分析聊天记录 · 完整指南

> 本文档记录了从零开始帮助朋友完成聊天记录分析的完整流程，包括技术方案、远程指导技巧和注意事项。

---

## 概览

「她不一样」可以帮朋友分析微信聊天记录，生成恋爱关系分析报告。整个流程分两个阶段：

| 阶段 | 谁来操作 | 产出 |
|------|---------|------|
| 数据提取 | 朋友在自己电脑上完成 | `messages.json` + `stats.json` + `chat_history.txt` |
| AI 分析 + 报告 | 你在自己电脑上完成 | `analysis.json` + HTML 报告 |

数据全程在朋友电脑上处理，不上传任何服务器。

---

## 前置条件

### 朋友需要满足的条件

- Windows 电脑（macOS 需要额外的微信重签名步骤，不建议非技术朋友尝试）
- 微信已安装并登录
- 能装 Python、能打开终端（有你远程指导）

### 你需要准备的

- 你的 Mac 上已跑通过完整流程
- GitHub 仓库已更新（含一键脚本）：`https://github.com/cattreemaybe/she-love-me`
- 视频通话工具（微信视频 / 腾讯会议 / 向日葵远程控制）

---

## 方案选择

### 方案 A：一键脚本 + 视频指导（推荐）

朋友运行一个 bat 脚本，自动完成全部数据提取。你只在选人环节介入。

**适合：** 朋友完全不懂技术，你需要全程指导

### 方案 B：向日葵远程控制

朋友安装向日葵，给你授权码，你直接操作他的电脑。

**适合：** 朋友连终端都不会打开，或者你想最快完成

---

## 方案 A 详细流程

### Step 1：发送材料给朋友

通过微信发送以下内容：

1. **操作指南**（直接粘贴 `FRIEND_GUIDE.md` 的内容到聊天窗口）
2. **仓库地址**：`https://github.com/cattreemaybe/she-love-me`

### Step 2：视频通话 + 屏幕共享

发起微信视频通话，让朋友共享屏幕。

#### 环节 1：安装 Python（约 3 分钟）

指导朋友：

> 「打开浏览器，输入 python.org/downloads，下载那个黄色按钮的 Python。安装的时候，**最底下有个 Add to PATH 的勾选框，一定要勾上**，然后点 Install Now。」

**你需要确认的事：** 安装界面底部的 Add to PATH 是否勾选。

#### 环节 2：打开管理员终端（约 1 分钟）

> 「按键盘左下角的 Windows 键，输入 powershell，搜到之后**右键点击**，选『以管理员身份运行』。」

#### 环节 3：下载项目 + 运行脚本（约 5 分钟）

让朋友在终端输入：

```powershell
git clone https://github.com/cattreemaybe/she-love-me.git
cd she-love-me
scripts\setup_windows.bat
```

> 「把这三行复制粘贴到终端里，按回车。」

**如果提示 Git 未安装：**

> 「去 git-scm.com/download/win 下载 Git，安装时全部点下一步就行。装完后重新输入那三行命令。」

#### 环节 4：选择联系人（约 1 分钟）

脚本会列出联系人列表。

> 「输入你要分析的那个人的序号，比如第一个就输入 1。」

朋友告诉你选了谁，你确认。

#### 环节 5：等待完成（约 2 分钟）

脚本自动运行提取消息、统计分析、生成采样。

> 「等它显示『数据提取完成』就行。」

#### 环节 6：收文件

> 「现在打开 she-love-me 文件夹，再打开里面的 data 文件夹，把里面三个文件发给我。」

朋友通过微信发送：
- `messages.json`
- `stats.json`
- `chat_history.txt`

#### 环节 7：清理

> 「分析完了，你可以把桌面上的 she-love-me 文件夹整个删掉。」

---

## 你收到文件后的操作

### Step 1：放入 data 目录

把朋友发来的 3 个文件放到你的项目 `data/` 目录下。

### Step 2：读取数据

读取 `data/stats.json` 和 `data/chat_history.txt`，结合分析框架进行 AI 深度分析。

### Step 3：生成 analysis.json

按照 F → A → B → C → D → E → G 模块顺序完成分析，保存到 `data/analysis.json`。

### Step 4：生成报告

```bash
python3 scripts/generate_html_report.py \
  --stats data/stats.json \
  --analysis data/analysis.json \
  --contact "联系人名字" \
  --output reports/
```

### Step 5：发送报告

把生成的 HTML 文件发给朋友。

---

## 文件清单

本次新增的文件：

| 文件 | 用途 |
|------|------|
| `scripts/one_click.py` | 一键分析脚本，串联全部数据提取步骤 |
| `scripts/setup_windows.bat` | Windows 双击启动器，自动检测 Python/Git/下载项目 |
| `FRIEND_GUIDE.md` | 发给朋友的零基础操作指南 |

本次修复的文件：

| 文件 | 修复内容 |
|------|---------|
| `scripts/list_contacts.py` | SQLite 只读模式（immutable） |
| `scripts/extract_messages.py` | SQLite 只读模式（immutable） |
| `scripts/generate_html_report.py` | 缺失的 render_html 函数 |

---

## 一键脚本参数

`scripts/one_click.py` 支持以下参数：

```
--decrypted-dir DIR    已解密的数据库目录（跳过解密）
--contact NAME         直接指定联系人（跳过选择）
--skip-decrypt         跳过解密步骤
--output-dir DIR       输出目录（默认 data/）
```

示例：如果朋友已经解密过，可以跳过解密直接选人：

```bash
python scripts/one_click.py --skip-decrypt --contact "小红"
```

---

## 常见问题

### 朋友遇到的问题

| 问题 | 解决方案 |
|------|---------|
| 提示「未检测到 Python」 | 重新安装 Python，勾选 Add to PATH |
| 提示「未检测到 Git」 | 去 git-scm.com/download/win 安装 Git |
| 提示「需要管理员权限」 | 右键选「以管理员身份运行」 |
| 解密失败 | 确认微信已打开并登录 |
| 提示「无法连接到 GitHub」 | 检查网络，或用向日葵远程帮你操作 |

### 你遇到的问题

| 问题 | 解决方案 |
|------|---------|
| 收到的文件不全 | 确认朋友发了 data/ 下全部 3 个文件 |
| 生成报告报错 | 检查 analysis.json 格式是否符合 schema |
| 朋友没有 Windows | macOS 需要额外做微信重签名，建议用向日葵远程操作 |

---

## 安全与隐私

- 所有数据处理在朋友电脑上完成，不联网、不上传
- `vendor/`、`data/`、`reports/` 均在 `.gitignore` 中，不会被提交到 GitHub
- 分析完成后建议朋友删除整个项目文件夹
- 你收到的 3 个文件包含聊天记录内容，分析完成后也应删除

---

## 未来优化方向

- [ ] 朋友端做成 `.exe` 安装包，双击即用
- [ ] 加一个自动清理脚本 `cleanup.py`
- [ ] 支持 macOS 朋友（封装重签名流程）
- [ ] 支持 QQ 聊天记录（QCE 已有基础）
