#!/usr/bin/env python3
"""
Competitor Research Script for ASO
Searches App Store for competitors and generates gap analysis
"""

import argparse
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any


def search_app_store(term: str, limit: int = 50) -> List[Dict]:
    """Search iTunes/App Store for apps matching the term"""
    url = f"https://itunes.apple.com/search?term={urllib.parse.quote(term)}&entity=software&limit={limit}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get('results', [])
    except Exception as e:
        print(f"Error searching App Store: {e}")
        return []


def analyze_app(app: Dict) -> Dict[str, Any]:
    """Extract key ASO data from an app"""
    return {
        'name': app.get('trackName', 'N/A'),
        'developer': app.get('artistName', 'N/A'),
        'description': app.get('description', ''),
        'primary_genre': app.get('primaryGenreName', 'N/A'),
        'genres': app.get('genres', []),
        'price': app.get('formattedPrice', 'Free'),
        'price_usd': app.get('price', 0),
        'average_user_rating': app.get('averageUserRating', 0),
        'user_rating_count': app.get('userRatingCount', 0),
        'current_version': app.get('version', 'N/A'),
        'release_date': app.get('releaseDate', 'N/A'),
        'current_version_release_date': app.get('currentVersionReleaseDate', 'N/A'),
        'screenshot_urls': app.get('screenshotUrls', []),
        'ipad_screenshot_urls': app.get('ipadScreenshotUrls', []),
        'icon_url': app.get('artworkUrl100', ''),
        'content_advisory_rating': app.get('contentAdvisoryRating', ''),
        'track_view_url': app.get('trackViewUrl', ''),
        'bundle_id': app.get('bundleId', ''),
        'features': app.get('features', []),
        'supported_devices': app.get('supportedDevices', []),
        'minimum_os_version': app.get('minimumOsVersion', ''),
    }


def extract_keywords_from_text(text: str) -> List[str]:
    """Extract potential keywords from app description"""
    # Common stop words to filter out
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
                  'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
                  'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
                  'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his',
                  'her', 'its', 'our', 'their', 'app', 'application', 'ios', 'iphone', 'ipad'}
    
    # Clean and split text
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter and count
    word_counts = {}
    for word in words:
        if word not in stop_words and len(word) > 3:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    # Return top keywords sorted by frequency
    return sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]


def analyze_pricing(apps: List[Dict]) -> Dict[str, Any]:
    """Analyze pricing strategies of competitors"""
    prices = [app.get('price', 0) for app in apps]
    free_apps = sum(1 for p in prices if p == 0)
    paid_apps = len(prices) - free_apps
    avg_price = sum(prices) / len(prices) if prices else 0
    
    price_ranges = {
        'free': free_apps,
        '0.99-2.99': sum(1 for p in prices if 0 < p <= 2.99),
        '3.00-9.99': sum(1 for p in prices if 3.00 <= p <= 9.99),
        '10.00+': sum(1 for p in prices if p >= 10.00)
    }
    
    return {
        'total_analyzed': len(prices),
        'free_percentage': round(free_apps / len(prices) * 100, 1) if prices else 0,
        'paid_percentage': round(paid_apps / len(prices) * 100, 1) if prices else 0,
        'average_price': round(avg_price, 2),
        'price_distribution': price_ranges
    }


def analyze_ratings(apps: List[Dict]) -> Dict[str, Any]:
    """Analyze rating patterns"""
    ratings = [app.get('averageUserRating', 0) for app in apps if app.get('averageUserRating')]
    review_counts = [app.get('userRatingCount', 0) for app in apps if app.get('userRatingCount')]
    
    if not ratings:
        return {'error': 'No rating data available'}
    
    return {
        'average_rating': round(sum(ratings) / len(ratings), 2),
        'highest_rating': round(max(ratings), 1),
        'lowest_rating': round(min(ratings), 1),
        'total_reviews_analyzed': sum(review_counts),
        'apps_with_4_plus_stars': sum(1 for r in ratings if r >= 4.0),
        'apps_with_3_plus_stars': sum(1 for r in ratings if r >= 3.0),
    }


def generate_gap_analysis(apps: List[Dict], category: str) -> List[str]:
    """Identify gaps and opportunities in the market"""
    gaps = []
    
    # Check for common features mentioned
    all_descriptions = ' '.join([app.get('description', '').lower() for app in apps[:10]])
    
    # Look for missing elements
    if 'dark mode' not in all_descriptions and 'darkmode' not in all_descriptions:
        gaps.append("🌙 **Dark Mode**: Many modern apps support dark mode - opportunity to stand out")
    
    if 'widget' not in all_descriptions:
        gaps.append("📱 **iOS Widgets**: Home screen widgets are popular but may be underutilized")
    
    if 'siri' not in all_descriptions:
        gaps.append("🎙️ **Siri Shortcuts**: Voice control integration could be a differentiator")
    
    if 'apple watch' not in all_descriptions and 'applewatch' not in all_descriptions:
        gaps.append("⌚ **Apple Watch**: Companion watch app could expand reach")
    
    if 'sync' not in all_descriptions or 'icloud' not in all_descriptions:
        gaps.append("☁️ **Cloud Sync**: Cross-device synchronization highly valued by users")
    
    if 'export' not in all_descriptions:
        gaps.append("📤 **Data Export**: Users increasingly want data portability")
    
    if 'family' not in all_descriptions and 'share' not in all_descriptions:
        gaps.append("👨‍👩‍👧‍👦 **Family Sharing**: Enable multiple family members to use the app")
    
    # Pricing gaps
    prices = [app.get('price', 0) for app in apps]
    if all(p == 0 for p in prices[:10]):
        gaps.append("💰 **Premium Option**: All top competitors are free - opportunity for premium paid features")
    
    return gaps


def generate_report(category: str, apps: List[Dict], output_file: str):
    """Generate markdown report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    analyzed_apps = [analyze_app(app) for app in apps[:20]]
    pricing_analysis = analyze_pricing(apps[:20])
    rating_analysis = analyze_ratings(apps[:20])
    gaps = generate_gap_analysis(apps, category)
    
    report = f"""# Competitor Analysis Report: {category.title()}

**Generated:** {timestamp}  
**Apps Analyzed:** {len(analyzed_apps)}  
**Category:** {category.title()}

---

## 📊 Market Overview

### Pricing Strategy
| Metric | Value |
|--------|-------|
| Free Apps | {pricing_analysis['free_percentage']}% |
| Paid Apps | {pricing_analysis['paid_percentage']}% |
| Average Price | ${pricing_analysis['average_price']} |

### Rating Landscape
| Metric | Value |
|--------|-------|
| Average Rating | {rating_analysis.get('average_rating', 'N/A')} ⭐ |
| Highest Rated | {rating_analysis.get('highest_rating', 'N/A')} ⭐ |
| Apps with 4+ Stars | {rating_analysis.get('apps_with_4_plus_stars', 'N/A')} |

---

## 🏆 Top Competitors

"""
    
    # Add top 10 competitors
    for i, app in enumerate(analyzed_apps[:10], 1):
        keywords = extract_keywords_from_text(app['description'])[:5]
        keyword_str = ', '.join([k[0] for k in keywords])
        
        report += f"""### {i}. {app['name']}
- **Developer:** {app['developer']}
- **Price:** {app['price']}
- **Rating:** {app['average_user_rating']} ⭐ ({app['user_rating_count']} reviews)
- **Keywords:** {keyword_str}
- **App Store:** [View]({app['track_view_url']})

"""
    
    # Add gap analysis
    report += """---

## 🎯 Gap Analysis & Opportunities

"""
    for gap in gaps:
        report += f"- {gap}\n"
    
    # Add screenshot analysis section
    report += """
---

## 📸 Screenshot Strategy Insights

### Common Patterns in Top Apps:
1. **First Screenshot:** Shows core value proposition clearly
2. **Feature Highlights:** 3-5 key features shown across screenshots
3. **Text Overlays:** Concise benefit-driven text on each image
4. **Lifestyle vs UI:** Mix of real usage and interface shots

### Recommendations:
- Lead with the "aha moment" - what makes users download?
- Show real data/screens, not just empty states
- Use consistent branding (colors, fonts) across all screenshots
- Localize screenshots for each target market

---

## 📝 Action Items

1. [ ] Analyze top 3 competitors in detail
2. [ ] Identify unique value proposition vs competition
3. [ ] Review competitor keywords for inspiration
4. [ ] Benchmark pricing strategy
5. [ ] Plan screenshot differentiation
6. [ ] Set up review monitoring for competitors

---

*Report generated by ASO Specialist Skill*
"""
    
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved to: {output_file}")
    return report


def main():
    parser = argparse.ArgumentParser(description='Research App Store competitors')
    parser.add_argument('--category', required=True, help='App category to research (e.g., "baby tracker")')
    parser.add_argument('--output', default=None, help='Output file path')
    parser.add_argument('--limit', type=int, default=50, help='Number of apps to analyze')
    
    args = parser.parse_args()
    
    print(f"🔍 Researching competitors for: {args.category}")
    print("⏳ Searching App Store...")
    
    apps = search_app_store(args.category, args.limit)
    
    if not apps:
        print("❌ No apps found. Try a different search term.")
        return
    
    print(f"✅ Found {len(apps)} apps")
    
    if args.output:
        output_file = args.output
    else:
        safe_category = args.category.replace(' ', '_').lower()
        output_file = f"competitor_analysis_{safe_category}.md"
    
    generate_report(args.category, apps, output_file)
    print(f"\n📄 Full report saved to: {output_file}")


if __name__ == '__main__':
    main()
