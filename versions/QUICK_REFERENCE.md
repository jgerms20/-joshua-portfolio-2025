# 🚀 Quick Version Management Reference

## Most Common Commands

### Before Making Changes
```bash
./versions/version_manager.sh pre-backup [description]
```
**Example:** `./versions/version_manager.sh pre-backup bmw_update`

### After Completing Feature
```bash
./versions/version_manager.sh milestone [version_name]
```
**Example:** `./versions/version_manager.sh milestone v1.7_bmw_complete`

### End of Day Backup
```bash
./versions/version_manager.sh daily
```

### See All Versions
```bash
./versions/version_manager.sh list
```

### Rollback to Previous Version
```bash
./versions/version_manager.sh rollback [version_folder]
```
**Example:** `./versions/version_manager.sh rollback v1.5_campaign_filters`

### Check Status
```bash
./versions/version_manager.sh status
```

## 📋 Current Version Tracking

**Latest:** v1.6_current_working  
**Next:** v1.7_bmw_update (planned)

## 🎯 Workflow

1. **Before changes:** `pre-backup [description]`
2. **Make your changes**
3. **Test thoroughly**
4. **After completion:** `milestone [version]`
5. **End of day:** `daily`

---
*Keep this file handy for quick reference!* 