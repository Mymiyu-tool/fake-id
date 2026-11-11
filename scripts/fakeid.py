#!/usr/bin/env python3
# Description: Generate a complete fictional person profile (name, address, SSN, credit card, education, career, online persona) from haoweichi.com for form testing, fixtures and placeholders.
# Display name: Fake Identity
# 显示名称：虚拟身份生成
# 描述: 生成完整的虚构人物档案：身份、地址、信用卡、学历、职业、生活方式、线上资料
# Timeout: 60
# Parameters:
# {"type":"object","properties":{
#   "country":{"type":"string","description":"Country code: US, GB, CA, AU, DE, FR, JP, SG, HK, TW, KR. Default US"},
#   "section":{"type":"string","enum":["all","basic","address","card","education","career","lifestyle","personal","online"],"description":"Only render one section. Default all"},
#   "format":{"type":"string","enum":["md","json"],"description":"Default md"},
#   "out":{"type":"string","description":"Write the raw JSON to this path, e.g. ~/Desktop/profile.json"},
#   "raw":{"type":"boolean","description":"Append the raw JSON to the output"}
# },"required":[]}
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.haoweichi.com/v1/profile"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

SECTIONS = [
    ("basic", "基本信息", "basic_information", [
        ("full_name", "姓名"), ("gender", "性别"), ("birthday", "生日"), ("age", "年龄"),
        ("race", "族裔"), ("nationality", "国籍"), ("language", "语言"), ("timezone", "时区"),
        ("email", "邮箱"), ("ssn", "SSN"),
    ]),
    ("address", "地址", "address", [
        ("full_address", "完整地址"), ("street", "街道"), ("city", "城市"),
        ("state_full", "州"), ("postcode", "邮编"), ("phone", "电话"),
        ("phone_international", "国际格式"),
    ]),
    ("card", "信用卡", "credit_card", [
        ("card_number", "卡号"), ("card_type", "卡组织"), ("expiry_date", "有效期"),
        ("cvv", "CVV"), ("cardholder_name", "持卡人"), ("bank", "银行"),
    ]),
    ("education", "教育", "education", [
        ("education_level", "学历"), ("major", "专业"), ("school", "学校"),
        ("school_type", "学校类型"),
    ]),
    ("career", "职业", "career", [
        ("occupation.name", "职业"), ("industry", "行业"), ("experience", "经验"),
        ("employment_type", "雇佣类型"), ("income_level", "收入区间"),
        ("company_name", "公司"), ("company_type", "公司类型"),
        ("company_size", "公司规模"), ("platform", "平台"),
        ("summary", "简介"),
    ]),
    ("lifestyle", "生活方式", "lifestyle", [
        ("relationship", "感情状态"), ("pet", "宠物"), ("interests", "兴趣"),
        ("personality", "性格"), ("favorite_foods", "喜欢的食物"),
        ("travel_style", "旅行风格"),
    ]),
    ("personal", "外貌", "personal_information", [
        ("height_cm", "身高(cm)"), ("weight_kg", "体重(kg)"), ("hair_color", "发色"),
        ("eye_color", "眼睛"), ("skin_tone", "肤色"), ("blood_type", "血型"),
        ("body_type", "体型"),
    ]),
    ("online", "线上资料", "online_profile", [
        ("username", "用户名"), ("nickname", "昵称"), ("website", "网站"),
        ("browser", "浏览器"), ("operating_system", "系统"), ("ip_address", "IP"),
        ("security_question", "密保问题"), ("security_answer", "密保答案"),
        ("online_signature", "签名"), ("online_status", "状态"),
    ]),
]


def args():
    raw = os.environ.get("MIYU_ARGS_JSON")
    if not raw:
        raw = sys.stdin.read() or "{}"
    try:
        return json.loads(raw)
    except Exception:
        return {}


def fetch(country):
    req = urllib.request.Request(
        f"{API}?country={urllib.parse.quote(country)}",
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def dig(obj, path):
    cur = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            return None
        cur = cur.get(part)
    return cur


def fmt(v):
    if isinstance(v, list):
        return "、".join(str(x) for x in v)
    return "" if v is None else str(v)


def render(data, section):
    basic = data.get("basic_information", {})
    title = f"# 虚拟身份：{basic.get('country', '?')} · {basic.get('full_name', '?')}"
    lines = [title, ""]
    for key, name, field, rows in SECTIONS:
        if section != "all" and section != key:
            continue
        obj = data.get(field) or {}
        if not isinstance(obj, dict):
            continue
        lines.append(f"## {name}")
        lines.append("")
        lines.append("| 字段 | 值 |")
        lines.append("|---|---|")
        for path, label in rows:
            value = dig(obj, path)
            if value in (None, "", []):
                continue
            lines.append(f"| {label} | {fmt(value)} |")
        lines.append("")
    avatar = dig(basic, "avatar.sizes.large.url")
    if avatar and section in ("all", "basic"):
        lines.append(f"头像：{avatar}")
        lines.append("")
    return "\n".join(lines)


def main():
    a = args()
    country = (a.get("country") or "US").upper()
    if country == "UK":
        country = "GB"
    section = a.get("section") or "all"
    out_fmt = a.get("format") or "md"

    try:
        payload = fetch(country)
    except urllib.error.HTTPError as e:
        print(f"请求失败：HTTP {e.code}（国家代码 {country} 可能不支持，或触发了风控）")
        return
    except Exception as e:
        print(f"请求失败：{type(e).__name__}: {e}")
        return

    if not payload.get("success", True) or "data" not in payload:
        print(json.dumps(payload, ensure_ascii=False)[:500])
        return

    data = payload["data"]

    if a.get("out"):
        path = os.path.expanduser(a["out"])
        os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"已保存原始 JSON：{path}")

    if out_fmt == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(render(data, section))
    if a.get("raw"):
        print("\n```json")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print("```")


if __name__ == "__main__":
    main()
