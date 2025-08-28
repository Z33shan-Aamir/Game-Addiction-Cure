from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer, Static, Button,Markdown, Input
from textual.containers import Vertical, Horizontal, Center, Container
from rich.text import Text
# loacl imports
from tracker.load_config import ALL_APPS, PRODUCTIVE_APPS, UNPRODUCTIVE_APPS


apps_list = []
def app_list_for_table() -> None:
    for index, app in enumerate(ALL_APPS,1):
        app : str= app.title() # convert app name to title case
        if app.lower() in PRODUCTIVE_APPS:
            data = (str(index), app, "Productive")
            apps_list.append(data)
        elif app.lower() in UNPRODUCTIVE_APPS:
            data = (str(index), app, "Unproductive")
            apps_list.append(data)
        else:
            data = (str(index), app, "Neutral")
            apps_list.append(data)
            
            
class DisplayTableOfApp(Static):
    """Simple app showing a table from a list"""
    def compose(self) -> ComposeResult:
        with Container(classes="data-table"):
            yield DataTable( )  # Create the table widget
        with Container(classes="button-container"):
            with Vertical():
                yield Input(placeholder="Enter App Name", classes="app-name-input")
            with Horizontal():
                    yield Button(
                        "Add App",
                        variant="primary",
                        tooltip="Press to add new apps in the app.",
                        action="notify('App was added')"
                    )
                    yield Button(
                        "Remove App",
                        variant="warning",
                        tooltip="Press to Remove apps in the input box.",
                        action="notify('App was removed')"
                        )
               
    
    def on_mount(self) -> None:
        
        # Get the table widget
        table = self.query_one(DataTable)
        
        # Add columns
        table.add_columns("ID", "App Name", "Category")
        # initialize the list that contains all the app name and related data 
        app_list_for_table()
        # Add rows from the list
        for row in apps_list:
            row_style = "italic #03AC13" if row[1].lower() in PRODUCTIVE_APPS else "italic bold #FF0000" if row[1].lower() in UNPRODUCTIVE_APPS else ""
            styled_row = [
                Text(str(cell), style=row_style) for cell in row
            ]
            table.add_row(*styled_row)
            
class AppUsage(Static):

    def compose(self):
        yield Static("Hellpo")

class TrackerTUI(App):
    CSS_PATH = "styles/styles.tcss"
    BINDINGS = [
        ("d", "toggle_dark","Toggle Dark/Light mode")
    ]
    def compose(self):
        yield Header()
        with Horizontal():
            with Container(classes="container table-of-app-container") as panel:
                yield Markdown("# Your Apps Live Here")
                panel.border_title = "App List"
                with Vertical():
                    yield DisplayTableOfApp()
                    
            with Container(classes="container graph-container") as panel:
                panel.border_title = "App Usage Graph"
                with Vertical():           
                    yield AppUsage()
        yield Footer()
    def action_toggle_dark(self):
        self.theme = "tokyo-night" if self.theme=="textual-light" else "textual-light"
    def on_mount(self):
        self.theme = "tokyo-night"
        self.title = "My tui app"
        self.sub_title = "View you app usage"

def main():
    TrackerTUI().run()