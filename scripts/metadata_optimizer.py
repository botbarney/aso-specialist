#!/usr/bin/env python3
"""
Metadata Optimizer for ASO
Optimizes all App Store metadata for maximum conversion
"""

import argparse
from datetime import datetime
from typing import Dict, List


def optimize_title(app_name: str, keywords: List[str]) -> Dict:
    """Optimize app title (30 characters max)"""
    
    # If app name is already long, just use it
    if len(app_name) >= 28:
        return {
            'title': app_name[:30],
            'length': len(app_name[:30]),
            'strategy': 'App name only (already long)',
            'alternatives': []
        }
    
    # Add keyword after app name
    remaining = 30 - len(app_name) - 3  # -3 for " - "
    
    best_keyword = None
    for kw in keywords:
        if len(kw) <= remaining:
            best_keyword = kw
            break
    
    if best_keyword:
        title = f"{app_name} - {best_keyword.title()}"
    else:
        title = app_name
    
    # Generate alternatives
    alternatives = []
    for kw in keywords[:3]:
        alt = f"{app_name} - {kw.title()}"
        if len(alt) <= 30 and alt != title:
            alternatives.append(alt)
    
    return {
        'title': title[:30],
        'length': len(title[:30]),
        'strategy': 'App name + primary keyword',
        'alternatives': alternatives[:2]
    }


def optimize_subtitle(app_name: str, category: str, keywords: List[str]) -> Dict:
    """Optimize subtitle (30 characters max)"""
    
    category_phrases = {
        'baby': ['Baby Care Made Simple', 'Track & Monitor Baby', 'Newborn Essentials', 'Parent Helper'],
        'health': ['Your Health Companion', 'Track Fitness Goals', 'Wellness Made Easy', 'Stay Healthy'],
        'productivity': ['Get More Done', 'Organize Your Life', 'Task Manager', 'Stay Productive'],
        'finance': ['Manage Your Money', 'Track Expenses', 'Budget Better', 'Save More'],
        'photo': ['Edit Photos Beautifully', 'Perfect Your Shots', 'Photo Enhancer', 'Create Memories'],
        'social': ['Connect With Friends', 'Share Moments', 'Stay Connected', 'Meet New People'],
        'travel': ['Explore The World', 'Plan Your Trip', 'Travel Smarter', 'Wanderlust'],
        'food': ['Cook With Confidence', 'Meal Planner', 'Recipe Organizer', 'Eat Better'],
        'education': ['Learn Something New', 'Study Smarter', 'Knowledge Builder', 'Skill Up'],
        'game': ['Play & Have Fun', 'Challenge Yourself', 'Game On', 'Level Up'],
    }
    
    # Find best category match
    category_lower = category.lower()
    phrases = ['Simple & Powerful', 'Easy & Intuitive', 'Made For You', 'Do More']
    
    for key, key_phrases in category_phrases.items():
        if key in category_lower:
            phrases = key_phrases
            break
    
    # Find phrase that fits
    best_subtitle = phrases[0]
    for phrase in phrases:
        if len(phrase) <= 30:
            best_subtitle = phrase
            break
    
    return {
        'subtitle': best_subtitle[:30],
        'length': len(best_subtitle[:30]),
        'strategy': 'Benefit-driven phrase',
        'alternatives': [p for p in phrases if p != best_subtitle and len(p) <= 30][:3]
    }


def optimize_keywords(keywords: List[str], title: str, subtitle: str) -> Dict:
    """Optimize keyword field (100 characters max)"""
    
    # Words already used in title/subtitle (don't repeat)
    used_words = set()
    for text in [title, subtitle]:
        used_words.update(text.lower().split())
    
    # Filter out used words and their singular/plural forms
    available_keywords = []
    for kw in keywords:
        kw_clean = kw.lower().strip()
        # Skip if word or its root is already used
        should_skip = False
        for used in used_words:
            if kw_clean in used or used in kw_clean:
                should_skip = True
                break
        if not should_skip:
            available_keywords.append(kw_clean)
    
    # Build keyword string within 100 char limit
    selected = []
    current_length = 0
    
    for kw in available_keywords:
        separator = 1 if selected else 0
        if current_length + len(kw) + separator <= 100:
            selected.append(kw)
            current_length += len(kw) + separator
    
    keyword_string = ','.join(selected)
    
    return {
        'keywords': keyword_string,
        'length': len(keyword_string),
        'count': len(selected),
        'strategy': 'Maximize coverage without repeating title/subtitle words',
        'unused_keywords': available_keywords[len(selected):][:10]
    }


def generate_promotional_text(app_name: str, category: str, highlight: str = None) -> Dict:
    """Generate promotional text (170 characters max)"""
    
    templates = [
        f"New in {app_name}: {highlight}!" if highlight else None,
        f"Just launched: {app_name} makes {category} easier than ever!",
        f"Try {app_name} - the easiest way to {category} on iPhone!",
        f"Join thousands using {app_name} for their {category} needs!",
        f"Limited time: {app_name} Premium is 50% off!",
        f"New update: Better, faster {category} tracking!",
    ]
    
    templates = [t for t in templates if t and len(t) <= 170]
    
    if not templates:
        templates = [f"Download {app_name} today!"]
    
    best = templates[0]
    for t in templates:
        if len(t) <= 170 and len(t) > len(best):
            best = t
    
    return {
        'promotional_text': best[:170],
        'length': len(best[:170]),
        'alternatives': templates[1:4],
        'strategy': 'Time-sensitive or feature highlight'
    }


def generate_description(app_name: str, category: str, features: List[str]) -> Dict:
    """Generate full description (4000 characters max)"""
    
    feature_lines = '\n'.join([f"• {f.title()} - Quick and easy" for f in features[:8]])
    
    # Category-specific opening paragraphs
    openings = {
        'baby': f"""**The {app_name} app helps parents track their baby's daily activities with ease.**

From feedings and diapers to sleep patterns and milestones, {app_name} makes it simple to monitor your little one's development. Designed with love by parents, for parents.""",
        'health': f"""**{app_name} is your personal health companion, helping you achieve your wellness goals.**

Track your activities, monitor your progress, and stay motivated with powerful insights. Whether you're just starting your fitness journey or training for your next event, {app_name} has you covered.""",
        'productivity': f"""**Stay organized and get more done with {app_name}.**

{app_name} brings all your tasks, schedules, and projects together in one beautiful, intuitive app. Stop juggling multiple tools and start focusing on what matters.""",
        'finance': f"""**Take control of your finances with {app_name}.**

Track expenses, monitor budgets, and achieve your savings goals with ease. {app_name} makes money management simple, secure, and even enjoyable.""",
    }
    
    category_lower = category.lower()
    opening = openings.get('baby')  # Default
    for key, text in openings.items():
        if key in category_lower:
            opening = text
            break
    
    description = f"""{opening}

**KEY FEATURES:**
{feature_lines}

**WHY USERS LOVE {app_name.upper()}:**
✓ Intuitive design - no learning curve
✓ Powerful features that just work
✓ Sync across all your devices
✓ Regular updates with new features
✓ Private and secure - your data stays yours

**SUPPORT:**
We'd love to hear from you! Contact our friendly support team at support@{app_name.lower().replace(' ', '')}.com

**PREMIUM FEATURES:**
Upgrade to Premium for unlimited access, advanced features, cloud backup, and priority support.

Download {app_name} today and join thousands of happy users!

---

**Privacy Policy:** https://{app_name.lower().replace(' ', '')}.com/privacy
**Terms of Service:** https://{app_name.lower().replace(' ', '')}.com/terms
"""
    
    return {
        'description': description,
        'length': len(description),
        'remaining': 4000 - len(description),
        'strategy': 'Structured for readability with clear benefits'
    }


def generate_whats_new(version: str, features: List[str], bugfixes: bool = True) -> Dict:
    """Generate What's New text for app updates"""
    
    feature_bullets = '\n'.join([f"• {f.title()}" for f in features[:5]])
    
    whats_new = f"""**New in Version {version}:**

{feature_bullets}
"""
    
    if bugfixes:
        whats_new += """
**Improvements:**
• Bug fixes and performance improvements
• Enhanced stability"""
    
    whats_new += """

Thanks for using our app! We read every review and appreciate your feedback."""
    
    return {
        'whats_new': whats_new,
        'length': len(whats_new),
        'strategy': 'Highlight new features, mention improvements'
    }


def generate_category_keywords(category: str) -> List[str]:
    """Generate relevant keywords for a category"""
    
    category_keywords = {
        'baby': ['newborn', 'infant', 'toddler', 'nursing', 'breastfeeding', 'formula', 'diaper', 'sleep', 'nap', 'schedule', 'tracker', 'log', 'monitor', 'parent', 'mom', 'dad', 'care', 'growth', 'milestone', 'feeding', 'pump', 'wean', 'solids'],
        'health': ['fitness', 'workout', 'exercise', 'gym', 'running', 'yoga', 'meditation', 'wellness', 'nutrition', 'diet', 'calories', 'steps', 'heart', 'sleep', 'weight', 'bmi', 'training', 'cardio', 'strength', 'healthkit'],
        'productivity': ['planner', 'organizer', 'calendar', 'schedule', 'todo', 'task', 'list', 'notes', 'reminder', 'timer', 'pomodoro', 'project', 'manager', 'time', 'focus', 'habit', 'goal', 'routine'],
        'finance': ['budget', 'money', 'expense', 'income', 'savings', 'debt', 'bill', 'payment', 'bank', 'cash', 'wallet', 'account', 'transaction', 'receipt', 'invest', 'crypto', 'tax', 'report'],
        'photo': ['editor', 'filter', 'effect', 'camera', 'collage', 'video', 'slideshow', 'beauty', 'retouch', 'frame', 'sticker', 'text', 'crop', 'rotate', 'adjust', 'enhance', 'share'],
        'travel': ['map', 'navigation', 'gps', 'flight', 'hotel', 'booking', 'trip', 'vacation', 'itinerary', 'guide', 'translator', 'currency', 'packing', 'explore', 'destination'],
        'food': ['recipe', 'cook', 'meal', 'plan', 'kitchen', 'grocery', 'shopping', 'list', 'nutrition', 'calorie', 'diet', 'vegetarian', 'vegan', 'restaurant', 'delivery'],
        'education': ['learn', 'study', 'course', 'lesson', 'quiz', 'test', 'flashcard', 'language', 'vocabulary', 'grammar', 'math', 'science', 'code', 'programming', 'skill'],
        'social': ['chat', 'message', 'call', 'video', 'friend', 'group', 'community', 'share', 'connect', 'meet', 'dating', 'network', 'follow', 'post', 'story'],
        'game': ['puzzle', 'adventure', 'action', 'strategy', 'arcade', 'racing', 'sports', 'word', 'trivia', 'card', 'board', 'multiplayer', 'casual', 'brain', 'quiz'],
    }
    
    category_lower = category.lower()
    for key, keywords in category_keywords.items():
        if key in category_lower:
            return keywords
    
    return ['app', 'mobile', 'ios', 'tool', 'utility', 'simple', 'easy', 'fast', 'smart', 'pro']


def generate_metadata_report(app_name: str, category: str, version: str = "1.0", 
                            custom_keywords: List[str] = None, new_features: List[str] = None) -> str:
    """Generate complete metadata optimization report"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Generate keywords
    category_keywords = generate_category_keywords(category)
    if custom_keywords:
        all_keywords = custom_keywords + category_keywords
    else:
        all_keywords = category_keywords
    
    # Remove duplicates while preserving order
    seen = set()
    all_keywords = [x for x in all_keywords if not (x in seen or seen.add(x))]
    
    # Generate all metadata
    title_data = optimize_title(app_name, all_keywords)
    subtitle_data = optimize_subtitle(app_name, category, all_keywords)
    keywords_data = optimize_keywords(all_keywords, title_data['title'], subtitle_data['subtitle'])
    promo_data = generate_promotional_text(app_name, category)
    
    features = new_features if new_features else category_keywords[:5]
    desc_data = generate_description(app_name, category, features)
    whatsnew_data = generate_whats_new(version, features[:3])
    
    report = f"""# App Store Metadata Package: {app_name}

**Generated:** {timestamp}  
**App:** {app_name}  
**Category:** {category.title()}  
**Version:** {version}

---

## 📱 App Information

### App Name (Title)
```
{title_data['title']}
```
**Length:** {title_data['length']}/30 characters  
**Strategy:** {title_data['strategy']}

**Alternatives to test:**
"""
    
    for alt in title_data['alternatives']:
        report += f"- `{alt}` ({len(alt)} chars)\n"
    
    report += f"""
### Subtitle
```
{subtitle_data['subtitle']}
```
**Length:** {subtitle_data['length']}/30 characters  
**Strategy:** {subtitle_data['strategy']}

**Alternatives:**
"""
    
    for alt in subtitle_data['alternatives']:
        report += f"- `{alt}`\n"
    
    report += f"""
---

## 🔑 Keywords

### Keyword Field (100 characters max)
```
{keywords_data['keywords']}
```
**Length:** {keywords_data['length']}/100 characters  
**Keyword count:** {keywords_data['count']}  
**Strategy:** {keywords_data['strategy']}

**Additional keywords to consider (if space allows):**
"""
    
    for kw in keywords_data['unused_keywords'][:5]:
        report += f"- `{kw}`\n"
    
    report += f"""
---

## 📝 Description

```
{desc_data['description']}
```

**Length:** {desc_data['length']}/4000 characters  
**Remaining:** {desc_data['remaining']} characters  
**Strategy:** {desc_data['strategy']}

---

## 📢 Promotional Text

```
{promo_data['promotional_text']}
```

**Length:** {promo_data['length']}/170 characters  
**Strategy:** {promo_data['strategy']}  
**Update frequency:** Change with each release or promotion

**Alternative options:**
"""
    
    for alt in promo_data['alternatives']:
        report += f"- `{alt}` ({len(alt)} chars)\n"
    
    report += f"""
---

## 🆕 What's New (Version {version})

```
{whatsnew_data['whats_new']}
```

**Length:** {whatsnew_data['length']} characters  
**Strategy:** {whatsnew_data['strategy']}

---

## ✅ Metadata Checklist

Before submitting to App Store Connect:

### Required Fields:
- [ ] App Name: 30 chars max ✓ ({title_data['length']} chars)
- [ ] Subtitle: 30 chars max ✓ ({subtitle_data['length']} chars)
- [ ] Keywords: 100 chars max ✓ ({keywords_data['length']} chars)
- [ ] Description: 4000 chars max ✓ ({desc_data['length']} chars)
- [ ] Promotional Text: 170 chars max ✓ ({promo_data['length']} chars)
- [ ] What's New: Required for updates ✓

### Quality Checks:
- [ ] No competitor app names in keywords (against guidelines)
- [ ] No special characters in title (emojis, symbols)
- [ ] Keywords are comma-separated, no spaces
- [ ] Description is formatted with markdown (bold, bullets)
- [ ] No "free" or price mentions in metadata
- [ ] No misleading claims

### Localization:
- [ ] Metadata translated for each target market
- [ ] Keywords researched per locale
- [ ] Cultural references appropriate
- [ ] Currency/formats localized

---

## 🚀 Quick Copy-Paste

**For App Store Connect - App Information:**

```
Name: {title_data['title']}
Subtitle: {subtitle_data['subtitle']}
```

**For App Store Connect - Keywords:**
```
{keywords_data['keywords']}
```

**For App Store Connect - Description:**
[Paste from Description section above]

**For App Store Connect - Promotional Text:**
```
{promo_data['promotional_text']}
```

**For App Store Connect - What's New:**
[Paste from What's New section above]

---

## 📊 Optimization Tips

### Title Optimization:
1. Put most important keywords first
2. Brand name should be recognizable
3. Don't stuff keywords - it looks spammy
4. Test variations with A/B testing

### Keyword Field Optimization:
1. Use all 100 characters
2. No spaces after commas
3. Don't repeat words from title/subtitle
4. Include both singular and plural forms
5. Add common misspellings
6. No competitor names (violates guidelines)

### Description Optimization:
1. First 3 lines are most important (above fold)
2. Use bullet points for readability
3. Include social proof (ratings, awards)
4. Clear call-to-action at end
5. Update with new features

---

*Metadata package generated by ASO Specialist Skill*
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Optimize App Store metadata')
    parser.add_argument('--app-name', required=True, help='Your app name')
    parser.add_argument('--category', required=True, help='App category (e.g., baby tracker)')
    parser.add_argument('--version', default='1.0', help='App version')
    parser.add_argument('--keywords', help='Comma-separated custom keywords')
    parser.add_argument('--features', help='Comma-separated new features')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    custom_keywords = [k.strip() for k in args.keywords.split(',')] if args.keywords else None
    new_features = [f.strip() for f in args.features.split(',')] if args.features else None
    
    print(f"📝 Generating metadata for: {args.app_name}")
    print(f"📂 Category: {args.category}")
    print(f"📦 Version: {args.version}")
    
    report = generate_metadata_report(
        args.app_name, 
        args.category, 
        args.version,
        custom_keywords,
        new_features
    )
    
    if args.output:
        output_file = args.output
    else:
        safe_name = args.app_name.replace(' ', '_').lower()
        output_file = f"metadata_{safe_name}.md"
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Metadata package saved to: {output_file}")
    print(f"📊 All fields optimized and within character limits")


if __name__ == '__main__':
    main()
