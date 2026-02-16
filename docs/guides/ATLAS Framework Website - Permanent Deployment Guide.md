# ATLAS Framework Website - Permanent Deployment Guide

This guide provides step-by-step instructions for deploying the ATLAS Framework website to permanent hosting.

---

## 🎯 Deployment Options

### Option 1: GitHub Pages (Recommended - Free)
### Option 2: Netlify (Easy - Free)
### Option 3: Vercel (Fast - Free)
### Option 4: Custom Server (Full Control)

---

## 🚀 Option 1: GitHub Pages (Recommended)

GitHub Pages provides free, reliable hosting with automatic SSL and custom domain support.

### Step 1: Create GitHub Repository

```bash
# Navigate to the website directory
cd ATLAS_Website_Docs

# Initialize git repository
git init
git add .
git commit -m "Initial commit: ATLAS Framework documentation"

# Create a new repository on GitHub:
# - Go to https://github.com/new
# - Name: atlas-framework-docs (or atlas-framework.github.io for user site)
# - Make it public
# - Do NOT initialize with README

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/atlas-framework-docs.git
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. The workflow in `.github/workflows/deploy.yml` will automatically deploy

### Step 3: Access Your Site

Your site will be available at:
- **User site**: `https://YOUR_USERNAME.github.io/`
- **Project site**: `https://YOUR_USERNAME.github.io/atlas-framework-docs/`

### Step 4: Add Custom Domain (Optional)

1. Purchase a domain (e.g., atlas-framework.org)
2. Add DNS records:
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   
   Type: A
   Name: @
   Value: 185.199.109.153
   
   Type: A
   Name: @
   Value: 185.199.110.153
   
   Type: A
   Name: @
   Value: 185.199.111.153
   
   Type: CNAME
   Name: www
   Value: YOUR_USERNAME.github.io
   ```
3. In GitHub repository settings → Pages:
   - Enter your custom domain
   - Enable "Enforce HTTPS"
4. Update `CNAME` file in repository root:
   ```bash
   echo "atlas-framework.org" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

---

## 🌐 Option 2: Netlify

Netlify offers easy deployment with continuous integration.

### Step 1: Build the Site

```bash
cd ATLAS_Website_Docs
mkdocs build
```

### Step 2: Deploy to Netlify

**Method A: Drag and Drop**

1. Go to https://app.netlify.com/drop
2. Drag the `site/` folder to the upload area
3. Your site is live!

**Method B: Git Integration**

1. Push your code to GitHub (see Option 1, Step 1)
2. Go to https://app.netlify.com/
3. Click "New site from Git"
4. Connect your GitHub repository
5. Configure build settings:
   - **Build command**: `mkdocs build`
   - **Publish directory**: `site`
6. Click "Deploy site"

### Step 3: Custom Domain

1. In Netlify dashboard → Domain settings
2. Click "Add custom domain"
3. Follow DNS configuration instructions
4. SSL is automatically provisioned

---

## ⚡ Option 3: Vercel

Vercel provides ultra-fast global CDN deployment.

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy

```bash
cd ATLAS_Website_Docs

# Build the site
mkdocs build

# Deploy
vercel --prod
```

### Step 3: Git Integration

1. Push your code to GitHub
2. Go to https://vercel.com/
3. Click "Import Project"
4. Select your repository
5. Configure:
   - **Build command**: `pip install mkdocs mkdocs-material pymdown-extensions mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin && mkdocs build`
   - **Output directory**: `site`
6. Deploy

### Step 4: Custom Domain

1. In Vercel dashboard → Domains
2. Add your custom domain
3. Follow DNS configuration
4. SSL is automatic

---

## 🖥️ Option 4: Custom Server

Deploy to your own server with Docker or direct installation.

### Docker Deployment

```bash
# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install mkdocs mkdocs-material pymdown-extensions mkdocs-minify-plugin mkdocs-git-revision-date-localized-plugin

# Copy website files
COPY . .

# Build site
RUN mkdocs build

# Serve with Python HTTP server
CMD ["python", "-m", "http.server", "8000", "--directory", "site"]

EXPOSE 8000
EOF

# Build and run
docker build -t atlas-docs .
docker run -d -p 80:8000 --name atlas-docs atlas-docs
```

### Nginx Deployment

```bash
# Build the site
mkdocs build

# Copy to web root
sudo cp -r site/* /var/www/html/

# Configure Nginx
sudo nano /etc/nginx/sites-available/atlas-framework

# Add configuration:
server {
    listen 80;
    server_name atlas-framework.org www.atlas-framework.org;
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/atlas-framework /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Add SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d atlas-framework.org -d www.atlas-framework.org
```

---

## 🔄 Continuous Deployment

### GitHub Actions (Already Configured)

The `.github/workflows/deploy.yml` file automatically:
- Builds the site on every push to `main`
- Deploys to GitHub Pages
- Runs on pull requests for testing

### Netlify/Vercel Auto-Deploy

Both platforms automatically deploy when you push to your repository.

---

## 🔒 Security & Performance

### Enable HTTPS

All recommended platforms provide automatic HTTPS:
- **GitHub Pages**: Automatic with custom domains
- **Netlify**: Automatic SSL provisioning
- **Vercel**: Automatic SSL provisioning
- **Custom Server**: Use Let's Encrypt (see Nginx example)

### Performance Optimization

The site is already optimized with:
- ✅ Minified HTML/CSS/JS (via mkdocs-minify-plugin)
- ✅ Optimized images
- ✅ CDN delivery (Mermaid.js from jsDelivr)
- ✅ Responsive design
- ✅ Lazy loading

### Additional Optimizations

```yaml
# Add to mkdocs.yml for better performance
plugins:
  - search
  - minify:
      minify_html: true
      minify_js: true
      minify_css: true
      htmlmin_opts:
        remove_comments: true
  - optimize:
      enabled: true
      cache: true
```

---

## 📊 Monitoring & Analytics

### Add Google Analytics

```html
<!-- Add to overrides/main.html -->
{% block analytics %}
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  </script>
{% endblock %}
```

### Add Plausible Analytics (Privacy-Friendly)

```html
<!-- Add to overrides/main.html -->
{% block analytics %}
  <script defer data-domain="atlas-framework.org" src="https://plausible.io/js/script.js"></script>
{% endblock %}
```

---

## 🧪 Testing Deployment

### Test Locally

```bash
# Serve locally
mkdocs serve

# Access at http://localhost:8000
```

### Test Production Build

```bash
# Build
mkdocs build

# Serve production build
cd site
python -m http.server 8000

# Access at http://localhost:8000
```

### Validate Links

```bash
# Install link checker
pip install linkchecker

# Check all links
linkchecker http://localhost:8000
```

---

## 🆘 Troubleshooting

### Build Fails

**Issue**: MkDocs build fails

**Solution**:
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check for syntax errors in mkdocs.yml
mkdocs build --strict
```

### 404 Errors

**Issue**: Pages return 404

**Solution**:
- Check file paths in `mkdocs.yml` navigation
- Ensure all linked files exist in `docs/` directory
- Verify base URL in `mkdocs.yml`

### Mermaid Diagrams Not Rendering

**Issue**: Diagrams don't appear

**Solution**:
- Verify `overrides/main.html` includes Mermaid.js script
- Check browser console for errors
- Ensure diagrams use correct syntax

---

## 📝 Maintenance

### Update Content

```bash
# Edit documentation files
nano docs/path/to/file.md

# Commit and push
git add .
git commit -m "Update documentation"
git push

# Automatic deployment via GitHub Actions/Netlify/Vercel
```

### Update Dependencies

```bash
# Update MkDocs and plugins
pip install --upgrade mkdocs mkdocs-material pymdown-extensions

# Test locally
mkdocs serve

# Commit updated requirements
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## ✅ Deployment Checklist

- [ ] Repository created on GitHub
- [ ] GitHub Actions workflow configured
- [ ] Site builds successfully locally
- [ ] All links validated
- [ ] Mermaid diagrams render correctly
- [ ] Custom domain configured (if applicable)
- [ ] HTTPS enabled
- [ ] Analytics added (optional)
- [ ] Favicon added
- [ ] Social media meta tags configured
- [ ] Search functionality tested
- [ ] Mobile responsiveness verified
- [ ] Performance optimized
- [ ] Backup strategy in place

---

## 🎉 Success!

Your ATLAS Framework website is now permanently deployed and accessible to the world!

**Next Steps**:
1. Share the URL with your team
2. Add content and documentation
3. Monitor analytics
4. Gather feedback
5. Iterate and improve

For questions or issues, open an issue on GitHub or contact the ATLAS team.
