# Internet Storm Center Clone

A Django-based clone of the SANS Internet Storm Center with integrated blog functionality and ISSN compliance support.

## Features

### Core ISC Features
- **Handler Diaries**: Daily security analysis posts by handlers
- **Threat Intelligence**: Track and display security threats
- **Port Activity Monitoring**: Display port scan statistics
- **Threat Level System**: InfoCon status indicator
- **IP Reputation Database**: Track malicious IPs

### Blog System
- Full-featured blog with CKEditor rich text editing
- Category and tag support
- Draft/Published/Archived status
- Author management
- SEO-friendly URLs with slugs
- Comment system
- RSS/Atom feeds

### ISSN Compliance
- ISSN metadata integration
- Publisher information display
- Proper citation formatting
- Dublin Core metadata
- RSS feeds with ISSN

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/caravori/isc-clone.git
cd isc-clone

# Start all services
docker-compose up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application at http://localhost:8000
```

**That's it!** Docker Compose will automatically:
- Set up PostgreSQL database
- Configure Redis cache
- Start Django web server
- Launch Celery workers
- Run database migrations

For detailed Docker documentation, see [DOCKER.md](DOCKER.md)

### Manual Installation

## Installation

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)
- PostgreSQL (optional, SQLite by default)
- Redis (for Celery tasks)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/caravori/isc-clone.git
cd isc-clone
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment configuration**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Database setup**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Run development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your ISC clone!

## ISSN Configuration

To make your publication ISSN-compliant:

1. Apply for an ISSN from your national ISSN center: https://www.issn.org/
2. Once assigned, update your `.env` file:
```
ISSN_NUMBER=1234-5678
ISSN_L=1234-5678
PUBLISHER_NAME=Your Organization
PUBLISHER_COUNTRY=US
```

3. The ISSN will appear in:
   - Site header/footer
   - RSS/Atom feeds
   - Post metadata
   - Dublin Core tags

## Project Structure

```
isc-clone/
├── isc_project/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog/                 # Blog application
│   ├── models.py        # Post, Category, Tag models
│   ├── views.py         # Blog views
│   ├── admin.py         # Admin configuration
│   └── templates/       # Blog templates
├── threats/             # Threat intelligence app
│   ├── models.py        # Threat, Port, IP models
│   ├── views.py
│   └── templates/
├── core/                # Core functionality
│   ├── models.py        # Shared models
│   ├── middleware.py
│   └── templates/       # Base templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploads
├── templates/           # Global templates
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose orchestration
└── requirements.txt
```

## Usage

### Admin Interface
Access the admin at `http://localhost:8000/admin/`

- **Blog Posts**: Create handler diaries and articles
- **Threat Data**: Add threat intelligence entries
- **Categories & Tags**: Organize content
- **Users**: Manage handlers/authors

### Creating Handler Diaries
1. Log into admin
2. Go to Blog → Posts → Add Post
3. Select "Handler Diary" category
4. Write your security analysis
5. Publish or save as draft

### Threat Intelligence
1. Go to Threats → Add Threat Entry
2. Enter threat details (IPs, ports, signatures)
3. Link to relevant blog posts

## API Endpoints

- `/api/threats/` - Threat intelligence data (JSON)
- `/api/ports/` - Port activity statistics
- `/api/infocon/` - Current threat level
- `/feed/rss/` - RSS feed with ISSN metadata
- `/feed/atom/` - Atom feed

## Customization

### Branding
Edit `templates/base.html` to customize:
- Site title and logo
- Color scheme
- Navigation

### ISSN Display
Edit `core/templatetags/issn_tags.py` to customize ISSN formatting

### Threat Analysis
Extend `threats/models.py` to add custom threat types

## Deployment

### Docker Compose (Recommended)

Production deployment with Docker:

```bash
# Update environment variables in docker-compose.yml
# Start with Nginx reverse proxy
docker-compose --profile production up -d
```

See [DOCKER.md](DOCKER.md) for complete Docker deployment guide.

### Traditional Deployment

1. Set `DEBUG=False` in `.env`
2. Configure PostgreSQL database
3. Set up Redis for Celery
4. Configure static files serving
5. Use gunicorn as WSGI server
6. Set up nginx reverse proxy
7. Configure SSL certificates

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production setup.

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[DOCKER.md](DOCKER.md)** - Docker Compose deployment guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Traditional production deployment
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

MIT License - see LICENSE file

## Acknowledgments

- SANS Internet Storm Center for inspiration
- Django community for excellent framework
- ISSN International Centre for standards

## Support

For issues and questions:
- GitHub Issues: https://github.com/caravori/isc-clone/issues
- Documentation: Check the wiki

## Credits

Developed by Gabriele Zancheta Scavazini
