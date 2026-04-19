# Quick SEO Integration Guide

Add SEO to any page in 3 steps:

## Step 1: Import SEO Component

```tsx
import SEO from '../components/SEO';
```

## Step 2: Add SEO to Your Page

### For Static Pages (use predefined config)

```tsx
export function AboutPage() {
  return (
    <>
      <SEO page="about" />
      <div>About content...</div>
    </>
  );
}
```

### For Dynamic Pages (override with data)

```tsx
export function BlogPostPage() {
  const { id } = useParams();
  const [blog, setBlog] = useState(null);

  useEffect(() => {
    // Fetch blog data
  }, [id]);

  return (
    <>
      <SEO 
        title={blog.title}
        description={blog.excerpt}
        image={blog.image}
        type="article"
      />
      <article>{blog.content}</article>
    </>
  );
}
```

## Step 3: (Optional) Add to seoConfig

If you're creating a new static page, add it to `src/config/seoConfig.ts`:

```typescript
export const seoConfig: Record<string, SEOMetadata> = {
  // ... existing entries
  
  myNewPage: {
    title: 'My Page Title - KG Launchpad',
    description: 'My page description with keywords...',
    keywords: 'keyword1, keyword2, keyword3',
    type: 'website',
  },
};
```

---

## Available Props

```typescript
interface SEOProps {
  page?: string;                    // Reference to seoConfig key
  title?: string;                   // Page title
  description?: string;             // Meta description
  keywords?: string;               // Keywords (comma separated)
  image?: string;                  // OG image URL
  type?: 'website' | 'article' | 'profile';  // Page type
  publishedTime?: string;          // Article published time (ISO)
  modifiedTime?: string;           // Article modified time (ISO)
  author?: string;                 // Article author name
}
```

---

## Examples by Page Type

### Project/Product Detail
```tsx
<SEO 
  title={`${project.name} - Student Project`}
  description={project.description}
  image={project.thumbnail}
  type="article"
/>
```

### Blog Post
```tsx
<SEO 
  title={blog.title}
  description={blog.excerpt}
  image={blog.featuredImage}
  type="article"
  publishedTime={blog.publishedAt}
  modifiedTime={blog.updatedAt}
  author={blog.author}
/>
```

### Service/Course Detail
```tsx
<SEO 
  title={`${service.title} - Consulting Service`}
  description={service.overview}
  image={service.image}
/>
```

### Listing Page (Projects, Blogs, etc.)
```tsx
<SEO 
  page="projects"  // Uses predefined config
/>
```

---

## Pages to Update (Priority Order)

### High Priority (Top trafficked)
- [ ] LandingPage → `<SEO page="home" />`
- [ ] ProjectsPage → `<SEO page="projects" />`
- [ ] BlogPage → `<SEO page="blogs" />`
- [ ] LaunchpadPage → `<SEO page="launchpad" />`
- [ ] LaunchDeckPage → `<SEO page="launchdeck" />`

### Medium Priority
- [ ] ProjectDetailPage → `<SEO title={...} description={...} />`
- [ ] BlogPostPage → `<SEO title={...} type="article" />`
- [ ] ServiceDetailPage → `<SEO title={...} description={...} />`
- [ ] CoursesPage → `<SEO page="courses" />`
- [ ] EventsPage → `<SEO page="events" />`

### Lower Priority
- [ ] ProfilePage
- [ ] DashboardPages (if needed for indexing)
- [ ] Admin pages (mark with robots: noindex)

---

## Checking Your Work

After adding SEO to a page:

1. **View in browser**: Right-click → View Page Source
2. **Look for**:
   - `<title>` tag
   - `<meta name="description">`
   - `<meta property="og:..."`
   - `<link rel="canonical"`

3. **Use browser extensions**:
   - SEOquake
   - Lighthouse
   - Site Analyzer

---

## Common Mistakes to Avoid

❌ **DON'T**
- Duplicate titles across multiple pages
- Copy-paste descriptions (make each unique)
- Keyword stuffing
- Forgetting to add SEO to dynamic pages
- Leaving placeholder text

✅ **DO**
- Write descriptive, unique titles (50-60 chars)
- Include call-to-action in descriptions
- Focus on user value, not just keywords
- Add SEO early in component creation
- Use actual dynamic data from API

---

## Need Help?

Check `SEO_IMPLEMENTATION.md` for detailed guide on:
- How sitemap works
- Testing and verification
- Best practices
- Monitoring tips

---

**Quick Links**:
- SEO Component: `src/components/SEO.tsx`
- Config: `src/config/seoConfig.ts`
- Implementation Docs: `SEO_IMPLEMENTATION.md`
