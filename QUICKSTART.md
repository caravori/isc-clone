# Quick Start Guide - ISC Clone

## Get Started in 5 Minutes

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/caravori/isc-clone.git
cd isc-clone

# 2. Create and activate virtual environment
python -m venv venv

# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser account
python manage.py createsuperuser
# Follow prompts to create admin account

# 7. Create static directory
mkdir static

# 8. Start development server
python manage.py runserver
```

### Access Your Application

- **Homepage**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Blog**: http://localhost:8000/blog/
- **Threat Dashboard**: http://localhost:8000/threats/
- **RSS Feed**: http://localhost:8000/blog/feed/rss/

### First Steps After Installation

1. **Login to Admin Panel**
   - Go to http://localhost:8000/admin
   - Use superuser credentials

2. **Configure Site Settings**
   - Navigate to Core → Site Settings
   - Update site name and description
   - Set InfoCon status

3. **Create Blog Categories**
   - Go to Blog → Categories
   - Add categories like:
     - Handler Diary
     - Security Analysis
     - Threat Intelligence
     - Incident Response

4. **Create Your First Post**
   - Go to Blog → Posts → Add Post
   - Write content using rich text editor
   - Select category and add tags
   - Change status to "Published"
   - Save

5. **Add Threat Data (Optional)**
   - Threats → Port Activities
   - Threats → IP Reputations
   - Threats → Threat Indicators

### ISSN Configuration

To make your publication ISSN-compliant:

1. Apply for ISSN at https://www.issn.org/
2. Once assigned, edit `.env` file:
   ```
   ISSN_NUMBER=1234-5678
   ISSN_L=1234-5678
   PUBLISHER_NAME=Your Organization
   PUBLISHER_COUNTRY=US
   ```
3. Restart server: `python manage.py runserver`

### Common Commands

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Start development server
python manage.py runserver

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

### Project Structure Overview

```
isc-clone/
├── isc_project/        # Main Django project
│   ├── settings.py    # Configuration
│   └── urls.py        # URL routing
├── core/              # Core functionality
│   ├── models.py      # Site settings, handlers
│   └── views.py       # Homepage, about
├── blog/              # Blog application
│   ├── models.py      # Posts, categories, comments
│   ├── views.py       # Blog views
│   └── feeds.py       # RSS/Atom feeds
├── threats/           # Threat intelligence
│   ├── models.py      # Threats, IPs, ports
│   └── views.py       # Threat dashboard
└── templates/         # HTML templates
```

### Key Features

✅ **Blog System**
- Rich text editor (CKEditor)
- Categories and tags
- Draft/Published status
- Comments
- RSS/Atom feeds

✅ **Threat Intelligence**
- Port activity monitoring
- IP reputation tracking
- Threat indicators (IoCs)
- InfoCon status system

✅ **ISSN Compliance**
- ISSN metadata integration
- Citation formatting
- RSS feeds with ISSN
- Dublin Core tags

### Troubleshooting

**Issue**: `ModuleNotFoundError`
- **Solution**: Ensure virtual environment is activated and dependencies installed

**Issue**: Database errors
- **Solution**: Run `python manage.py migrate`

**Issue**: Static files not loading
- **Solution**: Create `static` directory: `mkdir static`

**Issue**: Admin panel styling broken
- **Solution**: Run `python manage.py collectstatic`

### Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Review [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore the admin panel to familiarize yourself with features

### Need Help?

- 📚 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/caravori/isc-clone/issues)
- 💡 [Request Features](https://github.com/caravori/isc-clone/issues/new)

---

**Happy Coding! 🚀**
