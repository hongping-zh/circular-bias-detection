# Icon Component Usage Guide

## Quick Start

Import the Icon component:
```jsx
import Icon from './Icon';
```

Use it in your JSX:
```jsx
<Icon name="search" size={24} />
```

## Available Icons

| Icon Name | Visual | Use Case |
|-----------|--------|----------|
| `search` | 🔍 | Search, detective, scan |
| `check` | ✓ | Success, completion, validation |
| `warning` | ⚠️ | Warnings, alerts, bias detected |
| `help` | ❓ | Help, questions, tutorial |
| `sparkles` | ✨ | Features, highlights, special |
| `lab` | 🧪 | Testing, experimental, development |
| `settings` | ⚙️ | Settings, processing, configuration |
| `circle` | ○ | Default, neutral, inactive |
| `x` | ✗ | Close, error, delete |
| `info` | ℹ️ | Information, details |
| `refresh` | 🔄 | Refresh, reload, cycle |
| `chart` | 📊 | Analytics, charts, data |
| `wave` | 👋 | Welcome, greeting |

## Props

### `name` (required)
The icon identifier from the list above.
```jsx
<Icon name="search" />
```

### `size` (optional, default: 24)
Size in pixels for both width and height.
```jsx
<Icon name="check" size={16} />  // Small
<Icon name="check" size={24} />  // Default
<Icon name="check" size={48} />  // Large
```

### `color` (optional, default: 'currentColor')
Any valid CSS color value. Uses parent's text color by default.
```jsx
<Icon name="warning" color="#f44336" />
<Icon name="check" color="#4caf50" />
<Icon name="info" color="currentColor" />
```

### `className` (optional)
Additional CSS classes for custom styling.
```jsx
<Icon name="search" className="my-custom-class" />
```

## Examples

### Basic Usage
```jsx
<h1><Icon name="search" size={32} /> Sleuth</h1>
```

### With Color
```jsx
<Icon name="check" size={20} color="#4caf50" />
```

### In Buttons
```jsx
<button>
  <Icon name="search" size={16} /> Scan for Bias
</button>
```

### Dynamic Icons
```jsx
const statusIcon = isSuccess ? 'check' : 'warning';
<Icon name={statusIcon} size={24} />
```

### In Lists
```jsx
<ul>
  <li><Icon name="check" size={16} /> Feature 1</li>
  <li><Icon name="check" size={16} /> Feature 2</li>
</ul>
```

## Tips

1. **Size Guidelines**
   - Small icons (14-16px): List items, inline text
   - Medium icons (20-24px): Buttons, headers
   - Large icons (32-48px): Hero sections, major status

2. **Color Usage**
   - Use semantic colors: green for success, red for error, orange for warning
   - Default to `currentColor` to inherit parent's text color
   - Maintain sufficient contrast for accessibility

3. **Performance**
   - Icons are inline SVG, no external loading required
   - Small bundle size impact
   - Fast rendering across all devices

## Adding New Icons

To add a new icon, edit `Icon.jsx`:

```jsx
const icons = {
  // ... existing icons
  myNewIcon: (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2">
      {/* Your SVG path here */}
    </svg>
  )
};
```

All icons should:
- Use viewBox="0 0 24 24" for consistency
- Use `stroke={color}` for outline icons
- Use `strokeWidth="2"` for consistent line weight
- Include rounded line caps: `strokeLinecap="round" strokeLinejoin="round"`
