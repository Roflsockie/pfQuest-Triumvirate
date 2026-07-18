# Changelog

## 7.2.2-triumvirate-alpha (2026-07-18)

### Fixed
- **Quest data contamination**: `quests-wotlk.lua` contained 757 quests that also existed in vanilla/TBC data, overwriting correct level data via `patchtable()`. Filtered to keep only 2,004 WotLK-exclusive quests (IDs >= 11116).
- **Missing WotLK database files**: created stub files for `areatrigger-wotlk.lua`, `meta-wotlk.lua`, `refloot-wotlk.lua`, `minimap-wotlk.lua`, `quests-itemreq-wotlk.lua` — all 11 database types now have WotLK data entries.
- **Missing `professions-wotlk.lua`**: WotLK profession skill names (Jewelcrafting, Inscription, Riding) now loaded for profession-gated quests.
- **`init/data-wotlk.xml` incomplete**: updated from 5 to 10 includes, matching TBC's completeness.
- **`init/enUS-wotlk.xml` incomplete**: added `professions-wotlk.lua` include.
- **`db/init.lua` missing WotLK keys**: added `meta-wotlk` and `minimap-wotlk` entries to prevent nil errors during patching.

## 7.2.1-triumvirate-alpha (2026-07-18)

### Fixed
- **Outland quests not showing on map**: `enUS/zones-wotlk.lua` contained entries with zone IDs
  that belong to TBC zones (3430=Eversong Woods, 3433=Ghostlands, 3483=Hellfire Peninsula,
  3518=Nagrand, 3520=Zangarmarsh, 3521=Terokkar Forest, 3524=Blade's Edge Mountains).
  The `-wotlk` patching pass overwrote correct TBC zone names with WotLK names, breaking
  zone lookups for all Outland content. Removed conflicting entries.
- **Northrend zone coordinate data missing**: `db/zones-wotlk.lua` did not exist — only locale
  names were present in `enUS/zones-wotlk.lua`. Without zone coordinate data (parent map,
  width, height, x, y), `SearchZoneID()` could not position any Northrend zone markers on
  the world map. Created `db/zones-wotlk.lua` with coordinate data for all Northrend zones
  and subzones.
- **`init/data-wotlk.xml` missing zones include**: Added `zones-wotlk.lua` to the WotLK
  data loading XML so the zone coordinate data is loaded at startup.
- **`client.lua` GetQuestLogTitle override not checking WotLK data**: Added `data-wotlk`
  as a third fallback lookup after `data-tbc`, ensuring squished WotLK quest levels are
  used even when the main `data` table doesn't have the entry.

## 7.2.0-triumvirate-alpha (2026-07-09)

### Added
- **Minimap support for Northrend zones**: `UpdateMinimap` no longer requires `minimap_sizes[mapID]` — uses fallback `{6000, 4500}` for zones without minimap data. Fixes object markers (gear icons) not showing on the minimap in Borean Tundra, Howling Fjord, Dragonblight, etc.
- **`/pfquest debug minimap` command**: prints current config values (`showspawnmini`, `showspawn`, `showclustermini`, `minimapnodes`), zone mapID, node counts, and visible pin count for debugging minimap issues.
- **Quest level display on quest log**: new `hooksecurefunc`-based implementation with dual lookup — `QuestLogScrollFrame.buttons` (ElvUI style) or `_G["QuestLogTitleButton"..i]` fallback (stock WotLK). Includes scrollbar `HookScript` for live updates on scroll.
- **ElvUI Enhanced conflict detection popup**: when both pfQuest's `questloglevel` and ElvUI's `showQuestLevel` are enabled, a popup lets the user choose which one to keep.

### Fixed
- **Minimap markers sliding at different zoom levels**: replaced zoom-dependent `mapZoom * 20` fallback with constant `{6000, 4500}` — markers now stay in place regardless of zoom.
- **`SetPortraitToTexture(nil)` crash in LFD**: deferred `PlayerModel.SetPortraitToTexture` hook via `ADDON_LOADED` event + `pcall` fallback on `LFDDungeonReadyDialogReward_SetReward`.
- **`questloglevel` nil scrollFrame crash**: added nil-guard for when `QuestLog_Update` is called by ElvUI before the scroll frame exists.
- **Double `local btn` variable shadow** in quest log level fallback path — cleaned up.
- **Object coordinate parsing**: wotlkObjectDB spawns stored in field 4, not field 7 — now 93 objects with real coordinates appear on the map.

### Changed
- **questloglevel rewritten**: multiple iterations to resolve ElvUI hook conflicts, culminating in hybrid `QuestLogScrollFrame.buttons` + `_G["QuestLogTitleButton"..i]` approach.
- **Minimap code in `map.lua`**: removed `minimap_sizes[mapID]` requirement from zone iteration — any zone with node data renders minimap pins regardless of database entries.
- **Quest text fallback cleaned up**: removed redundant `_G[GetName()]` expression, uses simpler `btn:GetFontString()` fallback.

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
