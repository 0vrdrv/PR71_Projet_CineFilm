"""
Seed script to populate letterboxd.db with realistic data.
Run from /home/user/letterbox/backend/
"""
import sqlite3
import random
import datetime

conn = sqlite3.connect("letterboxd.db")
c = conn.cursor()

# Create missing tables
c.execute("""
CREATE TABLE IF NOT EXISTS watched (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    tmdb_id INTEGER,
    movie_title VARCHAR,
    poster_path VARCHAR,
    watched_at DATETIME,
    rewatch BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    tmdb_id INTEGER,
    movie_title VARCHAR,
    poster_path VARCHAR,
    rank INTEGER,
    added_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
conn.commit()

# ============================================================
# REAL TMDB MOVIE DATA (real IDs, real poster paths)
# ============================================================
MOVIES = [
    (278, "The Shawshank Redemption", "/9cjIGRtkTcHAdtWNOOSaiVKlW0F.jpg"),
    (238, "The Godfather", "/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"),
    (240, "The Godfather Part II", "/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg"),
    (424, "Schindler's List", "/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg"),
    (389, "12 Angry Men", "/ow3wq89wM8qd5X7hWKGecRhm28d.jpg"),
    (19404, "Dilwale Dulhania Le Jayenge", "/2CAL2433ZeIihfX1Hb2139CX0pW.jpg"),
    (129, "Spirited Away", "/39wmItIWsg5sZMyRUHLkWBcuVCM.jpg"),
    (155, "The Dark Knight", "/qJ2tW6WMUDux911ma7PaECWR3Li.jpg"),
    (550, "Fight Club", "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"),
    (680, "Pulp Fiction", "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"),
    (13, "Forrest Gump", "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg"),
    (122, "The Lord of the Rings: The Return of the King", "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg"),
    (497, "The Green Mile", "/8VG8fDNiy50H4FedGwdSVUPoaJe.jpg"),
    (372058, "Your Name.", "/q719jXXEzOoYaps6babgKnONONX.jpg"),
    (637, "Life Is Beautiful", "/74hLDKjD5aGYOotO6esUVaeISa2.jpg"),
    (324857, "Spider-Man: Into the Spider-Verse", "/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg"),
    (346, "Seven", "/6yoghtyTpznpBik8EngEmJskVUO.jpg"),
    (120, "The Lord of the Rings: The Fellowship of the Ring", "/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg"),
    (510, "One Flew Over the Cuckoo's Nest", "/3jcbDmRFiQ83drXNOvRDeKHxS0C.jpg"),
    (1891, "The Empire Strikes Back", "/nNAeTmF4CtdSgMDplXTDPOpYzsX.jpg"),
    (27205, "Inception", "/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg"),
    (603, "The Matrix", "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"),
    (569094, "Spider-Man: Across the Spider-Verse", "/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg"),
    (671, "Harry Potter and the Philosopher's Stone", "/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg"),
    (157336, "Interstellar", "/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"),
    (244786, "Whiplash", "/oPxnRhyAIzJKEUzEnS1MiIBfYiE.jpg"),
    (620, "Ghostbusters", "/rPlBf9uyUbOqJPlaGmOvIRNBjjt.jpg"),
    (429, "The Good, the Bad and the Ugly", "/bX2xnavhMYjWDoZp1VM6VnU1xwe.jpg"),
    (274, "The Silence of the Lambs", "/uS9m8OBk1RVfRPvLhxKx0Oss6hk.jpg"),
    (11, "Star Wars", "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg"),
    (872585, "Oppenheimer", "/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"),
    (346698, "Barbie", "/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg"),
    (76600, "Avatar: The Way of Water", "/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"),
    (438631, "Dune", "/d5NXSklXo0qyIYkgV94XAgMIckC.jpg"),
    (693134, "Dune: Part Two", "/8b8R8l88Qje9dn9OE8PY05Nez7H.jpg"),
    (299536, "Avengers: Infinity War", "/7WsyChQLEftFiDhRkKUOHQjyqWH.jpg"),
    (299534, "Avengers: Endgame", "/or06FN3Dka5tukK1e9sl16pB3iy.jpg"),
    (533535, "Deadpool & Wolverine", "/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg"),
    (1184918, "The Wild Robot", "/wTnV3PCVW5O92JMrFvvrRcV39RU.jpg"),
    (786892, "Furiosa: A Mad Max Saga", "/iADOJ8Zymht2JPMoy3R7xceZprc.jpg"),
    (823464, "Godzilla x Kong: The New Empire", "/z1p34vh7dEOnLDmyCrlUVLuoDzd.jpg"),
    (573435, "Bad Boys: Ride or Die", "/nP6RliHjxsz4irTKsxe8FRhKZYl.jpg"),
    (748783, "The Garfield Movie", "/p6AbOJvMQhBmffd0PIv0u8ghWeY.jpg"),
    (1022789, "Inside Out 2", "/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg"),
    (653346, "Kingdom of the Planet of the Apes", "/gKkl37BQuKTanygYQG1pyYgLVgf.jpg"),
    (1011985, "Kung Fu Panda 4", "/kDp1vUBnMpe8ak4rjgl3cLELqjU.jpg"),
    (945961, "Alien: Romulus", "/b33nnKl1GSFbao4l3fZDDqsMSF6.jpg"),
    (519182, "Despicable Me 4", "/wWba3TaojhK7NdycRhoQpsG0FaH.jpg"),
    (1087822, "Moana 2", "/yh64qw9mgXBvlaWDi7Q9tpUBAvH.jpg"),
    (762441, "A Quiet Place: Day One", "/yrpPYKijwdMHyTGIOd1iK1h0Xno.jpg"),
]

# Real reviews
REVIEW_COMMENTS = [
    "A masterpiece that deserves every bit of praise it gets. The acting is phenomenal and the story keeps you on the edge of your seat.",
    "One of the best films I've ever seen. Absolutely stunning cinematography and a soundtrack that gives you chills.",
    "I can see why this is so highly rated, but it didn't quite click with me. Still a very solid film though.",
    "Went in with low expectations and was completely blown away. This film has so many layers.",
    "The director really outdid themselves here. Every frame is like a painting.",
    "Not gonna lie, I cried three times during this movie. Emotionally devastating in the best way.",
    "A bit overrated in my opinion, but the performances carry it. The lead actor is incredible.",
    "This is the kind of film you need to watch twice to fully appreciate. So many hidden details.",
    "Beautifully shot and incredibly well-acted. A true cinematic experience.",
    "The pacing was a bit slow in the middle, but the payoff at the end was absolutely worth it.",
    "I watch this every year and it never gets old. A timeless classic.",
    "The script is razor-sharp and the dialogue is endlessly quotable. Pure cinema.",
    "An emotional rollercoaster from start to finish. I've never experienced anything like it in a theater.",
    "The visual effects in this are groundbreaking even by today's standards. A technical marvel.",
    "Not my usual genre but I'm so glad I gave it a chance. What a journey.",
    "The chemistry between the leads is electric. You can't take your eyes off the screen.",
    "Dark, gritty, and absolutely mesmerizing. This redefined what the genre could be.",
    "A feel-good movie that actually feels genuine. No manufactured emotions here.",
    "The twist at the end completely recontextualized everything. Brilliant storytelling.",
    "Honestly one of the most visually stunning films ever made. Every shot is breathtaking.",
    "The score alone makes this worth watching. Hans Zimmer at his absolute best.",
    "A slow burn that rewards patience. The final act is pure perfection.",
    "This film challenged me in ways I didn't expect. Still thinking about it days later.",
    "Perfect casting, perfect direction, perfect story. There's nothing I would change.",
    "The world-building in this is insane. You feel completely immersed from minute one.",
    "An incredible debut that showcases raw, unfiltered talent. Can't wait to see what's next.",
    "Rewatched it for the fifth time and noticed new things. That's the mark of a great film.",
    "The action sequences are jaw-dropping but it's the quiet moments that stay with you.",
    "A love letter to cinema itself. You can feel the passion in every frame.",
    "Exceeded all my expectations. The hype was real for once.",
    "I had chills during the entire third act. Absolutely phenomenal filmmaking.",
    "Simple story told extraordinarily well. Proof that execution is everything.",
    "The villain in this is genuinely terrifying. One of the best antagonists in film history.",
    "A gorgeous animated film with more depth than most live-action movies.",
    "The ending destroyed me. I sat in the theater for ten minutes after the credits rolled.",
    "Funny, touching, and surprisingly deep. A perfect blend of humor and heart.",
    "This film has aged like fine wine. Even better on rewatch twenty years later.",
    "The sound design is incredible. Watch this with good headphones or in a proper theater.",
    "A triumphant piece of filmmaking that proves cinema is far from dead.",
    "Controversial take: this is better than the original. Fight me.",
]

# ============================================================
# USERS DATA
# ============================================================
NEW_USERS = [
    ("CinemaAddict", "cinema@example.com", "Film enthusiast and amateur critic"),
    ("MovieBuff42", "moviebuff@example.com", "I watch too many movies"),
    ("FilmNoir_Fan", "filmnoir@example.com", "Classic cinema lover"),
    ("ReelTalk", "reeltalk@example.com", "Discussing movies one frame at a time"),
    ("PopcornCritic", "popcorn@example.com", "Reviews from the back row"),
    ("ScreenDreamer", "screen@example.com", "Lost in the silver screen"),
    ("CultClassics", "cult@example.com", "B-movies and beyond"),
    ("ArthouseLover", "arthouse@example.com", "Slow cinema enthusiast"),
    ("BlockbusterBro", "blockbuster@example.com", "Big movies, big opinions"),
    ("IndieWatcher", "indie@example.com", "Supporting independent film"),
    ("NightOwlCinema", "nightowl@example.com", "Late night movie marathons"),
    ("FrameByFrame", "frame@example.com", "Analyzing cinema one frame at a time"),
    ("SilverScreen", "silver@example.com", "Golden age of Hollywood fan"),
    ("DirectorsCut", "directors@example.com", "Always watching the extended edition"),
    ("MatineeMaven", "matinee@example.com", "Weekday afternoon screenings are underrated"),
    ("CinemaScopeX", "scope@example.com", "Widescreen is the only way"),
    ("FilmGrain", "grain@example.com", "Analog film preservation advocate"),
]

LIST_TEMPLATES = [
    ("Best Sci-Fi Films of All Time", "A curated collection of the greatest science fiction movies ever made."),
    ("Movies That Will Make You Cry", "Prepare tissues before watching any of these emotional masterpieces."),
    ("Perfect Date Night Films", "Romantic, funny, and guaranteed to impress."),
    ("Mind-Bending Thrillers", "Films that will keep you guessing until the very last frame."),
    ("Comfort Movies for Rainy Days", "The cinematic equivalent of a warm blanket and hot chocolate."),
    ("Visually Stunning Masterpieces", "Films where every frame could be a painting."),
    ("Hidden Gems You Probably Missed", "Underrated films that deserve way more attention."),
    ("Essential 2024 Watchlist", "The must-see films from last year."),
    ("Directors' Best Work", "The defining film of each legendary director's career."),
    ("Films That Changed Cinema", "Revolutionary movies that shaped the art form."),
    ("Best Animated Films Ever", "Animation is cinema. Here's the proof."),
    ("Sequels Better Than the Original", "Rare but they exist. Here are the best ones."),
    ("Perfect First Dates Movies", "Light, fun, and great conversation starters."),
    ("Horror Films for Beginners", "Not too scary, but still thrilling. A gentle introduction."),
    ("Oscar Snubs That Deserved Better", "The Academy got it wrong with these."),
]

now = datetime.datetime.utcnow()

def random_date(days_back=365):
    return now - datetime.timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

# ============================================================
# 1. CREATE NEW USERS
# ============================================================
print("Creating users...")
# Reuse existing bcrypt hash from user 1 (password doesn't matter for seed data)
hashed = "$2b$12$DglUtLs2NMzVHeRdqBIr2OG6bTR8Z5kC1e0GWGVwgBLAtj3L1w2fW"

for username, email, bio in NEW_USERS:
    c.execute("INSERT INTO users (username, email, hashed_password, bio) VALUES (?, ?, ?, ?)",
              (username, email, hashed, bio))
conn.commit()

c.execute("SELECT id, username FROM users")
all_users = c.fetchall()
user_ids = [u[0] for u in all_users]
print(f"  Total users: {len(all_users)}")

# ============================================================
# 2. CREATE FOLLOWS (rich social graph)
# ============================================================
print("Creating follows...")
follow_count = 0
for uid in user_ids:
    # Each user follows 5-12 random other users
    targets = random.sample([u for u in user_ids if u != uid], min(random.randint(5, 12), len(user_ids) - 1))
    for target in targets:
        try:
            c.execute("INSERT INTO follows (follower_id, followed_id, created_at) VALUES (?, ?, ?)",
                      (uid, target, random_date(180).isoformat()))
            follow_count += 1
        except:
            pass
conn.commit()
print(f"  Follows created: {follow_count}")

# ============================================================
# 3. CREATE REVIEWS (lots of them)
# ============================================================
print("Creating reviews...")
review_count = 0
review_id_start = 100

for uid in user_ids:
    # Each user reviews 8-20 random movies
    num_reviews = random.randint(8, 20)
    reviewed_movies = random.sample(MOVIES, min(num_reviews, len(MOVIES)))

    for tmdb_id, title, poster in reviewed_movies:
        rating = random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 3, 3.5, 4, 4, 4.5, 5, 5])
        comment = random.choice(REVIEW_COMMENTS) if random.random() > 0.15 else None
        has_spoilers = random.random() < 0.1
        watch_date = random_date(300)

        c.execute("""INSERT INTO reviews (tmdb_id, movie_title, rating, comment, has_spoilers, watch_date, created_at, user_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                  (tmdb_id, title, rating, comment, has_spoilers, watch_date.isoformat(), watch_date.isoformat(), uid))
        review_count += 1

conn.commit()
print(f"  Reviews created: {review_count}")

# ============================================================
# 4. CREATE REVIEW LIKES
# ============================================================
print("Creating review likes...")
c.execute("SELECT id FROM reviews")
all_review_ids = [r[0] for r in c.fetchall()]

like_count = 0
for uid in user_ids:
    # Each user likes 10-30 random reviews
    liked = random.sample(all_review_ids, min(random.randint(10, 30), len(all_review_ids)))
    for rid in liked:
        try:
            c.execute("INSERT INTO review_likes (user_id, review_id) VALUES (?, ?)", (uid, rid))
            like_count += 1
        except:
            pass
conn.commit()
print(f"  Likes created: {like_count}")

# ============================================================
# 5. CREATE WATCHED ENTRIES
# ============================================================
print("Creating watched entries...")
watched_count = 0
for uid in user_ids:
    num = random.randint(12, 35)
    watched_movies = random.sample(MOVIES, min(num, len(MOVIES)))
    for tmdb_id, title, poster in watched_movies:
        c.execute("""INSERT INTO watched (user_id, tmdb_id, movie_title, poster_path, watched_at, rewatch)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (uid, tmdb_id, title, poster, random_date(365).isoformat(), random.random() < 0.15))
        watched_count += 1
conn.commit()
print(f"  Watched entries: {watched_count}")

# ============================================================
# 6. CREATE WATCHLIST ENTRIES
# ============================================================
print("Creating watchlist entries...")
wl_count = 0
for uid in user_ids:
    num = random.randint(3, 12)
    wl_movies = random.sample(MOVIES, min(num, len(MOVIES)))
    for tmdb_id, title, poster in wl_movies:
        c.execute("""INSERT INTO watchlist (tmdb_id, movie_title, poster_path, user_id, added_at)
                     VALUES (?, ?, ?, ?, ?)""",
                  (tmdb_id, title, poster, uid, random_date(90).isoformat()))
        wl_count += 1
conn.commit()
print(f"  Watchlist entries: {wl_count}")

# ============================================================
# 7. CREATE FAVORITES (4 per user)
# ============================================================
print("Creating favorites...")
fav_count = 0
for uid in user_ids:
    fav_movies = random.sample(MOVIES, 4)
    for rank, (tmdb_id, title, poster) in enumerate(fav_movies, 1):
        c.execute("""INSERT INTO favorites (user_id, tmdb_id, movie_title, poster_path, rank, added_at)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (uid, tmdb_id, title, poster, rank, random_date(60).isoformat()))
        fav_count += 1
conn.commit()
print(f"  Favorites created: {fav_count}")

# ============================================================
# 8. CREATE MOVIE LISTS
# ============================================================
print("Creating movie lists...")
list_count = 0
existing_list_ids = []
c.execute("SELECT MAX(id) FROM movie_lists")
max_list_id = c.fetchone()[0] or 0

for uid in user_ids:
    # Each user creates 1-3 lists
    num_lists = random.randint(1, 3)
    user_lists = random.sample(LIST_TEMPLATES, min(num_lists, len(LIST_TEMPLATES)))
    for title, desc in user_lists:
        c.execute("""INSERT INTO movie_lists (title, description, is_public, created_at, user_id)
                     VALUES (?, ?, ?, ?, ?)""",
                  (title, desc, True, random_date(120).isoformat(), uid))
        existing_list_ids.append(c.lastrowid)
        list_count += 1
conn.commit()
print(f"  Lists created: {list_count}")

# ============================================================
# 9. ADD ITEMS TO LISTS
# ============================================================
print("Adding items to lists...")
item_count = 0
for list_id in existing_list_ids:
    num_items = random.randint(4, 12)
    list_movies = random.sample(MOVIES, min(num_items, len(MOVIES)))
    for rank, (tmdb_id, title, poster) in enumerate(list_movies, 1):
        c.execute("""INSERT INTO movie_list_items (list_id, tmdb_id, movie_title, poster_path, rank)
                     VALUES (?, ?, ?, ?, ?)""",
                  (list_id, tmdb_id, title, poster, rank))
        item_count += 1
conn.commit()
print(f"  List items added: {item_count}")

# ============================================================
# FINAL STATS
# ============================================================
print("\n=== FINAL DATABASE STATS ===")
for table in ["users", "follows", "reviews", "review_likes", "watched", "watchlist", "favorites", "movie_lists", "movie_list_items"]:
    c.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"  {table}: {c.fetchone()[0]} rows")

conn.close()
print("\nDone! Database populated successfully.")

