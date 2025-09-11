# Wagtail Marketing Starter Kit

A modern, flexible foundation for building high-performance marketing websites with Wagtail CMS.

## Features

- **Django 5.2 LTS** and **Wagtail 7.0 LTS** - Latest stable versions
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
│   ├── blocks/          # Custom StreamField blocks
│   ├── core/            # Base models and utilities
│   ├── frontend/        # Frontend assets and Tailwind integration
│   ├── pages/           # Page models and templates
│   ├── navigation/      # Navigation menu snippets
│   ├── seo/             # SEO settings and functionality
│   ├── search/          # Site search functionality
│   └── forms/           # Form handling
├── config/              # Django settings and configuration
├── templates/           # Django templates
│   ├── pages/           # Page-specific templates
│   ├── blocks/          # StreamField block templates
│   ├── includes/        # Reusable template components
│   └── snippets/        # Snippet templates
└── static/              # Static files
```

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd wagtail-starter-kit
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync
   ```

3. **Set up the database**

   ```bash
   uv run python manage.py migrate
   ```

4. **Create a superuser**

   ```bash
   uv run python manage.py createsuperuser
   ```

5. **Install frontend dependencies**

   ```bash
   cd apps/frontend/static_src
   bun install
   ```

6. **Build frontend assets**

   ```bash
   # Development build
   bun run dev

   # Production build
   bun run build
   ```

7. **Run the development server**
   ```bash
   uv run python manage.py runserver
   ```

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
- Category (ForeignKey to Category snippet)
- URL type preference (SEO-friendly or UUID-based)

### ShowcasePage Model

A page that showcases different types of entities (projects, services, portfolio items, resources).
Can display entities by category and supports filtering by entity type.
Inherits from `BasePage`.

### ProjectPage, ServicePage, PortfolioItemPage, ResourcePage Models

Specific page types for different entity categories:
- ProjectPage: Inherits from `BaseEntityPage`
- ServicePage: Inherits from `BaseEntityPage`
- PortfolioItemPage: Inherits from `BaseEntityPage`
- ResourcePage: Inherits from `BaseEntityPage`

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

- Menu: Container for menu items
- MenuItem: Individual menu items with links to pages or URLs

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

- Sqlite caching with wagtail-cache
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
