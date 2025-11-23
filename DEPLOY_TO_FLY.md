# Deploy to Fly.io - Free with Persistent Storage

## Why Fly.io?

✅ **Generous free tier:**
- 3 shared-cpu VMs (256MB RAM each)
- 3GB persistent storage
- 160GB bandwidth/month
- **No credit card required for free tier!**

✅ **Persistent storage included**
- SQLite database persists
- Uploaded images saved
- No data loss

## Prerequisites

- Fly.io account (free)
- Fly CLI installed

## Step 1: Install Fly CLI

**macOS:**
```bash
brew install flyctl
```

**Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

## Step 2: Sign Up & Login

```bash
# Sign up (opens browser)
flyctl auth signup

# Or login if you have account
flyctl auth login
```

## Step 3: Launch Your App

Navigate to your project directory:

```bash
cd /Users/sergei/Projects/test_website

# Launch the app
flyctl launch
```

You'll be prompted with questions:

```
? Choose an app name (leave blank for random): fastapi-blog-app
? Choose a region: [select closest to you]
? Would you like to set up a PostgreSQL database? No
? Would you like to deploy now? No
```

## Step 4: Configure for SQLite

Fly will create `fly.toml`. Update it:

```toml
app = "fastapi-blog-app"
primary_region = "sjc"  # or your chosen region

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256

# Persistent volume for SQLite database
[mounts]
  source = "app_data"
  destination = "/app/app_data"
```

## Step 5: Create Persistent Volume

```bash
# Create 1GB volume for database
flyctl volumes create app_data --size 1 --region sjc
```

(Replace `sjc` with your chosen region)

## Step 6: Deploy!

```bash
flyctl deploy
```

Wait 2-3 minutes for build and deployment.

## Step 7: Open Your App

```bash
flyctl open
```

Your blog is now live at: `https://fastapi-blog-app.fly.dev`

## Managing Your App

**View logs:**
```bash
flyctl logs
```

**Check status:**
```bash
flyctl status
```

**SSH into app:**
```bash
flyctl ssh console
```

**Scale up/down:**
```bash
flyctl scale count 1  # Number of instances
```

## Free Tier Limits

| Resource | Free Tier |
|----------|-----------|
| VMs | 3 x 256MB RAM |
| Storage | 3GB persistent |
| Bandwidth | 160GB/month |
| Cost | **$0 (no credit card!)** |

## Auto-Scaling

Fly automatically:
- Stops machines when idle (saves resources)
- Starts on first request (~2 seconds)
- Scales based on traffic

## Update Your App

Push changes to GitHub, then redeploy:

```bash
git pull origin main
flyctl deploy
```

Or deploy directly from local:

```bash
flyctl deploy
```

## Persistent Data

Your `app_data/` directory persists:
- ✅ SQLite database saved
- ✅ Uploaded images saved  
- ✅ Survives deployments
- ✅ No data loss

## Troubleshooting

### Build fails

Check `fly.toml` configuration and ensure all dependencies are in `requirements.txt`.

### App won't start

View logs:
```bash
flyctl logs
```

### Database not persisting

Ensure volume is mounted:
```bash
flyctl volumes list
```

Should show `app_data` volume.

### Need more resources

Upgrade to paid plan or increase VM size:
```bash
flyctl scale memory 512  # 512MB RAM
```

## Comparison

| Platform | Free Tier | Storage | Setup |
|----------|-----------|---------|-------|
| **Fly.io** | 3 VMs | ✅ 3GB | Medium |
| Railway | Trial expired | ✅ Yes | Easy |
| Render Free | 750 hrs | ❌ No | Easy |

## Cost

Free tier is **completely free** - no credit card needed!

If you exceed free tier:
- ~$2-5/month for small apps
- Pay only for what you use
- Can set spending limits

## Your Blog URLs

After deployment:
```
https://fastapi-blog-app.fly.dev
```

## Support

- **Docs**: https://fly.io/docs
- **Community**: https://community.fly.io
- **GitHub Issues**: https://github.com/siarheistar/fastapi-blog-app/issues

---

**Ready to deploy?** Follow the steps above! ⚡
