# UI Guidelines — Parling-Academy

## Design Language: Dark Tech

### Color Tokens
```css
--bg:      #0d0d12;
--surface: #16161f;
--card:    #1e1e2a;
--border:  #2a2a3a;
--accent:  #7c3aed;   /* purple */
--accent2: #06b6d4;   /* cyan */
--green:   #10b981;
--text:    #f1f1f6;
--muted:   #8888aa;
--radius:  14px;
--font:    'Segoe UI', system-ui, sans-serif;
```

### Layout
- Content max-width: `1200px`, `margin: 0 auto`, `padding: 0 5%`
- Hero: two-column grid (`1fr 1fr`), `gap: 60px`
- Section padding: `70px 5%`

### Gradient backgrounds
- CTA banner: `linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%)`
- Progress bars: purple `linear-gradient(90deg, #7c3aed, #a855f7)`
- Cyan bars: `linear-gradient(90deg, #06b6d4, #0ea5e9)`

### Component Behaviors
- `.lang-card:hover` → `border-color: --accent`, `translateY(-3px)`
- `.btn-primary:hover` → `translateY(-2px)`, deeper box-shadow
- `.btn-white:hover` → `translateY(-2px)`
- Nav: sticky, `backdrop-filter: blur(14px)`

### Radial glow effect
```css
background: radial-gradient(circle, rgba(124,58,237,.3) 0%, transparent 70%);
```
Used as `::before` pseudo on `.hero-visual`.
