import sublime
import sublime_plugin
import datetime

def status(msg):
    msg = "[InsertAnyDate] " + msg
    sublime.status_message(msg)
    print(msg)

class InsertAnyDateCommand(sublime_plugin.TextCommand):
    def run(self, edit, date=None):
        settings = sublime.load_settings("insert_date.sublime-settings")
        format_out = settings.get("format_out", "%a %B %d %Y")

        if format_out is not None:
            if format_out == '' or not isinstance(format_out, str) or format_out.isspace():
                # Not a string, empty or only whitespaces
                return

        if date is None:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime.strptime(date, "%Y-%m-%d")

        # Do the actual parse action
        try:
            text = date.strftime(format_out)
        except Exception as e:
            status("Error parsing format_out string `%s`" % format_out, e)
            return

        # Don't bother replacing selections with actually nothing
        if not text or text.isspace():
            return

        # Do replacements
        for r in self.view.sel():
            # Insert when sel is empty to not select the contents
            if r.empty():
                self.view.insert(edit, r.a, text)
            else:
                self.view.replace(edit, r, text)


class InsertAnyDatePromptCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings("insert_date.sublime-settings")
        format_in = settings.get("format_in", "%Y-%m-%d")
        date = datetime.datetime.now()
        default_date = date.strftime(format_in)

        # Unset save_on_focus_lost so that ST doesn't save and remove trailing
        # whitespace when the input/quick panel is opened, if that option is
        # also enabled. (#26)
        self.view.settings().set('save_on_focus_lost', False)

        # Ask for the format string
        i_panel = self.view.window().show_input_panel(
            # caption
            "Date (`%s`):" % format_in,
            # initial_text
            default_date,
            # on_done
            self.on_date_written,
            # on_change (unused)
            None,
            # on_cancel
            lambda: self.view.settings().erase('save_on_focus_lost')
        )

        # Select the default text
        i_panel.sel().clear()
        i_panel.sel().add(sublime.Region(0, i_panel.size()))

    def on_date_written(self, date_text):
        settings = sublime.load_settings("insert_date.sublime-settings")
        format_out = settings.get("format_out", "%a %B %d %Y")
        format_in = settings.get("format_in", "%Y-%m-%d")

        # Do the actual parse action
        try:
            date = datetime.datetime.strptime(date_text, format_in)
        except Exception as e:
            status("Error parsing format_in string `%s`" % format_in, e)
            return
        try:
            text = date.strftime(format_out)
        except Exception as e:
            status("Error parsing format_out string `%s`" % format_out, e)
            return

        self.view.run_command(
            'insert_any_date',
            {'date': date.strftime("%Y-%m-%d")}
        )
