BuyeeBot

BuyeeBot is a web scraping tool built with Python, Selenium, and PySimpleGUI that allows users to search for specific items on Buyee. It filters listings based on given keywords and saves the links to matching items in a text file. The bot includes a simple GUI to enter search terms, initiate a search, and view the number of matching listings.

Table of Contents

Features Setup Usage Troubleshooting Acknowledgments Features

Automated Search: Searches Buyee for specified terms and keywords. Filtered Results: Matches listings based on user-provided keywords. File Output: Saves the URLs of matched listings to matches.txt. Simple GUI: Provides a user-friendly interface to start a search and view results. Setup

Prerequisites Python: Ensure you have Python 3.7 or higher installed. Chrome: Install Google Chrome. ChromeDriver: Download and place the correct version of ChromeDriver in your system PATH or project folder. Installation Clone this repository to your local machine: bash Copy code git clone https://github.com/jdeandrade22/BuyeeBot1.git cd BuyeeBot Install the required Python packages: bash Copy code pip install -r requirements.txt Update the main.py file with the path to your ChromeDriver if it isn’t in your system PATH. Usage

Run the Bot: Launch the main script to open the GUI: bash Copy code python main.py Enter Search Criteria: Enter the search term in the input field (e.g., "work xt7") and click Search. Results Display: Once the search completes, the bot will display the number of matching listings in the results box. The links to matched listings will be saved to matches.txt. Troubleshooting

Timeout Errors: If the bot encounters a TimeoutException, make sure the ChromeDriver matches your Chrome version. Tcl RuntimeError: PySimpleGUI and Tkinter require single-threaded GUI updates. The bot uses a queue system to handle threading, but if errors persist, restart the bot and ensure Python is using the main thread for GUI updates. Empty Results: If no links are saved, verify the keywords used are appropriate for the desired listings on Buyee. Acknowledgments

BuyeeBot uses:

Selenium for web automation PySimpleGUI for the graphical interface