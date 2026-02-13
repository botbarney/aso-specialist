# ASO Specialist Skill

**Name:** aso-specialist  
**Version:** 1.0.0  
**Author:** OpenClaw  

## Description

Complete ASO automation for iOS apps. Research competitors, optimize keywords, generate screenshots, track rankings, improve conversion rates. Handles all app marketing so developers can focus on building.

This skill takes the pain out of App Store Optimization by automating the research, analysis, and content generation that would normally take hours of manual work.

## When to Use

- User mentions ASO or App Store optimization
- Need to create or update app screenshots
- Researching keywords for an app
- App marketing or competitor analysis
- Improving app downloads or conversion rates
- Preparing for App Store submission
- Writing app descriptions or metadata

## Installation

```bash
cd /Users/barneystinson/.openclaw/workspace/skills/aso-specialist
pip install -r scripts/requirements.txt
```

## Scripts

### 1. Competitor Research
```bash
python scripts/competitor_research.py --category "baby tracker" --output report.md
```

Searches App Store for competitor apps, analyzes their metadata, screenshots, pricing, and generates a gap analysis report.

### 2. Keyword Tracker
```bash
python scripts/keyword_tracker.py --category "baby tracker" --app-name "TotTracker"
```

Researches high-volume keywords, finds long-tail opportunities, and generates an optimized keyword list ready for App Store Connect.

### 3. Screenshot Generator
```bash
python scripts/screenshot_generator.py --app-name "TotTracker" --features "feeding tracking,sleep monitoring,growth charts"
```

Generates screenshot concepts, text overlays, dimensions for all iPhone sizes, and design direction.

### 4. Metadata Optimizer
```bash
python scripts/metadata_optimizer.py --app-name "TotTracker" --category "baby tracker" --keywords "feeding,baby,sleep"
```

Optimizes all App Store metadata: title, subtitle, keywords, promotional text, and full description.

## Quick Start

Run complete ASO analysis for your app:

```bash
cd /Users/barneystinson/.openclaw/workspace/skills/aso-specialist

# 1. Research competitors
python scripts/competitor_research.py --category "your category" --output competitors.md

# 2. Generate keywords  
python scripts/keyword_tracker.py --category "your category" --app-name "YourApp"

# 3. Create screenshot concepts
python scripts/screenshot_generator.py --app-name "YourApp" --features "feature1,feature2,feature3"

# 4. Optimize all metadata
python scripts/metadata_optimizer.py --app-name "YourApp" --category "your category"
```

## Output Files

All scripts generate markdown reports in the current directory:
- `competitor_analysis_*.md` - Competitor research report
- `keywords_*.md` - Optimized keyword list
- `screenshots_*.md` - Screenshot strategy document
- `metadata_*.md` - Complete metadata package

## References

- `references/aso_best_practices.md` - Ranking factors and CRO tips
- `references/app_store_guidelines.md` - Apple's official requirements
- `references/marketing_templates.md` - Templates by app category

## Tips for Best Results

1. **Be specific with categories** - "baby tracker" is better than "lifestyle"
2. **List all features** - The more features you provide, the better the screenshot concepts
3. **Iterate on keywords** - Run keyword research multiple times with variations
4. **Check character limits** - Scripts enforce limits but always double-check
5. **Localize** - Use the metadata optimizer for each target market

## Limitations

- Web scraping is used for competitor research (may need updates if App Store changes)
- Keyword volume estimates are approximate (based on search trends)
- Screenshot concepts require designer implementation
- Does not automate actual App Store Connect uploads

## Future Enhancements

- Integration with App Store Connect API
- Automated A/B test result tracking
- Real-time keyword ranking monitoring
- AI-powered screenshot generation
- Competitor price change alerts
