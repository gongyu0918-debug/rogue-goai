<p align="center">
  <img src="goai.png" width="96" alt="GoAI icon">
</p>

<h1 align="center">GoAI · Rogue Go Arena</h1>

<p align="center">
  把围棋做成一局会构筑、会翻盘、会爆发的 Roguelike 对弈游戏。
</p>

<p align="center">
  <img alt="Python 3.11" src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Windows first" src="https://img.shields.io/badge/Windows-first-0078D6?style=for-the-badge&logo=windows&logoColor=white">
  <img alt="KataGo powered" src="https://img.shields.io/badge/KataGo-powered-D4AF37?style=for-the-badge">
  <img alt="MIT license" src="https://img.shields.io/badge/License-MIT-111111?style=for-the-badge">
</p>

## 这是什么

GoAI 是一个基于 KataGo 的围棋游戏项目。它保留标准围棋对弈、AI 学习和本地双人玩法，同时加入 Rogue 卡牌、Ultimate 大招、闯关构筑、暗色木纹棋桌和 Windows 一键启动体验。

English: GoAI is a KataGo-powered Go / Weiqi game that blends classic AI play with roguelike cards, explosive ultimate skills, and a polished desktop-first board experience.

## 一眼能看懂的亮点

| 体验 | 你会看到什么 |
| --- | --- |
| Rogue 对局 | 开局三选一卡牌，整局规则被改写 |
| Ultimate 大招 | 双方各拿一张高爆发技能，短局强演出 |
| AI 也能 Rogue | 玩家和 AI 都能获得卡牌，局势更不可预测 |
| 学习模式 | 观看 AI 自战，用来观察布局、节奏和取舍 |
| 本地双人 | 面对面下棋，也能加入 Rogue 规则 |
| 暗色木纹 UI | 正俯视棋桌、木质按钮、沉浸式棋盘背景 |
| 自适应布局 | 适配窗口化、1080p、2K、4K 视图 |
| 引擎回退 | CUDA、OpenCL、CPU 路径按可用环境自动选择 |

## 当前版本重点

- 重做棋盘主界面：正俯视木纹棋桌，大棋盘优先，底部工具按钮贴近真实棋具风格。
- 优化窗口化体验：初始窗口下棋盘会给底部 UI 留出安全区域。
- 重做菜单和下拉控件：开始菜单、设置面板和顶栏统一暗色木纹视觉。
- 重构卡牌数据：Rogue / Ultimate 卡牌集中到 `app/data/cards.py`，便于维护和测试。
- 加强烟测：`card_smoke_test.py` 覆盖 Rogue 触发、主动技能、AI Rogue、双人 Rogue 和 Ultimate 关键链路。

## 玩法模式

### 普通对局

标准 AI 对弈。适合正常练棋、熟悉界面、测试不同 AI 强度。

### Rogue

开局从卡牌里选一张，之后整局围棋都会带着这张规则运行。它可以让 AI 手滑、限制 AI 区域、制造补子、触发连击、改变贴目，甚至把定式目标变成任务。

### Ultimate

双方各拿一张强力大招。节奏更快，效果更夸张，适合短时间体验高冲击局势。

### 学习

让 AI 与 AI 对弈。适合观察不同强度和风格下的布局选择。

### 双人

本地双人对局。适合线下分享，也适合把 Rogue 卡牌当成派对规则来玩。

## 快速开始

### 方式 1：使用 Windows 安装包

从 GitHub Releases 下载最新版安装包，安装后直接打开 GoAI。

项目会优先尝试 CUDA 引擎；环境不满足时会继续尝试 OpenCL 和 CPU。

### 方式 2：从源码运行

环境建议：

- Windows 8.1 / 10 / 11
- Python 3.11
- 一个现代浏览器
- 可选 NVIDIA / OpenCL GPU

安装依赖：

```bash
pip install -r requirements.txt
```

准备 KataGo：

```bash
python setup.py
```

启动桌面入口：

```bash
python launcher.py
```

或者直接启动后端：

```bash
python server.py
```

默认页面由本地服务提供，浏览器会打开 GoAI 主界面。

## KataGo 文件说明

仓库默认保留源码和配置，体积较大的第三方引擎文件、模型权重和运行时文件通过安装脚本或发布包获取。

KataGo 目录约定见 [katago/README.md](katago/README.md)。

## 项目结构

```text
app/
  config/          游戏和引擎配置
  data/            Rogue / Ultimate 卡牌数据
  domain/          棋局状态与坐标领域模型
  runtime/         WebSocket 行为和引擎运行逻辑
static/
  index.html       主游戏界面
  assets/          木纹、棋盘、按钮图标等资源
katago/            KataGo 配置和本地引擎文件位置
server.py          FastAPI 后端
launcher.py        Windows 桌面启动入口
card_smoke_test.py 卡牌与关键规则烟测
```

## 开发命令

运行卡牌烟测：

```bash
python card_smoke_test.py
```

运行运行时烟测：

```bash
python runtime_smoke_test.py
```

构建 Windows 发布包：

```powershell
.\build_windows_release.ps1
```

## 卡牌系统

当前版本包含：

- 34 张 Rogue 卡
- 25 张 Ultimate 卡
- Rogue 精选池、AI Rogue 池、双人 Rogue 池、闯关 Beta 池
- Ultimate 精选池和 AI Ultimate 池

完整卡牌定义位于 [app/data/cards.py](app/data/cards.py)。

<details>
<summary>Rogue 卡牌例子</summary>

| 卡牌 | 玩法变化 |
| --- | --- |
| 傀儡术 | 先指定 AI 下一手位置，随后 AI 被迫落到那里 |
| 战争迷雾 | 前期不断刷新禁区，后续持续封锁 AI 点位 |
| 神之一手 | 踩中隐藏区域后爆出己方棋子 |
| 三连星 | 前两手命中星位后补出第三颗星位棋和援军 |
| 快速思考 | 限时连击窗口，禁用推荐点位和悔棋 |
| 代练上号 | 后段由更强 AI 临时代打 |
| 起死回生 | 低胜率时触发一次逆转型补救 |

</details>

<details>
<summary>Ultimate 大招例子</summary>

| 大招 | 玩法变化 |
| --- | --- |
| 连珠棋 | 高概率追加行动 |
| 无限增殖 | 落点周围爆出多颗同色棋 |
| 双刀流 | 每回合固定连续落两手 |
| 时空裂缝 | 抹去对手最近行动 |
| 天崩地裂 | 十字方向清除敌子 |
| 神之一手 | 隐藏命中后清空敌子并铺满己棋 |
| 五子连珠爆发 | 五连触发大范围清除和补子 |

</details>

## 设计方向

GoAI 的目标是让围棋在保留基本棋感的同时更容易被新玩家尝试：

- 棋盘始终是视觉中心。
- UI 像棋具，按钮像可以按下的实体物件。
- AI 强度有回退路径，旧电脑也能进入游戏。
- 卡牌规则提供戏剧性，同时通过烟测保护关键行为。
- 中文和英文界面并行维护。

## 第三方与授权

GoAI 使用 MIT License。详见 [LICENSE](LICENSE)。

核心第三方组件：

- KataGo by David J Wu (`lightvector`) and contributors
- KataGo neural network weights from `katagotraining.org`
- FastAPI, Uvicorn, websockets and related Python packages

本项目是独立爱好者项目，与 KataGo 上游保持独立。第三方授权和说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 仓库策略

- 源码、配置、UI 资源进入 Git。
- 日志、构建产物、本地测试文件、模型和打包二进制保持在仓库外。
- Windows 安装包建议发布到 GitHub Releases。

## 开发透明度

项目开发过程中使用了 AI 编码辅助工具。维护者负责玩法方向、体验判断、打包目标、测试反馈和发布取舍。

