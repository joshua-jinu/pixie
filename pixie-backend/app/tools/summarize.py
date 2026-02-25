import httpx
from newspaper import Article
from bs4 import BeautifulSoup

from langchain_core.tools import tool
from app.llm.gemini import get_llm


async def extract_text_from_url(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    async with httpx.AsyncClient(timeout=20, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        html = response.text

    article = Article(url)
    article.download(input_html=html)
    article.parse()

    text = article.text

    if not text:
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = "\n".join(paragraphs)

    return text[:12000]

@tool
async def summarize(url: str) -> str:
    """Summarize the content of a webpage given its URL."""
    
    text = await extract_text_from_url(url)

    if not text:
        return "Unable to extract content from the webpage."

    prompt = f"""
    Summarize the following webpage content in 5 concise bullet points:

    {text}
    """

    llm = get_llm()

    response = await llm.ainvoke(prompt)

    return response.content