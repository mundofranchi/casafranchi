import instaloader

L = instaloader.Instaloader()
L.load_session_from_file("smartzone.com.ar")  # reemplazá con tu usuario de IG

username = "casafranchi"
posts_to_show = 6

profile = instaloader.Profile.from_username(L.context, username)
posts = list(profile.get_posts())[:posts_to_show]

html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Instagram Feed</title>
  <script async src="//www.instagram.com/embed.js"></script>
</head>
<body>
  <h2 style="text-align:center;">Últimos posts de Instagram</h2>
  <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:20px;">
"""

for post in posts:
    link = f"https://www.instagram.com/p/{post.shortcode}/"
    html += f"""
    <blockquote class="instagram-media" data-instgrm-permalink="{link}" data-instgrm-version="14" style="max-width:300px;"></blockquote>
    """

html += """
  </div>
</body>
</html>
"""

with open("instagram_feed.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Feed generado en instagram_feed.html")
