from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def fetch_website_contents(url):
    """
    Fetches the textual content from a given website URL using Playwright.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            # Wait for network to be idle, which is a good signal that JS has finished executing
            page.goto(url, wait_until='networkidle')
            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Error fetching website content with Playwright: {e}"

if __name__ == '__main__':
    # Example usage
    test_url = "https://www.python.org/"
    content = fetch_website_contents(test_url)
    print(content)
