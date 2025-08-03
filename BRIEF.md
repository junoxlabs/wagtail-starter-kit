## **Wagtail Marketing Starter Kit: System Architecture Document**

### **1. Introduction**

#### **1.1. Purpose**

This document outlines the system architecture for a universal, modern, and efficient **Wagtail Starter Kit**. The primary purpose of this starter kit is to serve as a robust and flexible foundation for building high-performance **marketing websites**.

#### **1.2. Scope**

The architecture described herein covers the backend structure, data modeling, frontend integration, performance strategies, and deployment considerations. It is intended to guide the development team in building a reusable boilerplate that prioritizes developer experience (DX), marketer user experience (UX), and maintainability.

#### **1.3. Core Principles**

The design of this system is guided by the following core principles:

- **Modularity:** Content and functionality will be constructed from independent, reusable, and composable blocks.
- **Convention over Configuration:** A clear and logical project structure will be established to ensure consistency and reduce cognitive overhead for developers.
- **Performance First:** The system will be architected for speed, incorporating caching, asset optimization, and efficient data retrieval by default.
- **Empowering Marketers (UX):** The Wagtail admin interface will be intuitive, providing content creators with the flexibility to build diverse pages without developer intervention.
- **Streamlined Development (DX):** The starter kit will provide a clean, well-documented, and modern development environment to maximize productivity.

---

### **2. System Architecture Overview**

The system is a monolithic web application built on the Django framework. Its architecture can be visualized in three primary layers:

1.  **Presentation Layer (Frontend):** Responsible for rendering the user interface. This layer is powered by Django's templating engine, styled with a utility-first CSS framework, and served as static assets. (whitenoise)
2.  **Application Layer (Backend):** Contains the core business logic. This is managed by **Wagtail CMS** and custom Django applications. It handles content management, data processing, user requests, and routing.
3.  **Data Layer:** Responsible for data persistence and caching. This includes a primary relational database (PostgreSQL is recommended) and an in-memory cache (Redis is recommended).

---

### **3. Technology Stack**

The following technologies will form the foundation of the starter kit. Specific versions are to be determined and managed by the development team.

- **Backend Framework:** Django (5 LTS)
- **Content Management System:** Wagtail CMS (7 LTS)
- **Programming Language:** Python (3.12)
- **Database:** PostgreSQL 17
- **Cache:** Redis 7 (Valkey)
- **Frontend Styling:** Tailwind CSS v4, DaisyUI v5 (via python-webpack-boilerplate >= v1.0.4)
- **Interactivity:** HTMX (htmx.org 2.0.6) + @hotwired/stimulus v3 (via python-webpack-boilerplate >= v1.0.4)
- **Server Environment:** A standard Python WSGI server (Gunicorn 23.0.0)
- **Build Environment:** A Bun js environment is required for the frontend asset build process. (not node.js, as bun is compatible with node/npm)

---

### **4. Application Structure (Django Apps)**

A modular application structure is mandated to ensure separation of concerns.

- **`project_name/`**: The core Django project directory containing `settings`, `urls.py`, and `wsgi.py`.
- **`apps/`**: A top-level directory to contain all custom applications.
  - **`home`**: Manages the `HomePage` model and templates. Acts as the default site entry point.
  - **`core`**: Contains foundational, project-wide logic. This includes abstract base models (`BasePage`), utility functions, custom template tags, and context processors.
  - **`frontend`**: Manages all frontend assets and the Tailwind CSS v4 integration. It contains no django models. Its sole purpose is to house `static_src` files, the Tailwind configuration, and collect the compiled `static` files. (via python-webpack-boilerplate >= v1.0.4)
  - **`blocks`**: A dedicated app for defining all custom `StreamField` and other blocks.
  - **`navigation`**: Manages site navigation. This will likely contain `Snippet` models for creating and managing menus.
  - **`seo`**: Manages global SEO settings and metadata, potentially via Site Settings or abstract models. (wagtail-seo >= 3.1.0)
  - **`search`**: for site-wide search functionality
  - **`forms`**: for handling user submissions if marketing sites will include contact and other forms. (wagtail-flexible-forms >= 2.1.0)
  - **(Other Apps)**: Specialized apps like `blog`, `portfolio`, or `services` can be added.

---

### **5. Data and Content Model**

This section defines the structure of the content that marketers will manage.

#### **5.1. Page Models**

All page types will inherit from a common base to ensure consistency.

- **`BasePage` (Abstract Model):** Defined in the `core` app. It will not be creatable on its own. It must include common fields essential for all pages, such as **SEO Title**, **Search Description**, **Open Graph Image**, and other metadata.
- **`StandardPage`:** A generic, flexible page type inheriting from `BasePage`. Its primary content area will be a `StreamField`.
- **`HomePage`:** A unique page type for the site's homepage. It may have a more structured layout with specific `StreamField` configurations for hero sections, featured content, etc.
- **Specialized Pages:** Other page types like `LandingPage`, `AboutPage`, etc., can be created as needed. They should inherit from `BasePage` and can customize their fields and allowed `StreamField` blocks.

#### **5.2. Content Composition: StreamField & StructBlocks**

The primary mechanism for flexible content creation will be **`StreamField`**. This allows marketers to build pages by combining pre-defined blocks. The following `StructBlocks` should be developed as a baseline:

- **Basic Blocks:** `RichTextBlock`, `HeadingBlock`, `ImageBlock` (with alt text and caption), `EmbedBlock`, `QuoteBlock`.
- **Component Blocks:**
  - `HeroBlock`: For primary page headers with headings, text, background images, and calls-to-action.
  - `CardBlock`: A repeatable block with an image, title, text, and link. To be used inside layout blocks.
  - `CallToActionBlock (CTA)`: A visually distinct block to encourage user action.
  - `ButtonBlock`: A configurable button with text, link, and style choices (e.g., primary, secondary).
- **Layout Blocks:**
  - `TwoColumnBlock` / `ThreeColumnBlock`: Structural blocks that can contain other blocks within them to create column-based layouts.
- **Advanced Blocks:** Blocks for integrating forms (`WagtailFormBlock`), tables (`TableBlock`), or displaying lists of other content (e.g., a "Latest Blog Posts" block).

#### **5.3. Reusable Data: Snippets**

For content that is not tied to a specific page and is reused across the site, **Wagtail Snippets** are required.

- **Navigation Menus:** A `Menu` snippet with an orderable `MenuItem` child model.
- **Testimonials:** A snippet for customer quotes, author names, and images.
- **Team Members:** A snippet for team member profiles.
- **FAQs:** A snippet for question/answer pairs, which can be grouped by category.
- **Reusable CTAs:** Snippets for standard calls-to-action that can be placed on multiple pages.

#### **5.4. Global Configuration: Site Settings**

Site-wide configuration that marketers need to manage will be implemented using **`wagtail.contrib.settings`**. This includes:

- **Site Identity:** Site Name, Logo, Favicon.
- **Contact Information:** Address, Phone Number, Email.
- **Social Media:** Links to social media profiles.
- **Analytics:** Fields for Google Analytics Tracking ID, Google Tag Manager ID, etc. [Do not use packages, make it vendor agnostic for analytics]
- **Global Scripts:** Header and footer script injection fields for marketing tags.

---

### **6. Frontend Architecture**

#### **6.1. Template Structure**

A standardized template hierarchy must be used:

- **`templates/base.html`**: The main site template. Contains the `<html>`, `<head>`, and `<body>` tags, loads the compiled CSS, and defines global block areas like `{% block content %}`.
- **`templates/pages/`**: Contains templates for specific page types (e.g., `home_page.html`).
- **`templates/blocks/`**: Contains templates for rendering each individual `StreamField` block (e.g., `hero_block.html`).
- **`templates/includes/`**: Contains reusable template fragments like the site header, footer, and navigation.
- **`templates/snippets/`**: Contains templates for rendering snippets.

#### **6.2. Styling & Static Assets**

The **`theme`** app is the single source of truth for frontend assets.

- **Configuration:** `tailwind.config.js` will define the design system (colors, fonts, spacing) and configure the DaisyUI plugin and theme.
- **Source Files:** All custom CSS will be located in `theme/static_src/src/styles.css`.
- **Build Process:** The team will use the `django-tailwind` package's management commands (`tailwind build`, `tailwind watch`) to compile source CSS into a single production-ready CSS file in `theme/static/css/`.
- **Asset Loading:** The compiled CSS file will be loaded in `base.html` using the `{% tailwind_css %}` template tag.
- **Production:** The standard `collectstatic` command will be used to gather all static files for deployment.

---

### **7. Performance & Optimization Strategy**

- **Caching:**
  - Implement a production cache backend (Redis). [wagtail-cache >= 3.0.0]
  - Use Wagtail's **frontend cache invalidation** to selectively purge cached pages upon updates.
  - Leverage Django's **template fragment caching** for expensive-to-render but frequently accessed components (e.g., navigation menus).
- **Database Queries:**
  - Mandate the use of `select_related` and `prefetch_related` in querysets to prevent N+1 query problems, especially when listing pages or snippets.
- **Image Optimization:**
  - Strictly use Wagtail's `{% image %}` template tag for all images. This enables on-the-fly resizing and cropping, ensuring that appropriately sized images are served to the user; consider adding specific guidance on image formats (WebP) and responsive image sets.
- **Asset Minification:**
  - The Tailwind CSS build process should be configured to minify the final CSS output for production.

---

### **8. User & Developer Experience**

#### **8.1. Marketer UX Enhancements**

- **Admin UI:** Use `ModelAdmin` to provide clean list, filter, and search interfaces for all Snippet types.
- **Help Text:** All fields in the Wagtail admin must have clear and concise `help_text`.
- **Block Grouping:** In `StreamField` definitions, blocks should be logically grouped using `group` attributes to create a cleaner UI.
- **Preview:** The Wagtail preview functionality must work flawlessly for all page and block types.
- **Accessibility**: Add WCAG compliance requirements and accessibility testing to the DX/UX section.

#### **8.2. Developer DX Enhancements**

- **Code Quality:** Implement automated linting and formatting tools (e.g., `ruff`, `black`, `isort`) in a pre-commit hook.
- **Documentation:** A comprehensive `README.md` must be maintained, outlining setup, environment variables, and common development tasks.
- **Type Hinting:** Python type hints should be used throughout the codebase for improved clarity and static analysis.
- **Testing:** A testing suite must be established, with a baseline of tests for custom models, utility functions, and complex StreamField blocks.

---

### **9. Deployment & Operations**

- **Environment Configuration:** All sensitive information (secret keys, database credentials, API keys) **must** be managed via environment variables, not hardcoded in settings.
- **Static Files:** A production-grade static file serving strategy is required, such as using WhiteNoise or a Content Delivery Network (CDN).
- **CI/CD Pipeline:** A continuous integration and deployment pipeline should be configured to automate testing, frontend asset building, static file collection, database migrations, and deployment.
- **Logging & Monitoring:** Configure structured logging and integrate with a monitoring service to track application performance and errors in production.
- **Containerization**: Docker support for consistent development and deployment environments.
- **Monitoring**: Be more specific about monitoring tools (e.g., Sentry for error tracking, New Relic for performance).
- **Backup Strategy**: Include database backup and recovery procedures. (Wagtail Admin Integration)

NOTE:

- do not use outdated and unmaintained packages; but keep long term stability in mind.
- use modern and fast tools as much as possible (but must be stable.)
