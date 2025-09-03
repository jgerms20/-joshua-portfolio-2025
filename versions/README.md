# Portfolio Version Management System

## 📁 Folder Structure

```
versions/
├── milestones/          # Major feature releases
├── daily_backups/       # End-of-day working versions
└── pre_change_backups/  # Safety backups before experimental changes
```

## 🎯 Version Management Protocol

### Before Making ANY Significant Changes:

1. **Create Pre-Change Backup:**
   ```bash
   cp index.html versions/pre_change_backups/before_[description]_$(date +%Y-%m-%d_%H%M%S).html
   ```

2. **After Completing Major Feature:**
   ```bash
   cp index.html versions/milestones/v[X.X]_[feature_description]/index.html
   ```

3. **Daily Backup (End of Session):**
   ```bash
   mkdir -p versions/daily_backups/$(date +%Y-%m-%d)
   cp index.html versions/daily_backups/$(date +%Y-%m-%d)/index_$(date +%H%M%S).html
   ```

## 📋 Version History

### v1.0 - Baseline Portfolio
**File:** `milestones/v1.0_baseline_portfolio/index.html`
**Date:** 2025-01-06 (from backup_20250601_095031)
**Description:** Starting point of the portfolio before major updates
**Features:**
- Original photography sections
- Initial skills section (word cloud format)
- Basic timeline
- Original campaign structure

### v1.1 - Photography Expansion
**File:** `milestones/v1.1_photography_expansion/index.html`
**Status:** ⚠️ Missing - Need to recreate
**Description:** Added new photos to all photography sections
**Changes:**
- **Landscape:** Added JMG_7535.jpg, JMG_7654.jpg, JMG_6496.jpg
- **Fashion:** Added JMG_4329.jpg, JMG_4324.jpg, JMG_4258.jpg, JMG_8986.jpg, JMG_3986.jpg, JMG_3729.jpg
- **Portraits:** Added JMG_1601.jpg, JMG_1430.jpg, JMG_1371.jpg, JMG_8928.jpg
- **Creative Spotlight:** New category with JMG_9553.jpg, JMG_8929.jpg, JMG_6994.jpg, JMG_6968.jpg

### v1.2 - Particles Bug Fix
**File:** `milestones/v1.2_particles_bugfix/index.html`
**Status:** ⚠️ Missing - Need to recreate
**Description:** Fixed critical loading issue
**Changes:**
- Fixed JavaScript syntax error in particles.js configuration
- Corrected malformed JSON structure in footer particles
- Resolved page stuck on "loading" issue

### v1.3 - Skills Section Redesign
**File:** `milestones/v1.3_skills_redesign/index.html`
**Status:** ⚠️ Missing - Need to recreate
**Description:** Replaced complex word cloud with clean grid layout
**Changes:**
- Removed word cloud visualization
- Implemented square-format display matching mini resume style
- Organized into 4 categories: Strategy, Creative, Digital, Innovation
- Used bullet-point format with clean grid layout

### v1.4 - Timeline Update
**File:** `milestones/v1.4_timeline_update/index.html`
**Status:** ⚠️ Missing - Need to recreate
**Description:** Updated work experience timeline
**Changes:**
- **2020-2023:** Jr. Communications Strategist at Goodby, Silverstein & Partners
- **2023-2024:** Comms + Media Supervisor at Wieden + Kennedy
- **2024-Present:** Senior Connections Strategist at TBWA\Chiat\Day

### v1.5 - Campaign Filter System
**File:** `milestones/v1.5_campaign_filters/index.html`
**Date:** 2025-01-06 (from backup_20250601_101542)
**Description:** Implemented campaign-specific filtering
**Changes:**
- Changed filter buttons from generic categories to specific campaign names
- Added filters: Levi's, Sephora, DoorDash, BMW, Califia, Sam Adams
- Fixed filtering functionality with proper data-filter attributes
- Added corresponding classes to brand cards
- Maintained "All" button for viewing all campaigns

### v1.6 - Current Working
**File:** `milestones/v1.6_current_working/index.html`
**Date:** 2025-01-06 (current)
**Description:** Latest working version ready for BMW updates
**Status:** 🟢 Ready for BMW section updates

## 🔄 Rollback Process

1. **Identify desired version** in appropriate folder
2. **Create backup of current version:**
   ```bash
   cp index.html versions/pre_change_backups/before_rollback_$(date +%Y-%m-%d_%H%M%S).html
   ```
3. **Copy chosen version back to root:**
   ```bash
   cp versions/milestones/[version_folder]/index.html index.html
   ```
4. **Test functionality** after rollback

## 📝 Quick Commands

### Create Pre-Change Backup
```bash
cp index.html versions/pre_change_backups/before_$(echo "DESCRIPTION_HERE")_$(date +%Y-%m-%d_%H%M%S).html
```

### Create Daily Backup
```bash
mkdir -p versions/daily_backups/$(date +%Y-%m-%d) && cp index.html versions/daily_backups/$(date +%Y-%m-%d)/index_$(date +%H%M%S).html
```

### Create Milestone Version
```bash
mkdir -p versions/milestones/v[X.X]_[description] && cp index.html versions/milestones/v[X.X]_[description]/index.html
```

## 🎨 Next Steps

- **BMW Section Update:** Add new images from Brand Imagery/BMW folder
- **Missing Versions:** Recreate intermediate versions if needed for specific rollback points
- **Documentation:** Update this README after each major milestone

---

**Last Updated:** 2025-01-06
**Current Version:** v1.6_current_working
**Next Planned:** BMW section enhancement 