# pptx（预置主题模板版）
## 安装
将本仓库作为 skills 源安装后，`pptx` 技能会自动被发现。
如果你需要在本地直接运行脚本生成 .pptx：
```bash
cd skills/pptx
npm install
```
## 快速开始
1. 复制示例并修改内容：
```bash
cp examples/deck.example.json /tmp/deck.json
```
2. 生成 PPTX：
```bash
node scripts/build.mjs --input /tmp/deck.json --output /tmp/output.pptx --theme ink-classic
```
## deck.json 结构
```json
{
  "meta": {
    "title": "演示标题",
    "subtitle": "副标题",
    "author": "作者",
    "date": "2026-05-12"
  },
  "defaults": {
    "variant": "light"
  },
  "slides": [
    {
      "type": "cover",
      "title": "一人公司",
      "subtitle": "被 AI 折叠的组织",
      "kicker": "私享会 · Keynote",
      "lead": "一句话摘要，最多两行。",
      "meta": ["Guizang", "独立创作者"],
      "foot": ["一场关于 AI·组织·个体的分享", "— 2026 —"]
    }
  ]
}
```
### slides[].variant
可选：`light` / `dark`。不填时会用该类型的默认值（如 `cover`、`question` 默认 `dark`）。
### 图片
支持在以下 slide 类型里使用本地图片路径：
- `two-column`：`image`
- `image-grid`：`images[]`
- `mixed`：`image`
建议使用 PNG/JPG，本地绝对路径最稳。
## 主题来源与致谢
主题色板与“电子杂志×电子墨水”的审美方向参考了 [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（MIT）。
