<p align="center">
  <img src="assets/icon.png" width="128" alt="Fake Identity">
</p>

<h1 align="center">Fake Identity · 虚拟身份生成</h1>

<p align="center">生成一整套虚构人物档案：身份、地址、信用卡、学历、职业、外貌、线上人设，用于表单测试、界面占位和演示数据。</p>

---

## 它生成什么

一次调用返回一个人物的八个部分：

| 部分 | 内容 |
|---|---|
| 基本信息 | 姓名、性别、生日、年龄、族裔、国籍、语言、时区、邮箱、SSN |
| 地址 | 完整地址、街道、城市、州、邮编、电话（本地 + 国际格式） |
| 信用卡 | 卡号、卡组织、有效期、CVV、持卡人、银行 |
| 教育 | 学历、专业、学校、学校类型 |
| 职业 | 职位、行业、经验、雇佣类型、收入区间、公司名 / 类型 / 规模 |
| 生活方式 | 感情状态、宠物、兴趣、性格、喜欢的食物、旅行风格 |
| 外貌 | 身高、体重、发色、眼睛、肤色、血型、体型 |
| 线上资料 | 用户名、昵称、网站、浏览器、系统、IP、密保问答、签名、状态 |

还有一张头像图片的 URL。

数据来自 [haoweichi.com](https://www.haoweichi.com/) 的公开接口，一次一个人物，服务端约 30 秒刷新一次。

## 安装

```bash
git clone https://github.com/Mymiyu-tool/fake-id.git
miyu pkg install ./fake-id
```

或者下载 Release：

```bash
curl -LO https://github.com/Mymiyu-tool/fake-id/releases/latest/download/fake-id-0.1.0.miyu
miyu pkg install fake-id-0.1.0.miyu
```

## 用法

```jsonc
// 默认：美国，完整档案
{}

// 换个国家
{ "country": "JP" }

// 只看地址
{ "country": "GB", "section": "address" }

// 存一份原始 JSON 到桌面
{ "country": "US", "out": "~/Desktop/person.json" }

// 给程序用
{ "country": "DE", "format": "json" }
```

### 参数

| 参数 | 说明 |
|---|---|
| `country` | `US` `GB` `CA` `AU` `DE` `FR` `JP` `SG` `HK` `TW` `KR`，默认 `US`；写 `UK` 会自动转成 `GB` |
| `section` | `all`（默认）/ `basic` / `address` / `card` / `education` / `career` / `lifestyle` / `personal` / `online` |
| `format` | `md`（默认）/ `json` |
| `out` | 把原始 JSON 写到这个路径，支持 `~` |
| `raw` | 在 md 后面附上原始 JSON |

### 关于脱敏

Miyu 会把输出里的邮箱、SSN、卡号、生日替换成 `{{EMAIL_xxx}}` 这样的占位符，这是**对话层的脱敏**，不影响数据本身。要拿完整原值，用 `out` 写文件，直接打开那个文件。

## 用途

- 表单、注册页、KYC 流程的测试数据
- 数据库 seed、演示截图、UI 占位
- 需要"看起来像真人的一整套资料"的场合

## 许可

MIT © 2026 yxxbc
