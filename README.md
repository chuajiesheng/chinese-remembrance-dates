# Chinese Memorial Dates Calendar Generator

A Python tool for generating calendar files (ICS) for traditional Chinese memorial dates, including both solar and lunar calendar events. This tool helps families keep track of important memorial dates and traditional observances.

## Note on Generation

This project's documentation and codebase were generated with the assistance of Claude 3.5 Sonnet (October 2024 version). While the core functionality has been verified, it's recommended to:
- Review and test the code thoroughly before use
- Check for updated dependencies and security patches
- Modify the code and documentation to match your specific needs

## Version

Current version: 0.1.0
- Initial release with basic calendar generation functionality
- Supports both solar and lunar calendar events
- Custom anniversary support via YAML configuration

## Features

- Generates ICS calendar files compatible with Google Calendar, Apple Calendar, and other calendar applications
- Supports both solar and lunar calendar dates
- Includes major traditional observances:
  - Qingming Festival (清明节)
  - Winter Solstice (冬至)
  - Hungry Ghost Festival (中元节)
  - Chinese New Year's Eve (除夕)
- Supports custom death anniversaries through YAML configuration
- Generates both individual event files and a combined calendar

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code:
```bash
git clone [your-repository-url]
cd chinese-memorial-calendar
```

2. Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install ics pytz pyyaml lunarcalendar
```

## Configuration

1. Create a `anniversaries.yml` file in the project directory with your custom anniversaries:

```yaml
anniversaries:
  - name: "Grandfather Zhang"
    chinese_name: "张爷爷"
    lunar_month: 3
    lunar_day: 15
    notes: "Annual family gathering day"
  
  - name: "Grandmother Li"
    chinese_name: "李奶奶"
    lunar_month: 7
    lunar_day: 21
    notes: "Favorite flowers: chrysanthemums"
```

## Usage

### Basic Usage

Generate calendar files for the current year:
```bash
python chinese_memorial_calendar.py
```

### Advanced Usage

Generate calendar files for a specific year:
```bash
python chinese_memorial_calendar.py --year 2025
```

Specify a custom output directory:
```bash
python chinese_memorial_calendar.py --output-dir my_calendars
```

Use a different configuration file:
```bash
python chinese_memorial_calendar.py --config my_anniversaries.yml
```

## Output

The script generates the following ICS files in the output directory:

- Individual event files:
  - `qingming.ics`
  - `winter_solstice.ics`
  - `ghost_festival.ics`
  - `chinese_new_year_eve.ics`
  - Individual anniversary files for each configured memorial date
- Combined calendar file: `all_events_[YEAR].ics`

## Importing Calendar Files

1. Google Calendar:
   - Go to Settings > Add Calendar > Import
   - Select the generated ICS file
   - Choose the destination calendar

2. Apple Calendar:
   - File > Import
   - Select the generated ICS file
   - Choose the destination calendar

3. Other Calendar Applications:
   - Most calendar applications support importing ICS files
   - Look for an "Import" or "Add Calendar" option

## Traditional Offerings Reference

The calendar events include reminders for traditional offerings:
- Incense (香)
- Fresh flowers (鲜花)
- Food offerings (食品)
- Joss paper (纸钱)
- Fruits (水果)
- Tea (茶)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

Please see the LICENSE file in the repository for license information.

## Acknowledgments

- Built using the `ics` library for calendar generation
- Uses `lunarcalendar` for lunar date conversions
- Inspired by traditional Chinese memorial practices

## Support

For questions or issues, please [open an issue](/../../issues) on the repository.