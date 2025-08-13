
# Prompt Builder (FastAPI + HTML)

## Chạy local
```bash
pip install fastapi uvicorn jinja2
uvicorn app:app --reload --port 8000
# Mở trình duyệt: http://127.0.0.1:8000
```

## Cấu trúc
```
fastapi_prompt_builder/
├── app.py
├── static/
│   ├── styles.css
│   └── app.js
└── templates/
    ├── index.html
    └── result.html
```

## Tips
- Paste multiline thoải mái ở Context/Constraints/Examples/Style.
- Nút **Copy** và **Tải .txt** có sẵn.
- Logic build prompt nằm ở `build_prompt(...)` để bạn tái sử dụng.


## Export mới
- **Tải .md**: nút "Tải .md" sẽ export nội dung prompt vào code block Markdown.
- **Copy 1-click**: nút "Copy" copy thẳng vào clipboard, không popup alert; nút đổi thành "✓ Copied" trong 1.5s.
