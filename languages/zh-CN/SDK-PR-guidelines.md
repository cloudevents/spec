# 拉取请求指导

语言: [English](../../docs/SDK-maintainer-guidelines.md) | [简体中文](SDK-PR-guidelines.md)

<!-- no verify-specs -->

在这里你会发现一步一步的指导，创建，提交和更新
对 SDK 存储库的 pull 请求。我们希望它能帮助你度过一段轻松的时光
管理你的工作，并在贡献时获得积极、满意的体验
你的代码。谢谢你的参与!火箭:

- [开始](#开始)
- [分支](#分支机构)
- [提交的信息](#提交的信息)
- [与主流保持同步](#与main保持同步)
- [提交和更新一个 Pull Request](#提交和更新你的拉请求)
- [恭喜你!](#恭喜你)

## 开始

在创建一个 pull 请求时，首先 fork 存储库并将其克隆到您的
本地开发环境。然后将存储库添加为上游。

```console
git clone https://github.com/mygithuborg/sdk-[lang].git
cd sdk-[lang]
git remote add upstream https://github.com/cloudevents/sdk-sdk-[lang].git
```

## 分支机构

你需要做的第一件事是为你的工作创建一个分支。
如果您提交的拉请求修复或涉及现有的
GitHub 问题，你可以在你的分支名称中使用它来保持事情的组织性。
例如，如果您要创建一个拉请求来修复
[httpAgent 的错误](https://github.com/cloudevents/sdk-javascript/issues/48)
你可以创建一个名为“48-fix-http-agent-error”的分支。

```console
git fetch upstream
git reset --hard upstream/main
git checkout FETCH_HEAD
git checkout -b 48-fix-http-agent-error
```

## 提交的信息

请按照[传统的提交规范](https://www.conventionalcommits.org/en/v1.0.0/)摘要。
提交的第一行应该以类型为前缀，应该是单个类型句，并简洁地指出此提交更改了什么。

如果可能，所有提交消息行都应该少于 80 个字符。

一个好的提交消息的例子。

```log
docs: remove 0.1, 0.2 spec support from README
```

### 签署你的提交

每次提交都必须签名。在提交时使用'——signoff '标志。

```console
git commit --signoff
```

这将为每个 git 提交消息添加一行:

    署名:乔·史密斯&lt;joe.smith@email.com&gt;

使用您的真实姓名(对不起，不能使用化名或匿名投稿。)

终止是提交消息末尾的签名行。你的
签名证明您编写了补丁或以其他方式有权通过
它是开源代码。看到[developercertificate.org](http://developercertificate.org/)
有关认证全文。

确保有“user.name”和“user”。邮件'设置在你的 git 配置。
如果你的 git 配置信息设置正确，那么查看“git log”
你的提交看起来像这样:

```
Author: Joe Smith <joe.smith@email.com>
Date:   Thu Feb 2 11:41:15 2018 -0800

    Update README

    Signed-off-by: Joe Smith <joe.smith@email.com>
```

注意“Author”和“Signed-off-by”行是匹配的。如果他们不这么做，你的 PR 就会这么做
被自动 DCO 检查拒绝。

## 与'main'保持同步

当你在你的分支上工作时，“main”上可能会发生变化。之前
提交你的拉请求，确保你的分支已经更新
使用最新的提交。

```console
git fetch upstream
git rebase upstream/main
```

如果您在分支上更改的文件是
也改变了主要。来自' git '的错误消息将指示是否发生冲突
存在哪些文件需要注意。然后，解决每个文件中的冲突
用' git rebase—Continue '继续重基。

如果你已经向你的“origin”分叉推送了一些更改，你就会
需要强行推动这些变化。

```console
git push -f origin 48-fix-http-agent-error
```

## 提交和更新你的拉请求

在提交 pull 请求之前，您应该确保所有的测试
成功地通过。

一旦你发送了 pull request， ' main '可能会继续进化
在你的 pull request 落地之前。如果在' main '上有任何提交
与您的更改发生冲突时，您可能需要用
这些更改都是在 pull 请求落地之前进行的。解决冲突
的方式。

```console
git fetch upstream
git rebase upstream/main
# fix any potential conflicts
git push -f origin 48-fix-http-agent-error
```

这将导致 pull 请求与您的更改一起更新
CI 将重新运行。

维护者可能会要求您对 pull 请求进行更改。有时,这些
更改很小，不应该出现在提交日志中。例如，你可以
在你的代码注释中有一个拼写错误，应该在合并之前修复。
您可以通过一个交互式的
变基。参见[git 文档](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History)
获取详细信息。

```console
git commit -m "fixup: fix typo"
git rebase -i upstream/main # follow git instructions
```

一旦重新创建了提交的基础，就可以像以前一样将 push 强制推到 fork。

## 恭喜你!

恭喜你!你已经做到了!我们非常感谢你的时间和精力
你为这个项目付出了很多。谢谢你！
