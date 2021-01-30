from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routes import router as GitaAPIRouter

app = FastAPI()


@app.get("/", tags = ["Root"], response_class = HTMLResponse)
async def read_root() -> str:
    return "Hi, I'm a GitaTeluguAPI running and powered by vercel.<br/>" \
           "Please check the source code at https://github.com/naveennamani/gita-telugu-api and" \
           "please check the docs <a href='/docs'>here</a>.<br/>" \
           "Support the developer https://t.me/naveennamani"


app.include_router(GitaAPIRouter)
