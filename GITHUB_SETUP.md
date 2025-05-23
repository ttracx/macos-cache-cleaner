# GitHub Setup Instructions

Your macOS Cache Cleaner project is ready to push to GitHub! Here's how to complete the setup:

## 🔐 Authentication Required

Since you're getting a 403 error, you need to authenticate with GitHub using one of these methods:

### Option 1: Personal Access Token (Recommended)

1. **Create a Personal Access Token:**
   - Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (full repository access)
   - Copy the generated token

2. **Use the token for push:**
   ```bash
   cd /Users/knightdev/macos-cache-cleaner
   git remote set-url origin https://YOUR_TOKEN@github.com/ttracx/macos-cache-cleaner.git
   git push -u origin main
   ```

### Option 2: GitHub CLI (Easiest)

1. **Install GitHub CLI:**
   ```bash
   brew install gh
   ```

2. **Authenticate and push:**
   ```bash
   cd /Users/knightdev/macos-cache-cleaner
   gh auth login
   git push -u origin main
   ```

### Option 3: SSH Key

1. **Generate SSH key:**
   ```bash
   ssh-keygen -t ed25519 -C "mail@tommytracx.com"
   ```

2. **Add to GitHub:**
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - Add to GitHub.com → Settings → SSH and GPG keys

3. **Update remote and push:**
   ```bash
   cd /Users/knightdev/macos-cache-cleaner
   git remote set-url origin git@github.com:ttracx/macos-cache-cleaner.git
   git push -u origin main
   ```

## 📦 What Will Be Pushed

Your repository contains:
- ✅ Complete cache cleaning utility (CLI + GUI)
- ✅ Professional app icon and macOS bundle
- ✅ Comprehensive documentation
- ✅ Installation scripts
- ✅ MIT License
- ✅ All files properly attributed to Tommy Xaypanya (@ttracx)

## 🎯 After Successful Push

Once pushed, consider:

1. **Add a release:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Update repository settings:**
   - Description: "🧹 Professional macOS cache & temp file cleaner with GUI - Free up disk space safely"
   - Topics: `macos`, `cache-cleaner`, `disk-space`, `python`, `gui`, `system-utility`
   - Website: `https://tommytracx.com`

3. **Create a release on GitHub:**
   - Go to Releases → Create new release
   - Tag: v1.0.0
   - Title: "macOS Cache Cleaner v1.0.0"
   - Upload the app bundle as an asset

## 🚀 Repository URL

Your repository: https://github.com/ttracx/macos-cache-cleaner

Choose the authentication method that works best for you and run the commands above!