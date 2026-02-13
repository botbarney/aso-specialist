#!/usr/bin/env python3
"""
Screenshot Generator for ASO
Creates screenshot concepts and strategy for App Store
"""

import argparse
from datetime import datetime
from typing import List, Dict


# iPhone screenshot dimensions
SCREENSHOT_DIMENSIONS = {
    '6.7 inch': {
        'devices': ['iPhone 16 Pro Max', 'iPhone 15 Pro Max', 'iPhone 14 Pro Max'],
        'portrait': '1290 x 2796',
        'landscape': '2796 x 1290',
        'required': True
    },
    '6.5 inch': {
        'devices': ['iPhone 14 Plus', 'iPhone 13 Pro Max', 'iPhone 12 Pro Max', 'iPhone 11 Pro Max', 'iPhone 11'],
        'portrait': '1284 x 2778',
        'landscape': '2778 x 1284',
        'required': True
    },
    '5.5 inch': {
        'devices': ['iPhone 8 Plus', 'iPhone 7 Plus', 'iPhone 6s Plus'],
        'portrait': '1242 x 2208',
        'landscape': '2208 x 1242',
        'required': False  # Optional but recommended
    },
    'iPad Pro 6th Gen': {
        'devices': ['iPad Pro 12.9" (6th gen)'],
        'portrait': '2048 x 2732',
        'landscape': '2732 x 2048',
        'required': False
    },
    'iPad Pro 2nd Gen': {
        'devices': ['iPad Pro 12.9" (2nd gen)'],
        'portrait': '2048 x 2732',
        'landscape': '2732 x 2048',
        'required': False
    }
}


def get_screenshot_templates(category: str) -> Dict[str, List[str]]:
    """Get screenshot templates based on app category"""
    templates = {
        'default': {
            'screenshot_1': ['Show the main interface', 'Highlight the core value prop', 'Use lifestyle imagery'],
            'screenshot_2': ['Show a key feature in action', 'Demonstrate ease of use'],
            'screenshot_3': ['Show another key feature', 'Highlight unique functionality'],
            'screenshot_4': ['Show results/tracking/progress', 'Visual proof of value'],
            'screenshot_5': ['Show customization/settings', 'Social proof or testimonials'],
        },
        'baby': {
            'screenshot_1': ['Cute baby photo + app overlay', 'Peaceful sleeping baby', 'Parent using app while feeding'],
            'screenshot_2': ['Feeding tracker interface', 'Timer in action', 'Log entry screen'],
            'screenshot_3': ['Sleep tracking visualization', 'Charts and patterns', 'Sleep schedule view'],
            'screenshot_4': ['Growth charts/milestones', 'Baby development tracker', 'Weight/height tracking'],
            'screenshot_5': ['Multiple device sync', 'Family sharing view', 'Export/share features'],
        },
        'health': {
            'screenshot_1': ['Active person exercising', 'Health metrics dashboard', 'Before/after transformation'],
            'screenshot_2': ['Workout in progress', 'Exercise demonstration', 'Heart rate monitoring'],
            'screenshot_3': ['Progress charts/graphs', 'Statistics overview', 'Goal tracking'],
            'screenshot_4': ['Meal/nutrition tracking', 'Food logging interface', 'Calorie counter'],
            'screenshot_5': ['Social features', 'Achievements/badges', 'Community challenges'],
        },
        'productivity': {
            'screenshot_1': ['Organized workspace', 'Clean task list', 'Calendar overview'],
            'screenshot_2': ['Task creation/management', 'Quick capture feature', 'Smart suggestions'],
            'screenshot_3': ['Calendar/scheduling view', 'Time blocking', 'Reminders'],
            'screenshot_4': ['Collaboration features', 'Sharing options', 'Team workspace'],
            'screenshot_5': ['Widgets/home screen', 'Siri integration', 'Cross-device sync'],
        },
        'finance': {
            'screenshot_1': ['Clean dashboard', 'Account overview', 'Balance display'],
            'screenshot_2': ['Expense tracking', 'Transaction list', 'Receipt capture'],
            'screenshot_3': ['Budget visualization', 'Spending by category', 'Pie/donut charts'],
            'screenshot_4': ['Savings goals', 'Investment tracking', 'Net worth graph'],
            'screenshot_5': ['Bill reminders', 'Reports/export', 'Bank sync'],
        },
        'photo': {
            'screenshot_1': ['Stunning before/after', 'Photo grid showcase', 'Artistic edit result'],
            'screenshot_2': ['Editing tools', 'Filter selection', 'Adjustment sliders'],
            'screenshot_3': ['AI features', 'Auto-enhance', 'Smart adjustments'],
            'screenshot_4': ['Collage/mosaic maker', 'Frame options', 'Layout selection'],
            'screenshot_5': ['Export/sharing', 'Social media ready', 'Print options'],
        }
    }
    
    category_lower = category.lower()
    for key in templates:
        if key in category_lower:
            return templates[key]
    
    return templates['default']


def generate_text_overlay(feature: str, category: str, index: int) -> Dict:
    """Generate text overlay copy for a screenshot"""
    
    headlines = {
        0: ["Simple & Intuitive", "Effortless Tracking", "Made for Parents", "Your Baby's Story"],
        1: ["Track Everything", "Smart Logging", "One-Tap Entry", "Quick & Easy"],
        2: ["See Patterns", "Understand Sleep", "Smart Insights", "Visual Timeline"],
        3: ["Watch Them Grow", "Milestones Matter", "Track Development", "Growth Charts"],
        4: ["Share with Family", "Stay in Sync", "Export Anytime", "Always Available"],
    }
    
    subheadlines = {
        0: ["Beautiful design that just works", "No complicated setup required", "Built by parents, for parents"],
        1: [f"Log {feature} in seconds", f"Never miss a {feature} again", f"Complete {feature} history"],
        2: ["Spot trends at a glance", "Understand your baby's rhythm", "Data-driven insights"],
        3: ["Track every milestone", "Pediatrician-ready reports", "Celebrate every moment"],
        4: ["Multi-device sync", "Share with caregivers", "Backup to cloud"],
    }
    
    idx = min(index, 4)
    
    return {
        'headline': headlines[idx][0],
        'subheadline': subheadlines[idx][0],
        'max_headline_length': 25,
        'max_subheadline_length': 40,
        'font_recommendation': 'SF Pro Display Bold (headline), SF Pro Text Regular (sub)',
        'color_scheme': 'High contrast - white text on dark background or vice versa'
    }


def get_design_direction(category: str) -> Dict:
    """Get design direction based on category"""
    directions = {
        'baby': {
            'style': 'Warm, soft, nurturing',
            'colors': 'Pastel blues, pinks, mint greens, soft yellows',
            'imagery': 'Real babies (with permission), soft textures, natural light',
            'typography': 'Rounded, friendly fonts',
            'tone': 'Supportive, reassuring, gentle'
        },
        'health': {
            'style': 'Energetic, motivating, clean',
            'colors': 'Vibrant greens, oranges, energetic blues',
            'imagery': 'Active people, gym environments, healthy food',
            'typography': 'Bold, athletic fonts',
            'tone': 'Encouraging, energetic, professional'
        },
        'productivity': {
            'style': 'Clean, minimal, organized',
            'colors': 'Blues, grays, whites, accent colors sparingly',
            'imagery': 'Clean workspaces, devices, calendars',
            'typography': 'Clean sans-serif, highly legible',
            'tone': 'Efficient, professional, focused'
        },
        'finance': {
            'style': 'Trustworthy, secure, professional',
            'colors': 'Blues, greens (for money), professional grays',
            'imagery': 'Charts, graphs, secure imagery',
            'typography': 'Clean, trustworthy fonts',
            'tone': 'Professional, secure, reliable'
        },
        'default': {
            'style': 'Modern, clean, approachable',
            'colors': 'Brand colors with high contrast',
            'imagery': 'Lifestyle or UI depending on app type',
            'typography': 'SF Pro or similar system fonts',
            'tone': 'Friendly, professional, helpful'
        }
    }
    
    category_lower = category.lower()
    for key in directions:
        if key in category_lower:
            return directions[key]
    
    return directions['default']


def generate_screenshot_concepts(app_name: str, features: List[str], category: str) -> List[Dict]:
    """Generate screenshot concepts"""
    templates = get_screenshot_templates(category)
    concepts = []
    
    screenshot_order = ['screenshot_1', 'screenshot_2', 'screenshot_3', 'screenshot_4', 'screenshot_5']
    
    for i, key in enumerate(screenshot_order):
        feature = features[i] if i < len(features) else (features[-1] if features else 'Core Feature')
        template_options = templates.get(key, templates['screenshot_1'])
        text = generate_text_overlay(feature, category, i)
        
        concepts.append({
            'position': i + 1,
            'purpose': 'Hero/Value Prop' if i == 0 else f'Feature {i}',
            'feature_to_show': feature,
            'visual_direction': template_options,
            'text_overlay': text,
            'call_to_action': 'Download now' if i == 4 else None,
            'notes': 'Lead with emotion on first screenshot' if i == 0 else 'Show actual UI interface'
        })
    
    return concepts


def generate_description(app_name: str, features: List[str], category: str) -> str:
    """Generate App Store description optimized for conversion"""
    
    feature_bullets = '\n'.join([f"• {f.title()} - Easy tracking and insights" for f in features[:5]])
    
    descriptions = {
        'baby': f"""**The {app_name} app helps busy parents track everything about their baby with ease.**

From feedings and diapers to sleep patterns and milestones, {app_name} makes it simple to monitor your little one's development. Designed by parents, for parents.

**KEY FEATURES:**
{feature_bullets}

**WHY PARENTS LOVE {app_name.upper()}:**
✓ Quick one-tap logging - perfect for 3 AM feedings
✓ Beautiful charts show patterns and trends
✓ Share data with partner, nanny, or pediatrician
✓ Works offline - sync when connected
✓ Private and secure - your data stays yours

**SUPPORT:**
We'd love to hear from you! Contact us at support@{app_name.lower().replace(' ', '')}.com

**PREMIUM FEATURES:**
Upgrade to Premium for unlimited history, advanced analytics, PDF reports, and cloud backup.

Download {app_name} today and spend less time tracking, more time bonding.
""",
        'default': f"""**{app_name} - The easiest way to {features[0] if features else 'track what matters'}.**

{app_name} helps you stay organized and in control. With an intuitive interface and powerful features, it's never been easier to manage your {category}.

**KEY FEATURES:**
{feature_bullets}

**WHY USERS CHOOSE {app_name.upper()}:**
✓ Simple, intuitive design
✓ Powerful features that just work
✓ Sync across all your devices
✓ Regular updates with new features
✓ Private and secure

**SUPPORT:**
Questions? We're here to help at support@{app_name.lower().replace(' ', '')}.com

Download {app_name} today and see why thousands of users trust us every day.
"""
    }
    
    category_lower = category.lower()
    for key in descriptions:
        if key in category_lower:
            return descriptions[key]
    
    return descriptions['default']


def generate_report(app_name: str, features: List[str], category: str) -> str:
    """Generate complete screenshot strategy report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    concepts = generate_screenshot_concepts(app_name, features, category)
    design = get_design_direction(category)
    description = generate_description(app_name, features, category)
    
    report = f"""# Screenshot Strategy: {app_name}

**Generated:** {timestamp}  
**Category:** {category.title()}  
**Features:** {', '.join(features)}

---

## 📐 Required Dimensions

### iPhone Screenshots (Required)
"""
    
    for size, specs in SCREENSHOT_DIMENSIONS.items():
        if 'iPhone' in specs['devices'][0]:
            report += f"""
**{size} Display**
- Devices: {', '.join(specs['devices'])}
- Portrait: {specs['portrait']} px
- Landscape: {specs['landscape']} px
- Status: {'Required' if specs['required'] else 'Recommended'}
"""
    
    report += f"""
### iPad Screenshots (Optional but Recommended)
"""
    
    for size, specs in SCREENSHOT_DIMENSIONS.items():
        if 'iPad' in size:
            report += f"""
**{size}**
- Portrait: {specs['portrait']} px
- Landscape: {specs['landscape']} px
"""
    
    report += """
---

## 🎨 Design Direction

"""
    
    for key, value in design.items():
        report += f"**{key.title()}:** {value}\n\n"
    
    report += f"""
---

## 📱 Screenshot Concepts (5 Screenshots)

"""
    
    for concept in concepts:
        report += f"""### Screenshot {concept['position']} - {concept['purpose']}

**Feature to Show:** {concept['feature_to_show']}

**Visual Direction:**
"""
        for direction in concept['visual_direction']:
            report += f"- {direction}\n"
        
        report += f"""
**Text Overlay:**
- **Headline:** "{concept['text_overlay']['headline']}"
- **Subheadline:** "{concept['text_overlay']['subheadline']}"
- **Font:** {concept['text_overlay']['font_recommendation']}
- **Max Lengths:** {concept['text_overlay']['max_headline_length']} chars (headline), {concept['text_overlay']['max_subheadline_length']} chars (sub)
- **Colors:** {concept['text_overlay']['color_scheme']}

**Notes:** {concept['notes']}

---

"""
    
    report += f"""## 📝 App Store Description

```
{description}
```

**Character count:** {len(description)}/4000

---

## ✅ Screenshot Checklist

### Technical Requirements:
- [ ] 72 dpi, RGB, flattened, no transparency
- [ ] High-quality JPEG or PNG
- [ ] No status bar (use Simulator or hide status bar)
- [ ] No device frame unless it's part of the design
- [ ] No pricing information
- [ ] No "Coming Soon" or future promises

### Content Guidelines:
- [ ] First screenshot shows value proposition clearly
- [ ] No excessive text (keep it scannable)
- [ ] Actual app UI (not mockups unless marked)
- [ ] Consistent branding across all screenshots
- [ ] Localized text for each market

### Best Practices:
- [ ] Test on device at actual size
- [ ] Check readability at thumbnail size
- [ ] A/B test different orders
- [ ] Update for major releases
- [ ] Seasonal variations for holidays

---

## 🛠️ Production Workflow

1. **Capture Screenshots**
   - Use iOS Simulator for perfect dimensions
   - Or use device frames in design tool
   - Include realistic data (not "Test User")

2. **Add Text Overlays**
   - Use Figma, Sketch, or Photoshop
   - Follow brand guidelines
   - Ensure text is readable at small sizes

3. **Export & Optimize**
   - Export at correct dimensions
   - Compress without quality loss
   - Name files descriptively

4. **Upload to App Store Connect**
   - Drag to appropriate device slots
   - Preview before saving
   - Check all localizations

---

## 🎯 A/B Testing Ideas

Test these variations to improve conversion:

1. **Screenshot Order:** Lifestyle first vs UI first
2. **Text Amount:** Minimal vs descriptive
3. **Color Schemes:** Light vs dark backgrounds
4. **Social Proof:** Add ratings/badges to first screenshot
5. **Device Framing:** With device frame vs full bleed

---

*Report generated by ASO Specialist Skill*
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Generate screenshot concepts for App Store')
    parser.add_argument('--app-name', required=True, help='Your app name')
    parser.add_argument('--features', required=True, help='Comma-separated features (e.g., "feeding tracking,sleep monitoring")')
    parser.add_argument('--category', default='general', help='App category')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    features = [f.strip() for f in args.features.split(',')]
    
    print(f"📱 Generating screenshot strategy for: {args.app_name}")
    print(f"🎯 Category: {args.category}")
    print(f"✨ Features: {', '.join(features)}")
    
    report = generate_report(args.app_name, features, args.category)
    
    if args.output:
        output_file = args.output
    else:
        safe_name = args.app_name.replace(' ', '_').lower()
        output_file = f"screenshots_{safe_name}.md"
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Screenshot strategy saved to: {output_file}")
    print(f"📊 Generated {len(features)} screenshot concepts")


if __name__ == '__main__':
    main()
