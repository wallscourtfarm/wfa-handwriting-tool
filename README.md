# Handwriting Sheet Generator

A Streamlit web app for generating dotted handwriting practice PDFs. Built for Wallscourt Farm Academy staff.

## What it does

Paste in words or sentences, choose a font style (print, pre-cursive or cursive — all dotted for tracing), set how many practice lines to add after each item, and download a print-ready PDF.

## Fonts included

All three fonts are embedded directly in `handwriting_sheet.py` as base64 — no separate font files are needed and nothing extra needs installing.

| Option | Font | Style |
|--------|------|-------|
| Print | Sassoon Infant Dotted | Non-cursive print |
| Pre-cursive | Linkpen 3b Print Dot | Pre-cursive with exit strokes |
| Cursive | XCCW Joined Dotted | Fully joined cursive |

These fonts are used under school licence and this repository is for internal WFA/CLF use only.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploying to Streamlit Community Cloud

1. Push this repository to GitHub (it can be private).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
3. Click **New app**.
4. Select your repository, branch (`main`) and set the main file path to `app.py`.
5. Click **Deploy**. Streamlit installs dependencies from `requirements.txt` automatically.
6. Share the URL with colleagues — they need no account to use it.

The app is free to host on Streamlit Community Cloud for public or private repos.

## Repository contents

```
handwriting-tool/
├── app.py                 # Streamlit UI
├── handwriting_sheet.py   # PDF generation engine (fonts embedded)
├── requirements.txt
├── .gitignore
└── README.md
```
