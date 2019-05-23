# InsertAnyDate

Easily insert custom-formatted dates in your files.

## Usage

All date format specifications follow the [Python strftime syntax](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior).

The following commands are provided in the command palette

- `InsertAnyDate: Today` which inserts the current date in the current file,
  formatted according to the `format_out` setting
- `InsertAnyDate: Custom Date` which requests the user an input date (
  formatted according to `format_in` setting) and inserts the it in the current
  file, formatted according to the `format_out` setting

Alternatively, hotkeys could be created:

```json
// Insert always the date 2000-01-01
{
  "keys": ["ctrl+alt+d"],
  "command": "insert_any_date",
  "args": {"date": "2000-01-01"}
},
// Insert the current date
{ "keys": ["ctrl+alt+t"], "command": "insert_any_date" },
// Prompt the user for a date to insert
{ "keys": ["ctrl+alt+y"], "command": "insert_any_date_prompt" }
```
