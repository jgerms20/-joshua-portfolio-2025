#!/bin/bash

# Portfolio Version Manager
# Usage: ./version_manager.sh [command] [description]

case "$1" in
    "pre-backup")
        if [ -z "$2" ]; then
            echo "Usage: ./version_manager.sh pre-backup [description]"
            echo "Example: ./version_manager.sh pre-backup bmw_update"
            exit 1
        fi
        filename="before_${2}_$(date +%Y-%m-%d_%H%M%S).html"
        cp index.html "versions/pre_change_backups/$filename"
        echo "✅ Pre-change backup created: $filename"
        ;;
    
    "daily")
        mkdir -p "versions/daily_backups/$(date +%Y-%m-%d)"
        filename="index_$(date +%H%M%S).html"
        cp index.html "versions/daily_backups/$(date +%Y-%m-%d)/$filename"
        echo "✅ Daily backup created: $(date +%Y-%m-%d)/$filename"
        ;;
    
    "milestone")
        if [ -z "$2" ]; then
            echo "Usage: ./version_manager.sh milestone [version_description]"
            echo "Example: ./version_manager.sh milestone v1.7_bmw_update"
            exit 1
        fi
        mkdir -p "versions/milestones/$2"
        cp index.html "versions/milestones/$2/index.html"
        echo "✅ Milestone created: $2"
        echo "📝 Don't forget to update versions/README.md with the changes!"
        ;;
    
    "rollback")
        if [ -z "$2" ]; then
            echo "Available versions:"
            ls -la versions/milestones/
            echo ""
            echo "Usage: ./version_manager.sh rollback [version_folder]"
            echo "Example: ./version_manager.sh rollback v1.5_campaign_filters"
            exit 1
        fi
        
        if [ ! -d "versions/milestones/$2" ]; then
            echo "❌ Version $2 not found!"
            exit 1
        fi
        
        # Create backup before rollback
        backup_name="before_rollback_to_${2}_$(date +%Y-%m-%d_%H%M%S).html"
        cp index.html "versions/pre_change_backups/$backup_name"
        echo "✅ Current version backed up as: $backup_name"
        
        # Perform rollback
        cp "versions/milestones/$2/index.html" index.html
        echo "✅ Rolled back to: $2"
        echo "🧪 Please test the site functionality!"
        ;;
    
    "list")
        echo "📁 Available Versions:"
        echo ""
        echo "🎯 Milestones:"
        ls -la versions/milestones/ | grep "^d" | awk '{print "  " $9}' | grep -v "^\.$" | grep -v "^\.\.$"
        echo ""
        echo "📅 Recent Daily Backups:"
        ls -la versions/daily_backups/ 2>/dev/null | tail -5 | grep "^d" | awk '{print "  " $9}' | grep -v "^\.$" | grep -v "^\.\.$"
        echo ""
        echo "🔒 Recent Pre-Change Backups:"
        ls -la versions/pre_change_backups/ 2>/dev/null | tail -5 | awk '{print "  " $9}' | grep -v "^\.$" | grep -v "^\.\.$"
        ;;
    
    "status")
        echo "📊 Portfolio Version Status"
        echo "=========================="
        echo "Current working file: index.html ($(stat -f%z index.html 2>/dev/null || echo 'unknown') bytes)"
        echo "Last modified: $(stat -f%Sm index.html 2>/dev/null || echo 'unknown')"
        echo ""
        echo "Total versions: $(find versions/milestones -name "index.html" | wc -l | tr -d ' ')"
        echo "Daily backups: $(find versions/daily_backups -name "*.html" 2>/dev/null | wc -l | tr -d ' ')"
        echo "Pre-change backups: $(find versions/pre_change_backups -name "*.html" 2>/dev/null | wc -l | tr -d ' ')"
        ;;
    
    *)
        echo "🎯 Portfolio Version Manager"
        echo "============================"
        echo ""
        echo "Commands:"
        echo "  pre-backup [description]     Create backup before making changes"
        echo "  daily                        Create end-of-day backup"
        echo "  milestone [version_name]     Create milestone version"
        echo "  rollback [version_folder]    Rollback to specific version"
        echo "  list                         Show all available versions"
        echo "  status                       Show version statistics"
        echo ""
        echo "Examples:"
        echo "  ./version_manager.sh pre-backup bmw_update"
        echo "  ./version_manager.sh milestone v1.7_bmw_complete"
        echo "  ./version_manager.sh rollback v1.5_campaign_filters"
        echo "  ./version_manager.sh daily"
        ;;
esac 