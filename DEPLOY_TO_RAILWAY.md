# Deploy to Railway.app - Quick Guide

Railway.app is **perfect for your blog** because:
- ✅ $5 free credit monthly (enough for ~500 hours)
- ✅ **Persistent storage included** (no extra setup needed!)
- ✅ Auto-detects Python apps
- ✅ GitHub auto-deploy
- ✅ Fastest deployment (2-3 minutes)

## Step-by-Step Deployment

### Step 1: Sign Up

1. Go to https://railway.app
2. Click **"Login"**
3. Sign in with your **GitHub account**
4. Authorize Railway to access your repositories

### Step 2: Create New Project

1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Search for and select: `siarheistar/fastapi-blog-app`
4. Click on the repository

### Step 3: Configure (Automatic!)

Railway automatically:
- ✅ Detects it's a Python app
- ✅ Reads your `Procfile`
- ✅ Installs from `requirements.txt`
- ✅ Sets up persistent storage
- ✅ Assigns a public URL

**No manual configuration needed!**

### Step 4: Deploy

1. Railway starts building automatically
2. Watch the deployment logs
3. Wait 2-3 minutes
4. Done! 🎉

### Step 5: Get Your URL

1. Click on your deployed service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"** section
4. Click **"Generate Domain"**
5. Your app will be at: `https://your-app.up.railway.app`

## Persistent Storage

**Good news!** Railway automatically provides persistent storage:
- SQLite database persists between deployments
- Uploaded images are saved
- No extra configuration needed
- Works on free tier!

The `app_data/` directory is automatically persistent.

## Environment Variables (Optional)

If you want to add custom settings:

1. Click on your service
2. Go to **"Variables"** tab
3. Add variables:
   ```
   ENVIRONMENT=production
   ```

## Free Tier Details

| Feature | Free Tier |
|---------|-----------|
| Credit | $5/month |
| Usage | ~500 hours |
| Storage | Persistent ✅ |
| Deploy Time | 2-3 minutes |
| Auto-deploy | Yes ✅ |

**Important:** After you use your $5 credit, the service pauses until next month.

## Monitor Your Usage

1. Go to Railway dashboard
2. Click **"Usage"** in sidebar
3. See remaining credit
4. Monitor hours used

## Upgrade Options

If you need more:
- **Hobby Plan**: $5/month for 100 hours
- **Pro Plan**: $20/month for unlimited usage

## Troubleshooting

### Service won't start

Check the logs:
1. Click on your service
2. Go to **"Deployments"** tab
3. Click latest deployment
4. View logs for errors

### Database not persisting

Railway automatically persists `/app_data`:
- Ensure your database is in `app_data/` directory
- This is already configured in your app ✅

### Need to redeploy

Railway auto-deploys on git push, but to manually redeploy:
1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Select **"Redeploy"**

## Auto-Deploy from GitHub

Every time you push to GitHub:
```bash
git add .
git commit -m "Update blog"
git push origin main
```

Railway automatically:
1. Detects the push
2. Builds your app
3. Deploys the new version
4. Keeps your data intact ✅

## Comparison: Railway vs Render

| Feature | Railway | Render Free |
|---------|---------|-------------|
| Free Tier | $5 credit | 750 hours |
| Persistent Storage | ✅ Included | ❌ Paid only |
| Setup Time | 2 minutes | 5 minutes |
| Auto-deploy | ✅ Yes | ✅ Yes |
| Sleep/Wake | After credit runs out | After 15 min idle |

**For your blog app, Railway is better** because of persistent storage on free tier!

## Your App URLs

After deployment, your blog will be live at:
```
https://fastapi-blog-app.up.railway.app
```

Share this URL with friends and start blogging! 🚀

## Support

- **Railway Docs**: https://docs.railway.app
- **Discord**: https://discord.gg/railway
- **GitHub Issues**: https://github.com/siarheistar/fastapi-blog-app/issues

---

**Ready to deploy?** Follow the steps above - takes only 2-3 minutes! ⚡
