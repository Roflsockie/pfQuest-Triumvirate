# pfQuest [Triumvirate]

**Fork of [pfQuest](https://github.com/shagu/pfQuest) — rebranded for the Triumvirate private server (WoW 3.3.5a WotLK).**

This version adapts pfQuest to servers with squished (1–60) quest levels. All quest levels displayed in the tracker, quest log, map, browser, and tooltips are scaled down from the original 1–80 range to match the server's 1–60 progression.

## Changes from Upstream

- **Squished quest levels** — Map, browser, and tooltips use a baked database with 1–60 scaled levels
- **Tracker fix** — Quest level overridden from database (by `self.questid`)
- **Quest log fix** — `GetQuestLogTitle` globally overridden to return squished levels; level text reapplied after each update to prevent overwrites
- **Removed hook addon dependency** — No external addons required; all patches are in-file
- **Alpha stage** — Quest log colour now correct, level text may still have edge cases

## Installation

1. Download the latest release
2. Extract the `pfQuest-Triumvirate` folder into `World of Warcraft\Interface\AddOns\`
3. Restart WoW (or log out completely)

## Requirements

- World of Warcraft 3.3.5a (WotLK)
- [pfUI-wotlk](https://github.com/shagu/pfUI-wotlk) (optional, for enhanced UI)

## Credits

- **Shagu** — Original pfQuest author
- **-Neayo-** — Triumvirate fork maintainer

## License

This project is licensed under the same terms as the original pfQuest.
