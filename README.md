# PPT-Design-Skill
本仓库提供一个 `pptx` Agent Skill：在生成 `.pptx` 的基础上，内置 5 套预置主题（电子杂志×电子墨水风格）与 10 种常用页面版式模板，直接产出可下载的 PowerPoint 文件。

## 安装（npx skills）
```bash
npx skills add billLiao/PPT-Design-Skill --skill ppt-design-skill
```

## 触发方式
- “帮我做一份 PPT / 幻灯片 / slide deck / pitch deck”
- “把这份大纲做成 .pptx”
- “用墨水经典/靛蓝瓷/森林墨/牛皮纸/沙丘主题做演示稿”

## 本地脚本生成（可选）
如果你希望在本地直接运行脚本生成 `.pptx`：
```bash
cd skills/pptx
npm install
node scripts/build.mjs --input /absolute/path/to/deck.json --output /absolute/path/to/output.pptx --theme ink-classic
```
示例 `deck.json` 在 [deck.example.json](file:///workspace/skills/pptx/examples/deck.example.json)。

## 技能说明
- 技能主文件：[SKILL.md](file:///workspace/skills/pptx/SKILL.md)
- 详细用法：[README.md](file:///workspace/skills/pptx/README.md)

## 参考项目
- [anthropics/skills PPTX](https://github.com/anthropics/skills/tree/main/skills/pptx)
- [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)
