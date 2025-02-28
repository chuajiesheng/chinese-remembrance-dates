import os
from datetime import datetime, timedelta

import ics
import yaml
from lunarcalendar import Converter, Solar, Lunar
from typing import List, Optional, Tuple


class ChineseMemorialCalendar:
    def __init__(self, year: int, output_dir: str = "calendar_events"):
        self.year = year
        self.timezone = datetime.now().astimezone().tzinfo  # Get local timezone
        self.anniversaries = []
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def _create_multiday_event(self, name: str, start_date: datetime, end_date: datetime,
                               description: str) -> ics.Event:
        """Create a multi-day ICS event with the given parameters."""
        event = ics.Event()
        event.name = name
        # Set as all-day event starting from start_date
        event.begin = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        # End date should be the day after the last day (as per iCal spec)
        event.end = (end_date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        event.make_all_day()
        event.description = description
        return event

    def _create_event(self, name: str, date: datetime, description: str) -> ics.Event:
        """Create an ICS event with the given parameters."""
        event = ics.Event()
        event.name = name
        # Set as all-day event by setting begin to midnight and making it a 24-hour duration
        event.begin = date.replace(hour=0, minute=0, second=0, microsecond=0)
        event.make_all_day()
        event.description = description
        return event

    def _solar_to_lunar(self, solar_date: datetime) -> Lunar:
        """Convert solar date to lunar date."""
        solar = Solar(solar_date.year, solar_date.month, solar_date.day)
        return Converter.Solar2Lunar(solar)

    def _lunar_to_solar(self, lunar_month: int, lunar_day: int, year: Optional[int] = None) -> datetime:
        """Convert lunar date to solar date.

        Args:
            lunar_month: The lunar month
            lunar_day: The lunar day
            year: Optional year (defaults to self.year if not provided)
        """
        year = year or self.year
        lunar_date = Lunar(year, lunar_month, lunar_day)
        solar_date = Converter.Lunar2Solar(lunar_date)
        return datetime(solar_date.year, solar_date.month, solar_date.day,
                        tzinfo=self.timezone)

    def _save_event_to_file(self, event: ics.Event, filename: str) -> str:
        """Save a single event to an ICS file."""
        calendar = ics.Calendar()
        calendar.events.add(event)

        print(event.name, ':', event.begin.date())

        filepath = os.path.join(self.output_dir, filename.replace(',', ''))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(calendar.serialize()))
        return filepath

    def generate_solar_calendar_events(self) -> List[Tuple[str, ics.Event]]:
        """Generate events for fixed solar calendar dates."""
        events = []

        # Qingming Festival (April 5th)
        qingming_date = datetime(self.year, 4, 5, tzinfo=self.timezone)
        qingming_desc = (
            "清明节 - Qingming Festival\n"
            "Traditional tomb sweeping and ancestral worship day.\n"
            "Traditional offerings include:\n"
            "- Incense (香)\n"
            "- Fresh flowers (鲜花)\n"
            "- Food offerings (食品)"
        )
        events.append(("qingming.ics",
                       self._create_event("Qingming Festival 清明节", qingming_date, qingming_desc)))

        # Winter Solstice
        winter_solstice_date = datetime(self.year, 12, 22, tzinfo=self.timezone)
        winter_solstice_desc = (
            "冬至 - Winter Solstice\n"
            "Traditional family reunion day with ancestral remembrance.\n"
            "Common practices include family gathering and special meals."
        )
        events.append(("winter_solstice.ics",
                       self._create_event("Winter Solstice 冬至", winter_solstice_date, winter_solstice_desc)))

        return events

    def generate_lunar_calendar_events(self) -> List[Tuple[str, ics.Event]]:
        """Generate events for lunar calendar dates."""
        events = []

        # Hungry Ghost Festival Month (7th lunar month)
        ghost_month_start = self._lunar_to_solar(7, 1)  # First day of 7th month
        ghost_month_end = self._lunar_to_solar(7, 30)  # Last day of 7th month
        ghost_festival_desc = (
            "中元节 - Ghost Month (鬼月)\n"
            "The entire 7th lunar month is the Ghost Month, with the 15th day being the Ghost Festival peak.\n"
            "Traditional practices include:\n"
            "- Making offerings to ancestors and wandering spirits\n"
            "- Burning joss paper and incense\n"
            "- Avoiding major life changes or events\n\n"
            "Peak Day (15th): 中元节\n"
            "Traditional offerings include:\n"
            "- Incense (香)\n"
            "- Food offerings (食品)\n"
            "- Joss paper (纸钱)\n"
            "- Fruits (水果)\n"
            "- Tea (茶)"
        )
        events.append(("ghost_month.ics",
                       self._create_multiday_event("Ghost Month 鬼月",
                                                   ghost_month_start,
                                                   ghost_month_end,
                                                   ghost_festival_desc)))

        # Chinese New Year's Eve
        # Get the first day of the next lunar year and subtract one day
        nye_date = self._lunar_to_solar(1, 1, self.year) - timedelta(days=1)

        nye_desc = (
            "除夕 - Chinese New Year's Eve\n"
            "Traditional family reunion dinner.\n"
            "Custom includes leaving an empty seat and chopsticks for deceased family members.\n"
            "Traditional practices include:\n"
            "- Family reunion dinner\n"
            "- Ancestral worship\n"
            "- Setting out offerings"
        )
        events.append(("chinese_new_year_eve.ics",
                       self._create_event("Chinese New Year's Eve 除夕",
                                          nye_date, nye_desc)))

        return events

    def load_anniversaries_config(self, config_file: str) -> None:
        """Load death anniversaries from a YAML configuration file."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            if not config or 'anniversaries' not in config:
                print("Warning: No anniversaries found in config file")
                return

            for anniversary in config['anniversaries']:
                try:
                    self.anniversaries.append({
                        'name': anniversary['name'],
                        'chinese_name': anniversary.get('chinese_name', ''),
                        'lunar_month': anniversary['lunar_month'],
                        'lunar_day': anniversary['lunar_day'],
                        'notes': anniversary.get('notes', '')
                    })
                except KeyError as e:
                    print(f"Warning: Missing required field {e} in anniversary config")

        except FileNotFoundError:
            print(f"Warning: Config file {config_file} not found")
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")

    def generate_anniversary_events(self) -> List[Tuple[str, ics.Event]]:
        """Generate events for all configured death anniversaries."""
        events = []

        for anniversary in self.anniversaries:
            date = self._lunar_to_solar(anniversary['lunar_month'], anniversary['lunar_day'])

            name = anniversary['name']
            if anniversary['chinese_name']:
                name = f"{name} ({anniversary['chinese_name']})"

            description = (
                f"{name}\n"
                f"Lunar Date: {anniversary['lunar_month']}月{anniversary['lunar_day']}日\n"
                f"\nNotes: {anniversary['notes'] if anniversary['notes'] else ''}\n"
            )

            # Create sanitized filename
            filename = f"anniversary_{anniversary['name']}.ics"
            filename = filename.lower().replace(' ', '_').replace('\'', '')
            events.append((filename, self._create_event(f"{name}", date, description)))

        return events

    def generate_calendars(self) -> List[str]:
        """Generate individual ICS files for all events."""
        generated_files = []

        # Generate and save all events
        for filename, event in (self.generate_solar_calendar_events() +
                                self.generate_lunar_calendar_events() +
                                self.generate_anniversary_events()):
            filepath = self._save_event_to_file(event, filename)
            generated_files.append(filepath)

        return generated_files


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate Chinese Memorial Dates Calendar')
    parser.add_argument('--year', type=int, default=datetime.now().year,
                        help='Year to generate calendar for (default: current year)')
    parser.add_argument('--output-dir', type=str, default='calendar_events',
                        help='Output directory for ICS files (default: calendar_events)')
    parser.add_argument('--config', type=str, default='anniversaries.yml',
                        help='YAML configuration file for death anniversaries (default: anniversaries.yml)')

    args = parser.parse_args()

    # Create calendar instance
    calendar_generator = ChineseMemorialCalendar(args.year, args.output_dir)

    # Load anniversaries from config
    calendar_generator.load_anniversaries_config(args.config)

    # Generate all calendar files
    generated_files = calendar_generator.generate_calendars()

    print(f"\nGenerated calendar files in {args.output_dir}:")
    for filepath in generated_files:
        print(f"- {os.path.basename(filepath)}")
    print("\nYou can import these files into Google Calendar or any other calendar application.")


if __name__ == "__main__":
    main()
