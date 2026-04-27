from flask import Flask, request, send_file
import csv, io, sqlite3
from datetime import date

app = Flask(__name__)

# Database
import sqlite3
conn = sqlite3.connect('leads.db')
conn.execute('CREATE TABLE IF NOT EXISTS users (phone TEXT PRIMARY KEY, used INTEGER DEFAULT 0)')

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html><head><title>YourDomain Leads</title>
<style>body{font-family:sans-serif;max-width:500px;margin:auto;padding:40px;background:#f0f4f8;}
.hero{background:linear-gradient(45deg,#4f46e5,#7c3aed);color:white;padding:40px;border-radius:20px;text-align:center;}
input,select,button{width:100%;padding:15px;margin:10px 0;border:none;border-radius:10px;font-size:16px;box-shadow:0 4px 12px rgba(0,0,0,0.1);}
button{background:#10b981;color:white;cursor:pointer;font-weight:bold;}
</style></head>
<body>
<div class="hero">
<h1>🚀 Verified B2B Leads</h1>
<p>Lucknow | Kanpur | Daily Fresh Leads</p>
</div>
<form method="post" action="/leads">
<input type="tel" name="phone" placeholder="📱 Phone Number" required>
<select name="industry">
<option>Real Estate</option><option>Retail</option><option>Healthcare</option><option>Services</option>
</select>
<input type="text" name="city" value="Lucknow" placeholder="City">
<button>Generate 50 Leads ➤</button>
</form>
<p style="text-align:center;color:#666;">Free trial: 5 leads | Pro: ₹499/mo 50 leads</p>
</body></html>
    '''

@app.route('/leads', methods=['POST'])
def leads():
    phone = request.form['phone']
    
    # Check quota
    cursor = conn.cursor()
    cursor.execute("SELECT used FROM users WHERE phone=?", (phone,))
    result = cursor.fetchone()
    used = result[0] if result else 0
    
    if used >= 50:
        return "❌ Daily 50 leads limit reached. Kal new leads!"
    
    # Generate demo leads (Real Google SERP later)
    leads_data = [
        ['Raj Sharma', 'ABC Realty', 'Owner', '9876543210', 'raj@abc.com', 'linkedin.com/in/raj'],
        ['Priya Singh', 'XYZ Properties', 'Manager', '9123456789', 'priya@xyz.com', 'linkedin.com/in/priya'],
        ['Amit Gupta', 'Modern Homes', 'Director', '9988776655', 'amit@modern.com', 'linkedin.com/in/amitg'],
    ][:5-used]  # Free trial limit
    
    # Save usage
    cursor.execute("INSERT OR REPLACE INTO users (phone, used) VALUES (?, ?)", (phone, used+len(leads_data)))
    conn.commit()
    
    # CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Company', 'Designation', 'Mobile', 'Email', 'LinkedIn'])
    writer.writerows(leads_data)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'fresh_leads_{phone[-4:]}.csv'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
