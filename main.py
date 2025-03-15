import PySimpleGUI as sg
import threading
from search_bot import SearchBot
from matrix_effect import MatrixEffect
from dataBase import create_database
import traceback

def main():
    try:
        create_database()
        
        class MainWindow:
            def __init__(self):
                sg.set_options(font=("Helvetica", 12))
                sg.change_look_and_feel('DarkGrey13')
                
                self.layout = [
                    [sg.Text("🔰 JDM Parts Search Bot", font=("Helvetica", 20, "bold"), text_color="red",
                             justification="center", pad=((0, 0), (10, 20)))],
                    [sg.Frame("Search Settings", [
                        [sg.Text("Enter Keyword:"),
                         sg.InputText(key="keyword", size=(30, 1))],
                        [sg.Text("Matching Criteria (comma-separated):"),
                         sg.InputText(key="criteria", size=(30, 1))],
                        [sg.Text("Min Price:"),
                         sg.InputText(key="min_price", size=(10, 1))],
                        [sg.Text("Max Price:"),
                         sg.InputText(key="max_price", size=(10, 1))]
                    ], relief=sg.RELIEF_SOLID, pad=((10,10), (10,10)))],
                    [sg.Button("🔍 Search", size=(12, 1), font=("Helvetica", 12, "bold")),
                     sg.Button("💾 Save Results", size=(12, 1), font=("Helvetica", 12, "bold"))],
                    [sg.Frame("Results", [
                        [sg.Multiline(size=(80, 20), key="results", disabled=True, background_color='black', text_color='green')]
                    ], relief=sg.RELIEF_SOLID, pad=((10,10), (10,10)))]
                ]
                
                self.window = sg.Window("JDM Parts Search Bot", 
                                      self.layout, 
                                      finalize=True,
                                      resizable=True,
                                      element_justification='center')
                
                self.rim_links = []
                self.search_completed = False
                self.matrix_thread = None
                self.search_thread = None
                self.stop_event = None

            def run(self):
                while True:
                    try:
                        event, values = self.window.read(timeout=100)
                        if event == sg.WIN_CLOSED:
                            break
                        
                        if event == "🔍 Search":
                            # Clear previous results
                            self.window["results"].update("")
                            
                            keyword = values["keyword"]
                            criteria = values["criteria"]
                            price_min = values["min_price"] if values["min_price"].isdigit() else "0"
                            price_max = values["max_price"] if values["max_price"].isdigit() else "10000"
                            
                            # Stop previous threads if they exist
                            if self.stop_event:
                                self.stop_event.set()
                            if self.matrix_thread and self.matrix_thread.is_alive():
                                self.matrix_thread.join()
                            if self.search_thread and self.search_thread.is_alive():
                                self.search_thread.join()
                            
                            self.stop_event = threading.Event()
                            matrix_effect = MatrixEffect(self.window, self.stop_event)
                            self.matrix_thread = threading.Thread(target=matrix_effect.start)
                            self.matrix_thread.daemon = True
                            self.matrix_thread.start()
                            
                            search_bot = SearchBot("Buyee", keyword, criteria, price_min, price_max)
                            
                            def perform_search_thread():
                                try:
                                    self.rim_links = search_bot.perform_search()
                                    self.search_completed = True
                                    self.stop_event.set()
                                except Exception as e:
                                    print(f"Search error: {e}")
                                    self.window["results"].update(f"Error during search: {str(e)}")
                                    self.stop_event.set()
                            
                            self.search_thread = threading.Thread(target=perform_search_thread)
                            self.search_thread.daemon = True
                            self.search_thread.start()
                        
                        if self.search_completed:
                            self.search_completed = False
                            if self.matrix_thread:
                                self.matrix_thread.join()
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
                    
                    except Exception as e:
                        print(f"Error in main loop: {e}")
                        traceback.print_exc()
                
                self.window.close()

        app = MainWindow()
        app.run()

    except Exception as e:
        print(f"Application error: {e}")
        traceback.print_exc()
        sg.popup_error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()