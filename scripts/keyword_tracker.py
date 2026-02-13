#!/usr/bin/env python3
"""
Keyword Tracker for ASO
Researches and optimizes keywords for App Store
"""

import argparse
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Set, Tuple


# Common high-value keyword modifiers by category
KEYWORD_MODIFIERS = {
    'baby': ['newborn', 'infant', 'toddler', 'parent', 'mom', 'dad', 'nursing', 'feeding', 'sleep', 'tracker', 'log', 'monitor', 'care'],
    'health': ['fitness', 'workout', 'meditation', 'wellness', 'nutrition', 'diet', 'exercise', 'gym', 'yoga', 'running'],
    'productivity': ['planner', 'organizer', 'calendar', 'todo', 'task', 'notes', 'manager', 'reminder', 'schedule', 'time'],
    'finance': ['budget', 'money', 'expense', 'tracker', 'savings', 'banking', 'invest', 'crypto', 'bill', 'payment'],
    'photo': ['editor', 'filter', 'camera', 'collage', 'video', 'effects', 'beauty', 'selfie', 'slomo', 'boomerang'],
    'social': ['chat', 'messenger', 'dating', 'friends', 'community', 'network', 'connect', 'meet', 'share'],
    'travel': ['map', 'navigation', 'flight', 'hotel', 'booking', 'guide', 'planner', 'trip', 'vacation', 'explore'],
    'food': ['recipe', 'cooking', 'meal', 'diet', 'nutrition', 'restaurant', 'delivery', 'grocery', 'kitchen'],
    'education': ['learn', 'study', 'course', 'lesson', 'quiz', 'language', 'math', 'science', 'student', 'school'],
    'game': ['puzzle', 'adventure', 'action', 'strategy', 'arcade', 'racing', 'sports', 'word', 'card', 'multiplayer'],
}


def get_category_modifiers(category: str) -> List[str]:
    """Get relevant keyword modifiers for a category"""
    category_lower = category.lower()
    for key, modifiers in KEYWORD_MODIFIERS.items():
        if key in category_lower:
            return modifiers
    # Default modifiers if no match
    return ['app', 'mobile', 'ios', 'best', 'free', 'pro', 'premium', 'simple', 'easy', 'smart']


def generate_keyword_combinations(base_terms: List[str], modifiers: List[str]) -> List[str]:
    """Generate keyword combinations"""
    combinations = set()
    
    # Add base terms
    for term in base_terms:
        combinations.add(term.lower().strip())
    
    # Add modifiers
    for modifier in modifiers:
        combinations.add(modifier)
    
    # Generate combinations
    for term in base_terms:
        term_clean = term.lower().strip()
        for modifier in modifiers:
            # term + modifier
            combinations.add(f"{term_clean} {modifier}")
            combinations.add(f"{modifier} {term_clean}")
    
    return list(combinations)


def estimate_keyword_value(keyword: str, category: str) -> Dict:
    """Estimate keyword metrics (simulated based on patterns)"""
    keyword_lower = keyword.lower()
    
    # Length factor (shorter often better for mobile)
    length_score = max(0, 10 - len(keyword)) / 10
    
    # Competition estimation based on commonality
    common_words = ['app', 'free', 'best', 'new', 'top', 'pro']
    competition = 'High' if any(w in keyword_lower for w in common_words) else 'Medium'
    
    # Search volume estimation (simulated)
    word_count = len(keyword.split())
    if word_count == 1:
        volume = 'High' if len(keyword) < 8 else 'Medium'
    elif word_count == 2:
        volume = 'Medium-High'
    else:
        volume = 'Low-Medium'
    
    # Difficulty score (0-100)
    difficulty = 50
    if competition == 'High':
        difficulty += 30
    if len(keyword) < 6:
        difficulty += 10
    
    return {
        'keyword': keyword,
        'search_volume': volume,
        'competition': competition,
        'difficulty': min(100, difficulty),
        'length_score': round(length_score, 2),
        'character_count': len(keyword),
        'word_count': word_count
    }


def optimize_keywords_for_field(keywords: List[str], max_chars: int = 100) -> str:
    """Optimize keywords to fit App Store's 100 character limit"""
    selected = []
    current_length = 0
    
    # Sort by value (prefer shorter, high-volume keywords)
    sorted_keywords = sorted(keywords, key=lambda k: (len(k), -ord(k[0]) if k else 0))
    
    for keyword in sorted_keywords:
        # Add comma separator if not first keyword
        separator = 1 if selected else 0
        new_length = current_length + len(keyword) + separator
        
        if new_length <= max_chars:
            selected.append(keyword)
            current_length = new_length
        else:
            break
    
    return ','.join(selected)


def find_long_tail_keywords(base_terms: List[str], category: str) -> List[Dict]:
    """Find long-tail keyword opportunities"""
    long_tail = []
    
    # Common long-tail patterns
    patterns = [
        'best {term} app',
        '{term} tracker free',
        'simple {term}',
        '{term} for parents',
        'easy {term} log',
        'daily {term}',
        '{term} assistant',
        'my {term}',
        '{term} diary',
        '{term} journal',
    ]
    
    for term in base_terms:
        for pattern in patterns:
            keyword = pattern.format(term=term)
            metrics = estimate_keyword_value(keyword, category)
            if metrics['difficulty'] < 60:  # Lower competition
                long_tail.append(metrics)
    
    return sorted(long_tail, key=lambda x: x['difficulty'])


def analyze_keyword_density(competitor_keywords: List[str]) -> Dict[str, int]:
    """Analyze keyword frequency from competitors"""
    all_words = []
    for kw in competitor_keywords:
        all_words.extend(kw.lower().replace(',', ' ').split())
    
    word_freq = {}
    for word in all_words:
        word = word.strip()
        if len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    return dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:30])


def generate_keyword_report(category: str, app_name: str, base_terms: List[str]) -> str:
    """Generate comprehensive keyword report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Get modifiers for category
    modifiers = get_category_modifiers(category)
    
    # Generate combinations
    all_keywords = generate_keyword_combinations(base_terms, modifiers)
    
    # Estimate metrics for each
    keyword_metrics = [estimate_keyword_value(kw, category) for kw in all_keywords[:50]]
    
    # Sort by difficulty (easiest first)
    keyword_metrics.sort(key=lambda x: x['difficulty'])
    
    # Find long-tail opportunities
    long_tail = find_long_tail_keywords(base_terms, category)[:15]
    
    # Optimize for App Store fields
    keyword_field = optimize_keywords_for_field([k['keyword'] for k in keyword_metrics])
    
    report = f"""# Keyword Research Report: {app_name}

**Generated:** {timestamp}  
**Category:** {category.title()}  
**Base Terms:** {', '.join(base_terms)}

---

## 🎯 Primary Keywords (Optimized for App Store)

### Keyword Field (100 chars max)
```
{keyword_field}
```
**Character count:** {len(keyword_field)}/100

---

## 📊 Top Keyword Opportunities

| Keyword | Search Volume | Competition | Difficulty | Chars |
|---------|--------------|-------------|------------|-------|
"""
    
    for metric in keyword_metrics[:20]:
        report += f"| {metric['keyword']} | {metric['search_volume']} | {metric['competition']} | {metric['difficulty']} | {metric['character_count']} |\n"
    
    report += f"""
---

## 🎣 Long-Tail Keyword Opportunities

These keywords have lower competition and can drive targeted downloads:

| Keyword | Search Volume | Difficulty | Notes |
|---------|--------------|------------|-------|
"""
    
    for lt in long_tail:
        note = "Low competition" if lt['difficulty'] < 40 else "Moderate competition"
        report += f"| {lt['keyword']} | {lt['search_volume']} | {lt['difficulty']} | {note} |\n"
    
    report += f"""
---

## 💡 Keyword Strategy Recommendations

### Immediate Actions:
1. **Target Low-Hanging Fruit**: Focus on keywords with difficulty < 40 first
2. **Brand Protection**: Include your app name variations
3. **Competitor Keywords**: Consider bidding on competitor names (if allowed)
4. **Seasonal Adjustments**: Update keywords for holidays/events

### Title Optimization:
- **Format:** App Name - Keyword Phrase
- **Example:** "{app_name} - {base_terms[0].title()} Tracker & Log"
- **Max:** 30 characters for title

### Subtitle Optimization:
- **Focus:** Key benefit + secondary keyword
- **Example:** "Track {base_terms[0]} & sleep patterns easily"
- **Max:** 30 characters

### Keyword Field Tips:
- ✅ Use commas to separate (no spaces needed)
- ✅ Include singular and plural forms
- ✅ Add misspellings if relevant
- ❌ Don't repeat words from title/subtitle
- ❌ No need for spaces after commas

---

## 🔄 Keyword Tracking Setup

Track these metrics weekly:
- [ ] Ranking position for target keywords
- [ ] Conversion rate by keyword
- [ ] Competitor keyword changes
- [ ] Search volume trends

### Keywords to Monitor:
"""
    
    for metric in keyword_metrics[:10]:
        report += f"- [ ] {metric['keyword']}\n"
    
    report += f"""
---

## 📈 Next Steps

1. [ ] Implement optimized keywords in App Store Connect
2. [ ] Set up keyword ranking tracker
3. [ ] Plan A/B test for title variations
4. [ ] Monitor competitor keyword updates
5. [ ] Update keywords monthly based on performance

---

*Report generated by ASO Specialist Skill*
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Research and optimize App Store keywords')
    parser.add_argument('--category', required=True, help='App category (e.g., "baby tracker")')
    parser.add_argument('--app-name', required=True, help='Your app name')
    parser.add_argument('--terms', help='Comma-separated base terms (optional)')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    print(f"🔍 Researching keywords for: {args.app_name}")
    print(f"📂 Category: {args.category}")
    
    # Determine base terms
    if args.terms:
        base_terms = [t.strip() for t in args.terms.split(',')]
    else:
        base_terms = [args.app_name] + args.category.split()
    
    print(f"📝 Base terms: {', '.join(base_terms)}")
    
    # Generate report
    report = generate_keyword_report(args.category, args.app_name, base_terms)
    
    # Save report
    if args.output:
        output_file = args.output
    else:
        safe_name = args.app_name.replace(' ', '_').lower()
        output_file = f"keywords_{safe_name}.md"
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Keyword report saved to: {output_file}")
    print(f"📊 Analyzed {len(base_terms)} base terms")
    print(f"🎯 Optimized keyword field: {len([c for c in report.split('Keyword Field (100 chars max)')[1].split('```')[1] if c != ',' and c != '\\n'])} chars")


if __name__ == '__main__':
    main()
