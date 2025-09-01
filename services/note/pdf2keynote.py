# kimi给的
import os, json, textwrap, zipfile, tempfile, shutil
import fitz  # PyMuPDF
from openai import OpenAI
from keynote import KeynotePresentation  # python-keynote

# ========= 1. 全局配置 =========
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client = OpenAI(api_key=OPENAI_API_KEY)

# 第二轮专用提示词模板（由第一轮返回 key 来选择）
KEYNOTE_PROMPTS = {
    "industry_report": """
        你是经济学讲师的专属助手。
        任务：把下面「行业报告」内容整理成 6-10 页 Keynote。
        结构要求：
        1) 标题页：报告名 + 日期
        2) 行业概览：3 句以内
        3) 市场规模：用 1 张柱状图/折线图（给出数值即可，代码会画图）
        4) 关键驱动因素：3 点
        5) 风险与挑战：2 点
        6) 结论 & 展望
        输出格式：严格 JSON，键是 "slides"，值是数组，每元素为
        {"layout": "title"|"bullet"|"chart", "title": "...", "body": [...], "chart_data": {...}}
    """,
    "financial_report": """
        你是财务分析专家。
        任务：把「企业财报」浓缩成 8-12 页 Keynote，供课堂案例。
        结构：
        1) 封面：公司 + 财年
        2) 收入 & 利润双柱状图
        3) 资产负债表关键指标（表格）
        4) 现金流趋势（折线）
        5) 分业务板块收入占比（饼图）
        6) 管理层讨论重点 3 句
        7) 风险提示
        8) 估值结论
        输出格式同上。
    """,
    "academic_book": """
        你是经济学研究者。
        任务：把「专业著作」章节整理成 5-8 页 Keynote。
        每章对应：
        - 核心论点
        - 关键模型/公式（用 LaTeX 表示）
        - 实证结果
        - 政策含义
        输出格式同上，但允许出现 "formula" layout。
    """
}

# ========= 2. 工具函数 =========
def extract_text(pdf_path: str, max_pages=20) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc[:max_pages]:
        text += page.get_text("text")
    return text

def round1_classify(text: str) -> dict:
    messages = [
        {"role": "system", "content": """
            你是文档分类器。请阅读用户提供的 PDF 前 20 页文本，输出 JSON：
            {
              "type": "industry_report" | "financial_report" | "academic_book",
              "title": "文档标题",
              "confidence": 0-1
            }
            判断标准：
            - 出现“行业”“市场规模”“竞争格局” → industry_report
            - 出现“合并资产负债表”“现金流量表”“年报” → financial_report
            - 出现“著”“ISBN”“参考文献”“模型” → academic_book
        """},
        {"role": "user", "content": text[:6000]}  # 截断避免超限
    ]
    res = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0)
    return json.loads(res.choices[0].message.content)

def round2_generate_keynote(text: str, doc_type: str) -> dict:
    system_prompt = KEYNOTE_PROMPTS[doc_type]
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    res = client.chat.completions.create(model="gpt-4o", messages=messages, temperature=0.3)
    return json.loads(res.choices[0].message.content)

def build_keynote(slides_json: dict, output_path: str):
    kp = KeynotePresentation()
    for s in slides_json["slides"]:
        slide = kp.add_slide()
        slide.set_title(s["title"])
        if s["layout"] == "bullet":
            slide.set_body_bullets(s["body"])
        elif s["layout"] == "chart":
            slide.add_chart(s["chart_data"])
        elif s["layout"] == "formula":
            slide.add_latex(s["body"][0])
        else:  # title
            pass
    kp.save(output_path)

# ========= 3. 主流程 =========
def pdf2keynote(pdf_path: str, keynote_path: str):
    text = extract_text(pdf_path)
    meta = round1_classify(text)
    print("[Round1] 识别结果:", meta)
    keynote_json = round2_generate_keynote(text, meta["type"])
    build_keynote(keynote_json, keynote_path)
    print(f"✅ 已生成 {keynote_path}")

# ========= 4. CLI =========
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("用法: python pdf2keynote.py input.pdf output.key")
        sys.exit(1)
    pdf2keynote(sys.argv[1], sys.argv[2])