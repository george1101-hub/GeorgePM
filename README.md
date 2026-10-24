# GeorgePM

**从需求定义、交互原型到研发交付，一个插件、三个 Skill。**

GeorgePM 将三阶段产品工作流整理成可复用的指引和模板，面向使用 AI 辅助产品设计的产品经理、独立开发者与小团队。默认中文，跟随用户语言。首版 v0.1.0。

| 阶段 | Skill | 输入 | 输出 |
| --- | --- | --- | --- |
| ① 需求定义 | `pm-define` | 想法、业务资料或迭代需求 | 可评审 PRD、需求编号、验收、待决项 |
| ② 交互原型 | `pm-prototype` | 已确认 PRD、设计系统或原型基线 | 可交互原型、评审说明、组件标注、覆盖与验证记录 |
| ③ 研发交付 | `pm-deliver` | 最终原型、有效决议、PRD | 自包含 HTML 研发规格、状态/异常、GWT 验收、埋点、实现差距 |

每个 Skill 可以独立使用，也能顺序交接。阶段切换以用户授权为准；完成文档不自动意味着评审通过、服务接入或生产验收。

## 快速开始

本仓库提供 Skill 源码和兼容插件清单，尚不代表已进入任何官方插件商店。无需 API Key、MCP 服务或作者的私人环境；原型真实验证需要宿主具备浏览器工具。

### Codex

在支持 repo marketplace 的 Codex 环境，将下载或克隆后的仓库作为本地来源添加：

```sh
codex plugin marketplace add /absolute/path/to/GeorgePM
```

然后按当前客户端的插件入口安装 GeorgePM，并在新聊天测试。仓库提供 `.agents/plugins/marketplace.json`；具体入口与可用性取决于客户端。也可把需要的 `skills/pm-*` 目录完整复制到宿主支持的 Skill 目录，保留 `references/` 和 `agents/`。

```text
使用 $pm-define，帮我梳理一个共享会议室预约工具的需求。
使用 $pm-prototype，按已确认的 PRD 做桌面 Web 原型，仅本地演示。
使用 $pm-deliver，把这个最终原型整理为研发交付规格。
```

### Claude Code

仓库同时提供 `.claude-plugin/plugin.json` 与本地 marketplace。在支持该命令的客户端，使用完整的本地仓库路径：

```text
/plugin marketplace add /absolute/path/to/GeorgePM
/plugin install georgepm@georgepm-marketplace
```

通过技能列表选择需求定义、交互原型或研发交付，或自然语言说明当前阶段。两类客户端的打包结构有官方文档依据，首版尚未完成真实宿主安装与跨客户端端到端试用；静态校验不能证明安装成功。

## 看一个例子

[会议室预约契约走读](examples/meeting-room/README.md) 用同一条需求展示三阶段如何衔接，包含明确的模拟和待验证标记。它是文档示例，**不包含可运行预约应用、真实截图或生产实现**。

模板在各 Skill 的 `references/` 下。建议项目按 `stage1/`、`stage2/`、`stage3/` 和 `HANDOFF.md` 存放；实际路径服从用户选择。插件不创建或强制使用作者本机目录。

## 包内与边界

- 内置：分批澄清、范围继承、稳定需求 ID、覆盖表、双向组件标注要求、真实验证记录、原型到规格追溯。
- 不捆绑：私人记忆、现有业务项目、品牌素材、账号、密钥、模型 SDK、外部组件库或生命周期 hooks。
- 不自动执行：公开发布、真实支付、服务写入、全局安装或替用户发送消息。
- 每个阶段保留已确认、建议默认、待产品确认、待技术确认、已测与未测的区别。

## 验证

Python 3.10+，仅标准库：

```sh
python3 scripts/validate_package.py
python3 -m unittest discover -s tests -v
```

验证器检查清单一致性、Skill/引用结构及明显隐私风险；不替代人工审查、模型行为测试或真实浏览器验收。实测范围见 [VALIDATION.md](VALIDATION.md)。

## 来源、许可与贡献

本公开稿依据作者已有三阶段工作流重新整理，移除项目专属规则和本机依赖；没有捆绑第三方 Skill、运行库和业务素材。说明见 [来源与边界](docs/provenance.md)。本仓库代码、文档与原创示例统一使用 [MIT License](LICENSE)。未来引入第三方资源时需逐项保留来源与许可。

提交改进时附触发场景、当前问题、预期结果与验证范围。请勿上传真实用户数据、内部业务文件或凭据。

官方打包参考：[OpenAI 插件打包](https://developers.openai.com/plugins/build/plugins)、[Claude Code 插件参考](https://code.claude.com/docs/en/plugins-reference)。GitHub 发布与插件市场上架是不同事项；本次只分发 GitHub 仓库。
