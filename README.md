# Dustloop_Scraping

Converts Dustloop's character info into a json format that is exportable into a json file.

# Usage

1. Clone the repository into a local file.
2. Run the command `python scrape.py ([character_name] or [any dustloop character link])` in the src directory of this repository.

The `character_name` can be any GGST strive.

### Valid Strive Characters (09/12/2021)
- Anji_Mito
- Axl_Low
- Chipp_Zanuff
- Faust
- Giovanna
- Goldlewis_Dickinson
- Happy_Chaos
- I-No
- Jack-O
- Ky_Kiske
- Leo_Whitefang
- May
- Millia_Rage
- Nagoriyuki
- Potemkin
- Ramlethal_Valentine
- Sol_Badguy
- Zato-1

Alternatively a full hyperlink to the character page of any series can be provided.(Note that due to varied differences between series, the scraper may not collect everything correctly).

e.g. `python scrape.py https://www.dustloop.com/wiki/index.php?title=GGXRD-R2/Dizzy`

# Scraped Data

### Character Overview
- Lore
- Voice
- Playstyle
- Pros
- Cons

### General Info
- Character Name
- Game-related stats

### Moves
- Name
- Images and hitboxes
- Frame Data
- Notes (formatting preserved under raw_notes)
