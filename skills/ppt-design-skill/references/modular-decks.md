# 分模块生成（≥15 页 deck）

> 单文件 .mjs 在 15 页以上会失控：改一页要在几千行里找位置，QA 定位难，子代理没法并行。
> 分模块管线把每页变成独立文件，规划门禁（outline.json）→ 桩生成 → 并行填充 → 一键编译。

## 何时用

- **≥15 页**：走本管线（`scripts/scaffold_deck.py` 一条命令出工程）
- <15 页：单文件即可（SKILL.md Step 2 常规流程）

## 工程结构

```
deck/
├── outline.json          # 规划门禁的产出物（scaffold 复制一份进来）
├── ppt-themes/           # 解析后的主题 JSON（compile/token_check 从这里找）
│   └── swiss-orange.theme.json
├── theme-loader.mjs      # 主题解析 + 归一化（scaffold 生成，勿改）
├── compile.mjs           # 组装器（scaffold 生成，勿改）
├── slide-01.mjs          # 每页一个模块
├── slide-02.mjs
└── ...
```

## 模块契约（锁死，compile.mjs 强制）

```js
export const meta = { page: 3, layout: "big-number" };   // 可选但强烈建议
export function createSlide(pres, theme) {               // 必须同步导出
  const slide = pres.addSlide();
  // ...只用 theme token（theme.colors.* / theme.fonts.* / theme.background*）
  return slide;
}
```

- `createSlide(pres, theme)` **同步**导出——compile 按文件名顺序调用
- `meta.page` 与文件名序号不一致 → compile 直接 fail（防乱序）
- 颜色/字体只用 theme token，硬编码 hex 会被 `token_check.py` 拦下
- 模块之间**不互相 import**、不共享可变状态——每页独立可渲染

## 工作流

```bash
# 1. 规划门禁（Step 1 产出 outline.json 后）
python3 scripts/qa/outline_check.py outline.json

# 2. 一键出工程（门禁不过会拒绝生成）
python3 scripts/scaffold_deck.py outline.json --out-dir deck --theme swiss-orange
cd deck && npm install pptxgenjs

# 3. 填充模块（自己写或子代理并行，见下节）
#    单页调试：node slide-05.mjs          → preview-05.pptx（只渲染这一页）

# 4. 编译
node compile.mjs --theme swiss-orange    # → output.pptx（outline 页数不符会 fail）

# 5. QA（SKILL.md Step 3 全套；token 门禁直接扫模块）
python3 <skill>/scripts/qa/token_check.py slide-*.mjs --theme swiss-orange
python3 <skill>/scripts/qa/cjk_overflow_check.py output.pptx
python3 <skill>/scripts/qa/contrast_check.py output.pptx
```

修复循环：改单个 slide-NN.mjs → `node slide-NN.mjs` 单页预览 → 复检相邻页 → 重新 compile。**不要为改一页重跑整套生成。**

## 子代理并行填充（≤5 页/代理）

主会话把模块分给子代理，每个代理 ≤5 页；代理只写自己名下的 slide-NN.mjs，不碰共享文件（compile.mjs / theme-loader.mjs / outline.json 由主会话持有，避免补丁撞车）。

给子代理的提示词模板（替换大写占位）：

```
你在为一个 pptxgenjs deck 写幻灯片模块。工作目录：/path/to/deck

1. 读 outline.json，你负责 page {{A}}-{{B}}（slide-{{A}}.mjs 到 slide-{{B}}.mjs，已生成桩）
2. 读 ppt-themes/{{THEME}}.theme.json 了解全部 token；读同目录一个已完成的模块作参照（如有）
3. 每页按 layout id 找版式代码：<skill>/templates/layouts/（杂志 magazine-layouts.md / 瑞士 swiss-layouts.md / 分析 analysis-models.md），按 design-playbook 自适应规则变形
4. 硬规则：只用 theme token；标题 ≤12 字；正文 ≤90 字；每页至少一个视觉元素；行文用 outline 的 title/summary，不要自由发挥
5. 自检：node slide-NN.mjs 出 preview-NN.pptx 确认能渲染、无报错
6. 汇报：每页完成情况 + 你拿不准的排版决策（不要自行改 outline.json / compile.mjs / 其他模块）
```

主会话收齐后：`node compile.mjs` → 全套 QA → 按失败模式目录修复。

## 与 QA 门禁的对应

| 门禁 | 作用对象 | 阶段 |
|------|----------|------|
| outline_check.py | outline.json | 规划（scaffold 前置） |
| token_check.py | slide-*.mjs | 填充后 / 编译前 |
| compile.mjs 页数/meta 校验 | 模块 vs outline | 编译 |
| cjk_overflow / contrast / font_check | output.pptx | 编译后 |
| edge_check.py | 渲染 PNG | 渲染后 |
