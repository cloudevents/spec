# 用于事件传输的 HTTP 1.1 Web Hooks - 1.0.3（制作中）

## 摘要

"Webhooks"是一种被广泛应用在应用和HTTP终端间传输通知消息的模式。尽管这种模式已经被广泛使用，但目前仍然没有一个对Web Hooks的正式定义。本规范旨在制定一个用于 [CNCF CloudEvents][ce]的Web Hooks的定义，但本定义仅作用于CloudEvents范围内。

## 目录

1. [简介](#1-introduction简介)

- 1.1. [一致性](#11-conformance一致性)
- 1.2. [与HTTP的关系](#12-relation-to-http与http的关系)

2. [传输通知](#2-delivering-notifications传输通知)
3. [认证](#3-authorization认证)
4. [滥用保护](#4-abuse-protection滥用保护机制)
5. [引用](#5-references引用)

## 1. Introduction/简介

["Webhooks"][webhooks]是一种被广泛应用在应用和HTTP终端间传输通知消息的模式。这些Webhook应用，允许其它应用程序注册成为一个接收当前有效通知的HTTP终端。

本规范根据以下内容制定了一套HTTP方法：发送者下发通知的过程、在事件传输中保护传输目标的认证模型以及一个保护发送者不被滥用成为HTTP洪水攻击发起者的注册握手机制。

### 1.1. Conformance/一致性

本文档中的关键词 "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD","SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" 需要按照 [RFC2119][rfc2119] 中的描述来理解。

### 1.2. Relation to HTTP/与HTTP的关系

本规范规定了一系列规则，以限制具体[HTTP 方法][rfc7231-section-4]和头部的使用以及处理。

本规范同样适用于HTTP/2 ([RFC7540][rfc7540]),因为它本身就与HTTP 1.1 的语义兼容。

## 2. Delivering notifications/传输通知

### 2.1. 传输请求

通知是通过HTTP请求的方式传输的，在响应中携带了该传输的状态。

在连接中必须使用HTTP-over-TLS (HTTPS) [RFC2818][rfc2818]。

用来传输请求的HTTP方法必须是[POST类型][post].

在HTTP 头部中[`Content-Type`][content-type]必须被指定，同时每个请求都必须要携带该内容类型下的有效负载(即有效内容)。本规范不允许没有携带有效负载的请求（比如某些通知请求的全部数据都在HTTP头部而没有内容数据）。

除上述限制外，本规范不会更多地限制通知的内容，同样不会强制用来传输的[HTTP 目标资源][rfc7230-section-5-1]。

如果传输目标支持并要求[滥用保护](#4-abuse-protection滥用保护机制)机制，则传输的请求必须包含`WebHook-Request-Origin`头部。`WebHook-Request-Origin`头部的值是一个能标识出发送者的DNS域名表达形式。

### 2.2. 传输响应

传输响应可能会包含一种提供具体状态信息的负载，这些信息是用来处理错误的。本规范不会去定义这种负载。

服务端的响应必须不能包含[3xx HTTP 状态码][3xx]同时客户端也不能使用此类状态码进行跳转。

一旦请求被接收、处理了且在响应中包含了处理细节的负载，则响应必须要包含[200 OK][200]或是[201 Created][201]状态码。在这种情形下，该响应必须要包含[`Content-Type`][content-type]头部。

如果请求被接收、处理了，但是请求中没有有效负载，则响应中必须包含[201 Created][201] or [204 No Content][204]状态码。

如果请求被接收了，但尚未被处理或是处理状态仍是未知的，则响应中必须包含[202 Accepted][202]状态码。

如果一个传输目标已经过期了，但HTTP站点仍然存在，则HTTP站点应当返回一个[410 Gone][410]状态码，同时发送者应当不再向该目标发送更多的通知。

如果传输目标因为超过请求限制而无法处理请求，它应当返回一个[429 Too Many Requests][429]状态码，同时必须包含[`Retry-After`][retry-after]头部。发送者必须观察Retry-After的值，直到指定时间后再发送后续请求。

如果传输因为通知格式不能被理解而被拒绝接收，则响应中必须包含[415 Unsupported Media Type][415]状态码。

其它的所有错误处理情形都需要参照[RFC7231][rfc7231]的表述。

## 3. Authorization/认证

传输请求必须要使用以下两种方式之一进行认证，这两种方法都依赖OAuth 2.0 Bearer 令牌 [RFC6750][rfc6750] 模型。

传输目标必须同时支持两种认证方式。

客户端可以使用任何基于令牌的认证方案。令牌可以采取任意形式，可以是标准化的令牌格式或是简单的key表达式。

禁止使用任何基于挑战的认证方案。

### 3.1. 头部请求认证字段

访问令牌是在HTTP/1.1中定义的头部[`Authorization`][authorization]字段中携带的。

对于[OAuth 2.0 Bearer][bearer] 令牌而言，"Bearer"方案必须被使用。

示例：

```text
POST /resource HTTP/1.1
Host: server.example.com
Authorization: Bearer mF_9.B5f-4.1JqM
```

### 3.2 URI 查询参数

当通过HTTP请求URI发送访问令牌时，客户需要按照"统一资源标志符 (URI): 通用句法" [RFC3986][rfc3986]中定义的方式，将"access_token"参数当作请求URI的查询内容进行发送。

例如，客户端生成如下的HTTP请求：

```text
POST /resource?access_token=mF_9.B5f-4.1JqM HTTP/1.1
Host: server.example.com
```
HTTP请求URI可能会包含其它特定的参数，此时必须正确地使用"&"(ASCII code 38)字符，将"access_token"参数与其它特定的参数分割开来。


例如:

    https://server.example.com/resource?access_token=mF_9.B5f-4.1JqM&p=q

使用URI查询查询参数这种形式的客户端，必须要发送一个缓存控制的头部并包含"no-store"选项。服务端成功(2XX 状态)的响应必须包含声明了"private"选项的缓存控制头部。

因为URI方法天然的安全弱点(参照[RFC6750, Section 5][rfc6750])，比如包含访问令牌的URI极有可能被记录，除了在无法使用"Authorization"字段的场景下，你都不应该这种方式来发送发送访问令牌。其它在[RFC6750][rfc6750]中告诫在此处同样适用。

## 4. Abuse Protection/滥用保护机制

任何允许任意HTTP终端注册或是传输通知的系统都可能受到潜在的滥用攻击，比如一些人恶意或是无意的注册一些不期望收到请求的系统地址或是一些注册方无法被认证的地址。在极端情况下，一个实现通知的网络基础设施可能会被滥用成为DoS攻击的发起方。

为了保护发送不受恶意滥用伤害，合法的传输目标需要表明它同意接收这条传输给它的通知。

上述的传输同意模式是通过下面的验证握手机制实现的。握手可以在注册时执行或是被当作一个被传输前的请求在传输前执行。

在这里，理解握手机制并不是为了建立一个认证上下文是尤为重要的。握手机制只是用来保护发送方不会将通知发送到并不想接收的接受者那里去。尽管在本规范中强制使用了认证模型，但这种模型无法保护那些没有实现访问控制但又不想接收不需要流量的网站，因此在这里`Authorization`是没有用的。

传输目标应该支持滥用保护特性。如果一个目标端不支持此特性，发送方可能会选择不发送到这个目标端，或是以一个特别低速率去发送请求。

### 4.1. 验证请求

验证请求使用了HTTP的[OPTIONS][options]方法。请求会被重定向到注册时指定的URI资源上去。

有了验证请求，发送方向目标端索要发送通知的权限，验证请求可以声明一个希望的请求速率（如每分钟收到多少请求）。

传输目标将会响应一个权限声明以及允许的请求速率。

下面就是在验证请求中使用的头部字段。

#### 4.1.2. WebHook-Request-Origin

希望发送通知的发送者必须要在验证请求和请求权限中包含`WebHook-Request-Origin`字段。这个字段必须要包含一个能标识发送系统的DNS表达式（如eventemitter.example.com）。这个字段的值是用来标识所有发送方的实例，而不是一个单独主机。

一旦握手和权限被承认，发送者必须在每个请求中都包含`WebHook-Request-Origin`这个字段以及它对应的值。


示例：

```text
WebHook-Request-Origin: eventemitter.example.com
```

#### 4.1.3. WebHook-请求回调

`WebHook-Request-Callback`是一个可选的用来补充`WebHook-Request-Origin`的字段。它允许传输目标通过HTTPs回调的方式异步地同意权限请求。

如果接收程序没有清楚地表明支持握手机制，管理员仍然可以在日志中找到回调的URL，再手动调用它来授权访问。


传输目标通过发布一个给定URL的HTTPS GET 或 POST请求来授权访问。HTTP GET请求通过浏览器来手动执行。

传输目标可能会在回调中包含`WebHook-Allowed-Rate`字段。

这个URL没有正式的限制条件，但它应该包含一个能标识出传输目标的标识符，同时它应该包含一个密钥来使URL更加难猜，从而使第三方就无法轻松地冒充传输目标。


示例:

```text
WebHook-Request-Callback: https://example.com/confirm?id=12345&key=...base64...
```

#### 4.1.4. WebHook-请求速率

发送者可能通过`WebHook-Request-Rate`字段来向接受者请求一个合适的发送请求速率。这个值以字符串形式来表示一个大于0的整数，它代表着每分钟发送多少个请求。

比如，下面的例子在索要一个每分钟发送120次请求的权限：


```text
WebHook-Request-Rate: 120
```

### 4.2. 验证响应

当且仅在传输目标允许事件传输的情况下，它必须要通过`WebHook-Allowed-Origin` 和`WebHook-Allowed-Rate`字段来响应请求。

如果传输目标选择回调的方式来授权，则它不会使用响应字段。

如果传输目标不允许事件传输或是不期望收到事件但仍想处理HTTP OPTIONS 方法，当前的响应则不应该被当作批准授权，握手机制此时不应该依靠状态码来判断。如果传输目标不希望处理HTTP OPTIONS方法，它应该以405状态码来响应，就像它不支持HTTP OPTIONS一样。

OPTIONS响应应该包含[Allow][allow]字段来表明[POST][post]方法已经被允许了。其它方法类型可能也被允许了，但它们并不在本规范的讨论范围内。

#### 4.2.1. WebHook-允许源头

当传输目标同意通知事件的传输时，必须要返回`WebHook-Allowed-Origin`字段。该字段的值必须是请求中`WebHook-Request-Origin`字段中发送方的名称，或者是一个单独的星号（\*）表明传输目标同意来自任意源头的通知。

```text
WebHook-Allowed-Origin: eventemitter.example.com
```

或

```text
WebHook-Allowed-Origin: *
```

#### 4.2.2. WebHook-允许速率

当请求中包含`WebHook-Request-Rate`字段时，响应中必须包含`WebHook-Allowed-Rate`字段。其它情况下`WebHook-Allowed-Rate`字段应当被返回。

本字段的值用来表示同意发送通知的速率。它可以是一个单独的星号（\*）或是字符串形式来表示一个大于0的整数。星号代表对速率没有限制。整数代表着每分钟接收多少个请求。对于请求速率大于允许接收速率的情形，发送方应当考虑限流。通过拒绝请求来限流可以参考HTTP的[429 过多请求][429]状态码。


示例： 下面的HTTP头部允许每分钟100次请求的发送速率:

```text
WebHook-Allowed-Rate: 100
```

## 5. References/引用

- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC2818][rfc2818] HTTP over TLS
- [RFC6750][rfc6750] The OAuth 2.0 Authorization Framework: Bearer Token Usage
- [RFC6585][rfc6585] Additional HTTP Status Codes
- [RFC7230][rfc7230] Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and
  Routing
- [RFC7231][rfc7231] Hypertext Transfer Protocol (HTTP/1.1): Semantics and
  Content
- [RFC7235][rfc7235] Hypertext Transfer Protocol (HTTP/1.1): Authentication
- [RFC7540][rfc7540] Hypertext Transfer Protocol Version 2 (HTTP/2)

[ce]: spec.md
[webhooks]: https://progrium.github.io/blog/2007/05/03/web-hooks-to-revolutionize-the-web/index.html
[content-type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[retry-after]: https://tools.ietf.org/html/rfc7231#section-7.1.3
[authorization]: https://tools.ietf.org/html/rfc7235#section-4.2
[allow]: https://tools.ietf.org/html/rfc7231#section-7.4.1
[post]: https://tools.ietf.org/html/rfc7231#section-4.3.3
[options]: https://tools.ietf.org/html/rfc7231#section-4.3.7
[3xx]: https://tools.ietf.org/html/rfc7231#section-6.4
[200]: https://tools.ietf.org/html/rfc7231#section-6.3.1
[201]: https://tools.ietf.org/html/rfc7231#section-6.3.2
[202]: https://tools.ietf.org/html/rfc7231#section-6.3.3
[204]: https://tools.ietf.org/html/rfc7231#section-6.3.5
[410]: https://tools.ietf.org/html/rfc7231#section-6.5.9
[415]: https://tools.ietf.org/html/rfc7231#section-6.5.13
[429]: https://tools.ietf.org/html/rfc6585#section-4
[bearer]: https://tools.ietf.org/html/rfc6750#section-2.1
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986]: https://tools.ietf.org/html/rfc3986
[rfc2818]: https://tools.ietf.org/html/rfc2818
[rfc6585]: https://tools.ietf.org/html/rfc6585
[rfc6750]: https://tools.ietf.org/html/rfc6750
[rfc7159]: https://tools.ietf.org/html/rfc7159
[rfc7230]: https://tools.ietf.org/html/rfc7230
[rfc7230-section-3]: https://tools.ietf.org/html/rfc7230#section-3
[rfc7231-section-4]: https://tools.ietf.org/html/rfc7231#section-4
[rfc7230-section-5-1]: https://tools.ietf.org/html/rfc7230#section-5.1
[rfc7231]: https://tools.ietf.org/html/rfc7231
[rfc7235]: https://tools.ietf.org/html/rfc7235
[rfc7540]: https://tools.ietf.org/html/rfc7540
