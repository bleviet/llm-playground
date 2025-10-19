# Quick Start Tutorial - Your First 30 Minutes

This tutorial will get you from zero to running the LLM web summarizer in 30 minutes.

## Prerequisites (5 minutes)

### What You Need
- Python 3.8 or higher
- An OpenAI API key (optional but recommended)
- A Google Gemini API key (optional)

### Check Your Python Version
```bash
python --version
# Should show Python 3.8 or higher
```

## Step 1: Installation (10 minutes)

### Clone or Navigate to the Project
```bash
cd /path/to/llm
```

### Create a Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt.

### Install Dependencies
```bash
pip install openai playwright python-dotenv rich beautifulsoup4 google-generativeai
```

### Install Playwright Browsers
```bash
python -m playwright install
```

This downloads Chromium (needed for web scraping).

## Step 2: Configuration (5 minutes)

### Get API Keys

**OpenAI** (Recommended):
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy it

**Google Gemini** (Optional):
1. Go to https://ai.google.dev/
2. Get an API key
3. Copy it

### Create `.env` File

Create a file named `.env` in the project root:

```env
OPENAI_API_KEY=sk-proj-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
```

**⚠️ Important**: Never commit this file to Git!

## Step 3: Your First Run (5 minutes)

### Start with Ollama Only

If you don't have API keys yet, edit `summarize_webpage.py`:

```python
PROVIDERS = [
    OllamaProvider(model_name="llama3.2:latest"),
    # Comment out the others for now
    # OpenAIProvider(model_name="gpt-4o-mini"),
    # GeminiProvider(strategy=OpenAIAPIStrategy(), model_name="gemini-2.5-flash"),
    # GeminiProvider(strategy=GeminiNativeStrategy(), model_name="gemini-2.5-flash"),
]
```

### Run It!
```bash
python summarize_webpage.py
```

You should see:
```
⠋ Querying Ollama...
╭─────────── Ollama (llama3.2:latest) ───────────╮
│ # Website Summary                              │
│                                                │
│ [Summary appears here in markdown]             │
╰────────────────────────────────────────────────╯
```

🎉 **Congratulations!** You've run your first LLM summarization!

## Step 4: Understanding What Happened (5 minutes)

### The Flow

```
1. summarize_webpage.py (Main Script)
   ↓
2. Loads PROVIDERS list
   ↓
3. For each provider:
   │
   ├─→ scraper.py fetches website content (Playwright)
   │
   ├─→ provider.get_client() creates API client
   │
   ├─→ provider.summarize() generates summary
   │
   └─→ Rich library displays beautiful output
```

### What's Happening in Code?

**1. Provider Initialization** (`summarize_webpage.py`):
```python
PROVIDERS = [
    OllamaProvider(model_name="llama3.2:latest"),
]
```
This creates an Ollama provider with the llama3.2 model.

**2. Fetching Content** (`scraper.py`):
```python
def fetch_website_contents(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        html_content = page.content()
        # ... parse and clean HTML ...
```
Playwright renders JavaScript and waits for the page to load completely.

**3. Generating Summary** (`core/summarizer.py`):
```python
def summarize_and_display(provider, url):
    client = provider.get_client()
    website_content = fetch_website_contents(url)
    summary = provider.summarize(client, website_content, system_prompt, user_prompt_prefix)
    console.print(Panel(Markdown(summary), ...))
```

## Step 5: Your First Customization (5 minutes)

### Change the Target Website

Edit `summarize_webpage.py`:
```python
if __name__ == "__main__":
    target_url = "https://news.ycombinator.com"  # Changed!
    for provider in PROVIDERS:
        summarize_and_display(provider, target_url)
```

Run it again:
```bash
python summarize_webpage.py
```

### Change the Prompt

Edit `core/summarizer.py`:
```python
system_prompt = """
You are a technical analyst that summarizes websites.
Focus on key technical details and implementation.
Respond in markdown with bullet points.
"""
```

Run it again to see the difference!

### Try a Different Model

Edit `summarize_webpage.py`:
```python
PROVIDERS = [
    OllamaProvider(model_name="llama3.3:latest"),  # Different model!
]
```

## Common First-Time Issues

### "Playwright browser not found"
```bash
python -m playwright install
```

### "API key not found"
Check your `.env` file:
- Is it in the project root?
- Are the key names correct (`OPENAI_API_KEY`, `GEMINI_API_KEY`)?
- No extra spaces?

### "Cannot import name..."
Make sure you're in the virtual environment:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

Then reinstall:
```bash
pip install -r requirements.txt  # If you created one
# Or install packages individually
```

### Ollama Not Running
Make sure Ollama is installed and running:
```bash
ollama list  # Should show installed models
ollama pull llama3.2  # If model not available
```

## Next Steps

### Beginner Exercises

1. **Change the Target URL**: Summarize your favorite website
2. **Modify the Prompt**: Make it funnier, more technical, or more concise
3. **Try Different Models**: `llama3.3`, `gpt-4o-mini`, `gemini-1.5-pro`
4. **Add OpenAI Provider**: Get an API key and enable it

### Intermediate Challenges

1. **Add a New Provider**: Try adding Anthropic Claude
2. **Batch Processing**: Summarize multiple URLs
3. **Save Results**: Write summaries to a JSON file
4. **CLI Arguments**: Use `argparse` to pass URL from command line

Example CLI enhancement:
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', help='URL to summarize')
args = parser.parse_args()

target_url = args.url
```

Usage:
```bash
python summarize_webpage.py https://example.com
```

### Advanced Projects

1. **Async Processing**: Run providers in parallel
2. **Streaming Responses**: Display text as it's generated
3. **Web API**: Wrap this in FastAPI
4. **Comparison Dashboard**: Compare summaries side-by-side
5. **Cost Tracking**: Track API costs per provider

## Learning Resources

### Understanding the Code
- Read `README.md` for architecture overview
- Read `ARCHITECTURE.md` for design patterns
- Explore `providers/` to see how providers work
- Check `strategies/` to understand API strategies

### Design Patterns
- Strategy Pattern: https://refactoring.guru/design-patterns/strategy
- Dependency Injection: https://en.wikipedia.org/wiki/Dependency_injection

### LLM APIs
- OpenAI: https://platform.openai.com/docs
- Google Gemini: https://ai.google.dev/docs
- Ollama: https://ollama.ai/

### Python Libraries
- Playwright: https://playwright.dev/python/
- Rich: https://rich.readthedocs.io/
- python-dotenv: https://pypi.org/project/python-dotenv/

## Tips for Success

1. **Start Simple**: Use just one provider initially
2. **Read Error Messages**: They usually tell you exactly what's wrong
3. **Use Print Debugging**: Add `print()` statements to understand flow
4. **Experiment Freely**: This code is meant for learning
5. **Ask Questions**: Open an issue if something is unclear

## Debugging Tips

### See What's Being Sent to the LLM

Add logging to `strategies/openai_api_strategy.py`:

```python
def summarize(self, provider, client, website_content, ...):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website_content},
    ]
    
    print(f"DEBUG: Sending to {provider.name}")
    print(f"DEBUG: Model: {provider.model}")
    print(f"DEBUG: Message length: {len(messages[1]['content'])} chars")
    
    response = client.chat.completions.create(model=provider.model, messages=messages)
    return response.choices[0].message.content
```

### See Raw Website Content

Add to `scraper.py`:

```python
def fetch_website_contents(url):
    # ... existing code ...
    
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    # Debug: Save to file
    with open('debug_content.txt', 'w') as f:
        f.write(text)
    
    return text
```

Now check `debug_content.txt` to see what the LLM receives.

## Summary

In 30 minutes, you've:
- ✅ Set up the development environment
- ✅ Configured API keys
- ✅ Run your first LLM summarization
- ✅ Understood the basic architecture
- ✅ Made your first customizations

**You're ready to explore!** The codebase is designed to be readable and extensible. Don't be afraid to modify things and see what happens.

Happy coding! 🚀
