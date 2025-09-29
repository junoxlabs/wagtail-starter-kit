# Wagtail Marketing Starter Kit

A modern, flexible foundation for building high-performance marketing websites with Wagtail CMS.

## Features

- **Django 5.2 LTS** and **Wagtail 7.0 LTS** - Latest stable versions
- **SQLite** as primary database with Litestream replication
- **Tailwind CSS v4** with **DaisyUI v5** - Modern utility-first CSS framework
- **Turbo 8** + **Stimulus 3** - Enhanced interactivity without complex JavaScript
- **StreamField Blocks** - Flexible content composition system
- **Navigation Snippets** - Reusable menu system
- **SEO Ready** - Built-in SEO functionality with wagtail-seo
- **Caching** - Performance optimization with wagtail-cache
- **Forms** - Flexible form handling with wagtail-flexible-forms
- **Django-Vite Integration** - Modern asset pipeline

## Project Structure

```
├── apps/
│   ├── blocks/                     # Custom StreamField blocks
│   ├── core/                       # Base models and utilities
│   ├── pages/                      # Page models and templates
│   ├── navigation/                 # Navigation menu snippets
│   ├── search/                     # Site search functionality
│   ├── settings/                   # Site settings
│   ├── snippets/                   # Content snippets
│   └── forms/                      # Form handling
├── config/                         # Django settings and configuration
├── db/                             # SQLite database files
├── dev/                            # Development environment configuration
│   ├── docker-compose.dev.yml      # Docker Compose configuration for development
│   ├── Dockerfile                  # Dockerfile for development environment
│   ├── init.sh                     # Initialization script for development container
│   ├── litestream.yml              # Litestream configuration for SQLite replication
│   └── supervisord.conf            # Supervisor configuration for running services
├── frontend/                       # Frontend source files and build configuration
│   ├── src/                        # Source files
│   │   ├── app/                    # JavaScript application code
│   │   │   ├── main.js             # Main JavaScript entry point
│   │   │   └── controllers/        # Stimulus controllers
│   │   │       ├── form.js
│   │   │       └── navbar.js
│   │   └── css/                    # CSS source files
│   │       └── styles.css
│   ├── package.json                # Frontend dependencies
│   ├── vite.config.mjs             # Vite build configuration
│   └── bun.lock                    # Bun lock file
├── templates/                      # Django templates
│   ├── pages/                      # Page-specific templates
│   ├── blocks/                     # StreamField block templates
│   ├── includes/                   # Reusable template components
│   └── snippets/                   # Snippet templates
├── .env                            # Environment variables
├── .gitignore
├── Dockerfile
├── Makefile
├── manage.py
├── mise.toml
├── pyproject.toml
└── uv.lock
```

## Development Setup

This project uses `mise` for dependency management and `Docker` for the development environment.

1. **Prerequisites**

   Install `mise` to manage project dependencies:

   ```bash
   # On macOS
   brew install mise

   # Or follow installation instructions at https://mise.jdx.dev/
   ```

2. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd wagtail-starter-kit
   ```

3. **Install dependencies with mise**

   ```bash
   # Trust the mise configuration and install dependencies
   mise trust && mise install
   ```

4. **Start the development environment**

   ```bash
   # This will start Django, Vite, and all required services in Docker
   make dev
   ```

5. **Access the application**

   - Django: http://localhost:8000
   - Wagtail Admin: http://localhost:8000/admin/
   - Django Admin: http://localhost:8000/django-admin/
   - Vite Dev Server: http://localhost:5173

## Development Workflow

After starting the development environment with `make dev`, you can:

- View logs: `make dev-logs`
- Enter the app container: `make dev-bash`
- Once inside the container, run Django commands like:
  - `make migrate` - Run database migrations
  - `make makemigrations` or `make make` - Create new migrations
- Create a superuser: `make dev-createsuperuser` (run from host)

## Content Modeling

### BasePage Model

Abstract base page model that defines common fields and functionality that should be shared across all page types.
Inherits from `SeoMixin` and `Page` to provide SEO functionality via wagtail-seo.

- SEO Title and Description
- Open Graph Image
- Structured data support
- UUID field for stable identifiers

### FlexPage Model

A flexible page model that can be used for the homepage or other standard pages.
It uses a StreamField for maximum content flexibility.
Inherits from `BasePage`.

### BaseEntityPage Model

Abstract base page for all showcase entities with common fields.
Inherits from `FlexPage` (and thus `BasePage`).

- Tag (ForeignKey to Tag snippet)
- URL type preference (SEO-friendly or UUID-based)

### Showcase Pages

Specialized pages for displaying collections of entities:

- ProjectShowcasePage: Displays projects
- ServiceShowcasePage: Displays services
- PortfolioShowcasePage: Displays portfolio items
- ResourceShowcasePage: Displays resources

### ProjectPage, ServicePage, PortfolioItemPage Models

Specific page types for different entity categories:

- ProjectPage: Inherits from `BaseEntityPage`
- ServicePage: Inherits from `BaseEntityPage`
- PortfolioItemPage: Inherits from `BaseEntityPage`

### StreamField Blocks

The starter kit includes a comprehensive set of reusable blocks:

**Basic Blocks:**

- RichTextBlock
- HeadingBlock
- ImageBlock (with alt text and caption)
- EmbedBlock
- QuoteBlock

**Component Blocks:**

- HeroBlock: Primary page headers with headings, text, background images, and CTAs
- CardBlock: Repeatable block with image, title, text, and link
- CallToActionBlock: Visually distinct block to encourage user action
- ButtonBlock: Configurable button with text, link, and style choices

**Layout Blocks:**

- TwoColumnBlock: Structural block for two-column layouts
- ThreeColumnBlock: Structural block for three-column layouts

### Navigation Snippets

- Menu: Container for hierarchical menu items
- MenuItem: Individual menu items with links to pages or URLs, supporting nested structures

### Content Snippets

- Tag: For categorizing and organizing showcase entities

## Frontend Architecture

### CSS Framework

- Tailwind CSS v4 with DaisyUI v5
- Utility-first approach for rapid development
- Responsive design built-in

### JavaScript

- Turbo 8 & Stimulus 3 for for dynamic interactions and complex behaviors when needed

### Asset Pipeline

- Vite for bundling and optimization
- Bun for fast JavaScript package management
- Development and production build configurations

## Performance Features

- SQLite as primary database with Litestream replication
- Seperate SQLite database for caching with wagtail-cache
- Frontend cache invalidation
- Template fragment caching
- Image optimization with Wagtail's image tag
- Asset minification for production

## Development Tools

- Pre-commit hooks for code quality
- Type hints throughout the codebase
- Automated testing framework

## Deployment

- Environment variables for configuration
- WhiteNoise for static file serving
- Docker support for consistent environments
- CI/CD pipeline ready

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
