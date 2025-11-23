# Quick Deployment Guide

## TL;DR - Deploy in 3 Minutes

### ⚠️ GitHub Pages Won't Work
Your app needs Python/FastAPI backend. GitHub Pages only hosts static HTML.

### ✅ Best Option: Railway.app

**Why Railway?**
- ✅ **Persistent storage on FREE tier** (Render free tier doesn't have this!)
- ✅ $5 free credit monthly (~500 hours)
- ✅ Auto-detects your app
- ✅ 2-3 minute deployment

**Quick Steps:**

1. Go to https://railway.app
2. Login with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select `siarheistar/fastapi-blog-app`
5. Click "Deploy"
6. Generate domain in Settings
7. Done! 🎉

**Full guide:** See [DEPLOY_TO_RAILWAY.md](DEPLOY_TO_RAILWAY.md)

### ⚠️ Render.com Free Tier Issue

**Problem:** Render.com FREE tier does NOT support persistent disks (see screenshot you shared)

**This means:**
- ❌ Database resets on each deployment
- ❌ Uploaded images disappear
- ❌ All user data is lost

**Options:**
1. **Use Railway instead** (has persistent storage free) ← Recommended
2. **Upgrade to Render paid** ($7/month for persistent disk)
3. **Use Render free** for testing only (accept data loss)
4. **Switch to PostgreSQL** on Render (more complex)

**See:** [RENDER_FREE_TIER_WORKAROUND.md](RENDER_FREE_TIER_WORKAROUND.md)

## Comparison Table

| Platform | Free Tier | Persistent Storage | Setup Time | Best For |
|----------|-----------|-------------------|------------|----------|
| **Railway.app** ⭐ | $5 credit | ✅ **Yes!** | 2 min | **You!** |
| Render.com Free | 750 hrs | ❌ **No** | 5 min | Testing only |
| Render.com Paid | N/A | ✅ Yes | 5 min | Production |
| Fly.io | 3 VMs | ✅ Yes | 10 min | Docker users |

## My Recommendation

**Use Railway.app** because:
1. Persistent storage on free tier (unlike Render)
2. Easiest deployment
3. Your code works as-is
4. No compromises

## Deployment Guides

- **Railway** (Recommended): [DEPLOY_TO_RAILWAY.md](DEPLOY_TO_RAILWAY.md)
- **Render with workarounds**: [RENDER_FREE_TIER_WORKAROUND.md](RENDER_FREE_TIER_WORKAROUND.md)
- **Render detailed**: [DEPLOY_TO_RENDER.md](DEPLOY_TO_RENDER.md)
- **All platforms**: [DEPLOYMENT.md](DEPLOYMENT.md)

## Need Help?

Open an issue: https://github.com/siarheistar/fastapi-blog-app/issues

---

**Ready?** Start with Railway: https://railway.app 🚀
