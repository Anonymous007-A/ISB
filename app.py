GitHub → app.py → Edit (pencil icon)

**generate_demo_leads function replace karo:**
```python
def generate_real_leads(query, count=50):
    api_key = "YOUR_SERPAPI_KEY_HERE"  # Paste your key
    
    url = f"https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": 100
    }
    
    response = requests.get(url, params=params)
    results = response.json().get('organic_results', [])
    
    leads = []
    for result in results[:count]:
        # Extract from title/snippet
        title = result.get('title', '')
        snippet = result.get('snippet', '')
        link = result.get('link', '')
        
        # Simple parsing (production mein better)
        name = title.split('-').strip() if '-' in title else "Owner"
        company = industry if industry else "Local Business"
        phone = extract_phone(snippet) or "N/A"
        email = "contact@" + link.split('/') if link else "N/A"[1]
        
        leads.append([name, company, "Owner", phone, email, link])
    
    return leads[:count]
```

**Route update:**
```python
@app.route('/generate', methods=['POST'])
def generate():
    # ... existing code ...
    
    query = f"{city} {industry} owners phone number email"
    leads = generate_real_leads(query, 50)
    
    # Rest same...
```

**YOUR_SERPAPI_KEY_HERE** replace with actual key
