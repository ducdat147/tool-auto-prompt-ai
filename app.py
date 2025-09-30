# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from io import BytesIO
import os

app = FastAPI(title="Prompt Builder – FastAPI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(BASE_DIR, "templates")

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


def _normalize(val):
    if val is None:
        return ""
    if isinstance(val, (list, tuple)):
        return "\n".join(f"- {str(x).strip()}" for x in val if str(x).strip())
    return str(val).strip()


def build_prompt(role, context, objective, constraints, examples, style):
    role = _normalize(role)
    context = _normalize(context)
    objective = _normalize(objective)
    constraints = _normalize(constraints)
    examples = _normalize(examples)
    style = _normalize(style)

    blocks = []
    if role:
        blocks.append(f"Bạn là {role}")
    if context:
        blocks.append(f"Ngữ cảnh: {context}")
    if objective:
        blocks.append(f"Mục tiêu: {objective}")
    if constraints:
        blocks.append(f"Ràng buộc: {constraints}")
    if examples:
        blocks.append(f"Ví dụ:\n{examples}")
    if style:
        blocks.append(f"Bắt đầu trả lời ngay và {style}")
    else:
        blocks.append("Bắt đầu trả lời ngay và trình bày từng bước, rõ ràng, tập trung vào kết quả cuối.")
    return "\n\n".join(blocks).strip() + "\n"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    template = env.get_template("index.html")
    return template.render(request=request)


@app.post("/build", response_class=HTMLResponse)
async def build(request: Request,
                role: str = Form(""),
                context: str = Form(""),
                objective: str = Form(""),
                constraints: str = Form(""),
                examples: str = Form(""),
                style: str = Form("")):
    prompt = build_prompt(role, context, objective, constraints, examples, style)
    template = env.get_template("result.html")
    return template.render(request=request, prompt=prompt)


@app.post("/download")
async def download(prompt: str = Form(...)):
    buf = BytesIO(prompt.encode("utf-8"))
    headers = {
        "Content-Disposition": 'attachment; filename="prompt.txt"'
    }
    return StreamingResponse(buf, media_type="text/plain; charset=utf-8", headers=headers)

@app.post("/download_md")
async def download_md(prompt: str = Form(...)):
    # Wrap prompt into a Markdown code block for portability
    md_content = "```text\n" + prompt + "\n```"
    buf = BytesIO(md_content.encode("utf-8"))
    headers = {
        "Content-Disposition": 'attachment; filename="prompt.md"'
    }
    return StreamingResponse(buf, media_type="text/markdown; charset=utf-8", headers=headers)
