# Changelog

## 7.1.0-triumvirate-alpha (2026-07-09)

### Added
- **Wrath of the Lich King (Northrend) quest database**: 2,761 quests, 1,970 NPCs (1,557 with coords, 8,342 spawn points), and objects converted from Questie-335.
- **Northrend zone locale entries** for `GetMapID` compatibility — quest markers now appear on the world map and minimap in all Northrend zones (Borean Tundra, Howling Fjord, Dragonblight, Grizzly Hills, Zul'Drak, Sholazar Basin, Storm Peaks, Icecrown, Wintergrasp, etc.).
- **Quest level squishing for WotLK**: levels 68–80 are compressed to 51–60 using `ceil(lvl × 60 / 80)`, consistent with existing TBC squishing.
- **`build/convert_wotlk.js`**: converter script that extracts WotLK data from Questie-335 and outputs pfQuest-format files with automatic logging (`logs/convert-wotlk-*.txt`).

### Fixed
- **Northrend quests filtered out on the map**: `race=0` in quest data caused all WotLK quests to be hidden by `QuestFilter` (Lua treats `0` as truthy). Removed `race=0` / `class=0` entries from generated data.
- **ElvUI Enhanced conflict popup**: removed StaticPopup that warned about duplicate quest levels (no longer needed — ElvUI fixed upstream).

### Changed
- **.toc**: added `init\data-wotlk.xml` and `init\enUS-wotlk.xml` include entries for WotLK data loading.
- **`database.lua`**: existing `-wotlk` patching loop (already present) now activates with the new data files — no code changes needed.

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
