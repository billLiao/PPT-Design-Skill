---
name: pptx
description: "当用户需要创建或输出 .pptx（演示文稿/幻灯片/slide deck/pitch deck/路演材料）时使用此技能。该技能提供 5 套预置主题（电子杂志×电子墨水风格）与 10 种常用版式模板，并通过脚本直接生成可下载的 .pptx 文件；适合从大纲/文档快速生成一份有设计感的演示稿。"
license: MIT
---
## PPTX Skill（带预置主题模板）
### 你能做什么
- 选择预置主题（5 套）与页面版式（10 种），生成一份风格一致的 .pptx
- 通过 `deck.json` 描述内容与结构，使用脚本生成 `output.pptx`
### 工作流
1. 澄清需求
   - 受众与场景（路演/内部分享/技术发布/作品集）
   - 时长与页数目标（10-12 页 / 15-20 页 / 25+ 页）
   - 是否有既有材料（文档/链接/旧 PPT/数据/图片）
   - 主题选择（见下方主题列表）
2. 产出大纲与“页-版式”映射
   - 避免全程标题+要点，至少混用 4 种以上版式
3. 生成 `deck.json`
   - 放到项目工作目录（或 `skills/pptx/examples/` 基于示例改）
4. 生成 .pptx
   - 首次使用需安装依赖：
     - 进入 `skills/pptx/` 运行 `npm install`
   - 生成：
     - `node scripts/build.mjs --input /absolute/path/to/deck.json --output /absolute/path/to/output.pptx --theme ink-classic`
5. 交付前自检
   - 打开 .pptx 做视觉检查：是否溢出、是否遮挡、字号是否过小、是否有主题不一致的页面
### 主题（5 套预置）
只能从预设中选择，不接受随意自定义色值（避免搭配失控）：
- `ink-classic`：墨水经典（通用默认）
- `indigo-porcelain`：靛蓝瓷（科技/研究/数据）
- `forest-ink`：森林墨（自然/文化/非虚构）
- `kraft-paper`：牛皮纸（人文/怀旧/文学）
- `dune`：沙丘（艺术/设计/创意）
### 版式（10 种）
`deck.json` 的 `slides[].type` 支持：
- `cover`：开场封面（默认暗底）
- `section`：章节幕封
- `big-number`：数据大字报
- `two-column`：左文右图 / 双栏内容
- `image-grid`：图片网格（多图对比）
- `pipeline`：流程（步骤卡片）
- `question`：问题页（默认暗底）
- `quote`：大引用
- `before-after`：对比（Before/After）
- `mixed`：图文混排
### 输出约定
- 默认 16:9
- 默认输出路径以 `--output` 为准；如果未指定，脚本会生成到当前工作目录
