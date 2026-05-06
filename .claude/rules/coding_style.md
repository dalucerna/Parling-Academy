# Coding Style — Parling-Academy

## HTML
- Semantic elements (`<nav>`, `<section>`, `<footer>`, etc.)
- Inline styles only for dynamic/one-off values; use CSS classes otherwise
- Classes follow `kebab-case`

## CSS
- All design tokens as CSS custom properties on `:root`
- Mobile-first with `min-width` media queries
- No `!important`
- Group rules: Reset → Variables → Layout → Components → Utilities

## Keeping it a single file
- Styles in `<style>` inside `<head>`
- No external stylesheets or JS frameworks
- Scripts (if any) at bottom of `<body>`
