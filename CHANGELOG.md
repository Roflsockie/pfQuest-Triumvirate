# Changelog

## 7.0.2-triumvirate-alpha (2026-07-08)

### Fixed
- **Quest log level display rewritten**: removed all conflicting hooks and text manipulation.
  Global `GetQuestLogTitle` override in `compat/client.lua` is now the single source of
  squished levels — Blizzard and all addons get correct levels automatically.
- **No more double level prefix / missing names**: removed `hooksecurefunc` on
  `QuestLogTitleButton_Resize`, button text iteration in `QuestLog_Update`, and
  `FixQuestLogButtonLevel` helper. Text is left entirely to native code.
- **Compatibility with ElvUI Enhanced**: global override works correctly regardless
  of whether ElvUI Enhanced's `showQuestLevel` is enabled or disabled.
- **Dead code cleanup**: removed unused `SquishLevel` helper from quest.lua.
- **build_scaled fix**: now reads `.orig` source files instead of already-baked DB
  (previously caused double-squishing of quest levels like 10057→10→10).

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
