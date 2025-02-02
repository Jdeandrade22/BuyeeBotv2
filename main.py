from search_bot import SearchBot
from matrix_effect import MatrixEffect
from dataBase import create_database
create_database()
class MainWindow:
    def __init__(self):
        sg.theme_background_color("darkgray")
        self.layout = [
            [sg.Text("🔰 JDM Parts Search Bot", font=("Helvetica", 20, "bold"), text_color="red",
                     background_color="darkgray", justification="center")],
            [sg.Frame("Search Settings", [
                [sg.Text("Select Platform:", background_color="darkgray", font=("Helvetica", 12)),
                 sg.Combo(['Buyee', 'eBay'], default_value='Buyee', key="platform", size=(30, 1),
                          background_color="darkgray", text_color="white")],
                [sg.Text("Enter Keyword:", background_color="darkgray", font=("Helvetica", 12)),
                 sg.InputText(key="keyword", size=(30, 1), background_color="black", text_color="white")],
                [sg.Text("Matching Criteria (comma-separated):", background_color="darkgray", font=("Helvetica", 12)),
                 sg.InputText(key="criteria", size=(30, 1), background_color="black", text_color="white")],
                [sg.Text("Min Price:", background_color="darkgray", font=("Helvetica", 12)),
                 sg.InputText(key="min_price", size=(10, 1), background_color="black", text_color="white")],
                [sg.Text("Max Price:", background_color="darkgray", font=("Helvetica", 12)),
                 sg.InputText(key="max_price", size=(10, 1), background_color="black", text_color="white")]
            ], font=("Helvetica", 12), title_color="red", relief="ridge", background_color="darkgray")],
            [sg.Button("🔍 Search", font=("Helvetica", 12, "bold"), button_color=("red", "black"), size=(12, 1)),
             sg.Button("💾 Save Results", font=("Helvetica", 12, "bold"), button_color=("red", "black"), size=(12, 1))],
            [sg.Frame("Results", [
                [sg.Multiline(size=(80, 20), key="results", disabled=True, background_color="black", text_color="lightgreen")]
            ], font=("Helvetica", 12), title_color="red", relief="ridge", background_color="darkgray")]
        ]
        self.window = sg.Window("JDM Parts Search Bot", self.layout)
        self.rim_links = []
        self.search_completed = False
    def run(self):
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break
            if event == "🔍 Search":
                platform = values["platform"]
                keyword = values["keyword"]
                criteria = values["criteria"]
                price_min = values["min_price"] if values["min_price"].isdigit() else "0"
                price_max = values["max_price"] if values["max_price"].isdigit() else "10000"
                self.stop_event = threading.Event()
                matrix_thread = threading.Thread(target=MatrixEffect(self.window, self.stop_event).start)
                matrix_thread.start()
                search_bot = SearchBot(platform, keyword, criteria, price_min, price_max)
                def perform_search_thread():
                    self.rim_links = search_bot.perform_search()
                    self.search_completed = True
                    self.stop_event.set()
                threading.Thread(target=perform_search_thread, daemon=True).start()
            if self.search_completed:
                self.search_completed = False
                matrix_thread.join()
                if self.rim_links:
                    self.window["results"].update("\n".join(self.rim_links))
                    sg.popup("Search Complete", f"Found {len(self.rim_links)} matching listings.")
                else:
                    self.window["results"].update("No matching links found.")
                    sg.popup("Search Complete", "No matching links found.")
            if event == "💾 Save Results":
                if self.rim_links:
                    with open("rim_links.txt", "w") as file:
                        for link in self.rim_links:
                            file.write(link + "\n")
                    sg.popup("Save Successful", "Results saved to rim_links.txt")
                else:
                    sg.popup("Save Failed", "No results to save.")
        self.window.close()
if __name__ == "__main__":
    app = MainWindow()
    app.run()