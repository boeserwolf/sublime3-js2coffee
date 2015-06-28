import sublime, sublime_plugin
import subprocess

class JsToCoffeescriptCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        # get non-empty selections
        regions = [s for s in view.sel() if not s.empty()]
        # if there's no non-empty selection, filter the whole document
        if len(regions) == 0:
            regions = [ sublime.Region(0, view.size()) ]
        for region in reversed(regions):
            content = view.substr(region)
            new_content = self.js2coffee(content)
            view.replace(edit, region, new_content)

    def js2coffee(self, contents):
            indentation = 4
            command = "js2coffee -i%d" % (indentation)
            js2coffee = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            output, error = js2coffee.communicate(bytearray(contents, "utf-8"));

            if error:
                # self.write_to_console(error)
                # self.window.run_command("show_panel", {"panel": "output.exec"})
                print("JsToCoffeescript: ERROR!")
                print("Result: %s" % error)
                return None
            return output.decode("utf-8")