# Deploy to Render.com Free Tier (Without Persistent Disk)

## Important Limitation

⚠️ **Render.com's free tier does NOT support persistent disks.**

This means:
- ❌ SQLite database resets on each deployment
- ❌ Uploaded images are lost
- ❌ All data is temporary

## Solutions

### Option A: Accept Temporary Data (Testing/Demo Only)

If this is just for **testing or demo purposes**, you can deploy as-is:

1. Your app will work fine
2. Users can create accounts and posts
3. **BUT** data will be lost when:
   - App restarts after sleep
   - You push new code
   - Render redeploys

**How to deploy:**
- Follow normal Render deployment steps
- Skip the "Add Disk" step
- Your app works, but data is temporary

### Option B: Upgrade to Render Paid Tier ($7/month)

Get persistent storage with paid tier:
- **Starter Plan**: $7/month
- Includes persistent disk support
- Always-on (no sleep)
- Better performance

### Option C: Use Railway.app Instead (Recommended)

Railway.app includes persistent storage on free tier:
- ✅ $5 free credit/month
- ✅ Persistent storage included
- ✅ Easier setup
- ✅ See DEPLOY_TO_RAILWAY.md

### Option D: Use PostgreSQL on Render Free Tier

Switch from SQLite to PostgreSQL (both free on Render):

**Steps:**

1. **Create PostgreSQL database on Render**
   - New → PostgreSQL
   - Free tier
   - Get connection URL

2. **Update your app** (I can help with this)
   - Modify `app/infrastructure/db.py`
   - Add `psycopg2-binary` to requirements
   - Use DATABASE_URL from environment

3. **Deploy with PostgreSQL**
   - PostgreSQL data persists ✅
   - SQLite replaced with Postgres
   - No disk needed

**Trade-off:** PostgreSQL is more complex than SQLite

## Recommendation

For your blog app, I recommend:

1. **Best for beginners**: Railway.app (see DEPLOY_TO_RAILWAY.md)
   - Has persistent storage on free tier
   - Easiest setup
   - Your code works as-is

2. **Best for testing**: Render free tier without disk
   - Accept temporary data
   - Good for demos
   - Upgrade later if needed

3. **Best for production**: Render paid tier or PostgreSQL
   - Real persistent storage
   - Better reliability
   - Worth $7/month if serious

## Which Should You Choose?

**Choose Railway.app if:**
- ✅ You want free persistent storage
- ✅ You want easiest deployment
- ✅ Your code should work as-is

**Choose Render free (no disk) if:**
- ✅ Just testing/learning
- ✅ Don't care about data persistence
- ✅ Will upgrade later

**Choose Render paid if:**
- ✅ Want production-quality hosting
- ✅ Can afford $7/month
- ✅ Need reliable storage

## My Recommendation

**Use Railway.app** - It's perfect for your needs:
- Free persistent storage
- Easier than Render
- No compromises
- See DEPLOY_TO_RAILWAY.md for quick setup

---

Want me to help you deploy to Railway instead? It takes only 2-3 minutes!
