# Changelog

## 7.0.1-triumvirate-alpha (2026-07-08)

### Added
- Squished (1–60) quest level database (build_scaled tool)
- Global `GetQuestLogTitle` override returning squished levels from database
- Reapply timer to protect quest log level text from late overwrites

### Fixed
- Tracker now shows correct squished quest levels (via `self.questid` → DB lookup)
- Quest log now shows correct squished quest levels and difficulty colour
- Tooltips use squished levels from baked database (already correct in upstream)

### Removed
- pfQuest-Scaled60 hook addon (no longer needed)
- All retail/Cataclysm+ API dependencies
