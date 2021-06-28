# ---------------------------------------------------------------------------- #
#                                PROGRAM HEADER                                #
# ---------------------------------------------------------------------------- #

# Name          : ChapterCheck.py
# Programmer    : Sanchaai Mathi
# Date          : 06/06/21
# Description   : Chapter Check provides users with a way to stay up to date on
#                 the newest releases of their favourite mangas! Aside from the
#                 primary function of searching for new chapter releases, the
#                 program also boasts various supplementary features, such as
#                 supporting multiple users and allowing one to view and manage
#                 a personal (and easily updatable) manga list.


# ---------------------------------------------------------------------------- #
#                               IMPORT STATEMENTS                              #
# ---------------------------------------------------------------------------- #

import random # Allows for the selection of a randomized home screen version
import requests # Enables the program to scrape the internet for manga data
import tkinter # Used to provide the user with a GUI to interact with


# ---------------------------------------------------------------------------- #
#                           LOGICAL/BACKEND FUNCTIONS                          #
# ---------------------------------------------------------------------------- #

# ------------------------------ LOGIN FUNCTIONS ----------------------------- #

# Note: Some functions have "event=None" as a parameter. This is because when
# these functions are called by a button click, information about the button
# click event is also passed to the function (even if it won't be used). Hence,
# "event=None" allows the function to ignore this superfluous argument.

# Function to validate the username and password entered by the user, and to log
# them in (or display appropriate error messages, depending on the input)
def validate_login(event=None):

    # Globalize username and password, since they are only being read; also, the
    # username must be globalized in order to be displayed on the home screen
    global username
    global password

    # Obtain the entered username and password from the entry boxes on the login
    # screen
    username = user_entry.get()
    password = pass_entry.get()
    
    # Only proceed with the rest of the checks if the user's input is
    # alphanumeric (this is validated using the "user_pass_alnum" function)
    if user_pass_alnum() == True:

        # The login credentials are checked using the "credentials_check"
        # function, and the returned result is stored in login_status
        login_status = credentials_check()

        # If the user does not already exist, create the new user using the
        # "create_user" function, and then proceed to the home screen
        if login_status == "New User":
            create_user()
            home_screen()

        # If the user exists and the password is correct, proceed to the home
        # screen
        elif login_status == "Correct Password":
            home_screen()

        # Otherwise (if the user exists but the password is incorrect), display
        # an appropriate error message after deleting any pre-existing error
        # messages
        else:
            canvas.delete("error")
            canvas.create_text(665, 479, font=("Century Gothic", 9), fill="red",
                               text = "ERROR: INCORRECT PASS", tags="error")

    # If the user input is not alphanumeric, display an appropriate error
    # message after deleting any pre-existing error messages
    else:
        canvas.delete("error")
        canvas.create_text(665, 479, font=("Century Gothic", 9), fill="red",
                           text = "ERROR: USER AND PASS MUST BE ALPHANUMERIC",
                           tags="error")


# Function that returns whether both the entered username and password are
# alphanumeric (consisting of only letters and numbers)
def user_pass_alnum():

    if (username.isalnum() == True) and (password.isalnum() == True):
        return True
    else:
        return False


# Function used to check if the entered login credentials are correct (or
# returns an appropriate message if a new user must be created)
def credentials_check():

    # Opens credentials file and reads a line from said file
    credentials_file = open("database/credentials_list.txt", "r")
    credentials_read = credentials_file.readline()

    # Continues to loop until an empty line is found (which denotes that the end
    # of the file has been reached)
    while credentials_read != "":

        # Strips the newline character from the line that has been read, and
        # splits it (by the "|" character) into a list
        credentials_read = credentials_read.strip()
        credentials_read = credentials_read.split("|")

        # If the first element in the list (representing the username) matches
        # the entered username:
        if credentials_read[0] == username:

            # Close the file, since it will not be needed for the rest of the
            # function (the user in question has already been located, and their
            # data is stored in "credentials_read")
            credentials_file.close()

            # Check if the second element in the list (representing the
            # password) maches the entered password, and return the
            # corresponding message
            if credentials_read[1] == password:
                return "Correct Password"
            else:
                return "Incorrect Password"
            
        # Read a new line from the credentials file
        credentials_read = credentials_file.readline()

    # If the function reaches this portion, it means that the entire credentials
    # file has been scanned, yet the entered username was not found, meaning a
    # new user should be made; Hence, close the file and return "New User"
    credentials_file.close()
    return "New User"


# Function used to create a new user
def create_user():

    # The credentials file is opened, the new user's username and password
    # (separated by the "|" character) are appended to the file (along with a
    # newline character), and the file is closed
    credentials_file = open("database/credentials_list.txt", "a")
    credentials_file.write(username + "|" + password)
    credentials_file.write("\n")
    credentials_file.close()

    # A new file is also created in the user's name (by opening the desired
    # filename in write mode), in order to store their personal manga list; Once
    # the file is created, it is promptly closed
    user_filename = "database/" + username + ".txt"
    user_file = open(user_filename, "w")
    user_file.close()


# -------------------------- NEW RELEASES FUNCTIONS -------------------------- #

# Function that handles searching for new manga chapter releases
def search_releases(event=None):

    # Displays the loading screen, since this process could potentially be time
    # consuming (due to the usage of the "requests" library)
    loading_screen()

    # Obtains the user's manga list and stores it in user_list
    user_list = get_user_list()

    # Only perform the following actions if the user's manga list is not empty
    if user_list != []:

        # Variable to store the updated manga list (with the latest chapters)
        updated_list = []

        # Variable to store only the newly released manga names and chapters,
        # which will be displayed to the user
        new_manga_chapters = []
        
        # Iterates through each item in the user's manga list
        for i in user_list:
            
            # The first element of the item holds the manga ID, a unique
            # identifying number specific to each manga, used by the
            # "releases_query" function when searching for new chapters
            manga_id = i[0]

            # The second element holds the manga name
            manga_name = i[1]

            # The final element holds the chapter last read by the user
            last_read_chapter = i[-1]
            
            # Uses the "releases_query" function to obtain the latest chapter,
            # and stores the result in the latest_chapter variable
            latest_chapter = releases_query(manga_id)
            
            # Appends the up-to-date manga information to updated_list
            updated_list.append([manga_id, manga_name, latest_chapter])
            
            # If the latest chapter is not the same as the last read chapter,
            # a new chapter must be out, and hence the manga name and latest
            # chapter must be appended to the new_manga_chapters variable
            if latest_chapter != last_read_chapter:
                new_manga_chapters.append([manga_name, latest_chapter])
        
        # If the new_manga_chapters variable is not empty (meaning that there
        # are new releases), then update the manga list and display the releases
        # screen (also, pass the new_manga_chapters variable as an argument)
        if new_manga_chapters != []:
            update_list(updated_list)
            releases_screen(new_manga_chapters)

        # Otherwise (if there are no new releases), display the screen that
        # reflects this
        else:
            releases_no_new_screen()

    # If the manga list is empty, display the screen that reflects this
    else:
        releases_empty_screen()


# Function used to request the latest chapter of a manga
def releases_query(id_num):
    
    # URL for the page that gives the information on a manga, using its unique
    # ID number
    manga_site_url = f"https://www.mangaupdates.com/series.html?id=" + id_num

    # Obtains all of the text from the above page
    manga_site_data = requests.get(manga_site_url).text

    # Search for the index of the "Latest Release" substring, in order to
    # provide a starting point for searching for the latest chapter
    latest_index = manga_site_data.find('Latest Release')

    # Starting from latest_index, search for the first instance of the substring
    # "c.<i>", which is the HTML formatting that precedes a chapter (in order to
    # make the chapter number appear in italics on the site)
    italics_start = manga_site_data.find('c.<i>', latest_index)

    # If the above substring ("c.<i>") could not be found, then return "N/A" as
    # the latest chapter
    if italics_start == -1:
        return "N/A"

    # Otherwise (if there is a latest chapter available), do the following
    else:

        # Add 5 (length of "c.<i>") to the italics_start index, in order to set
        # the index stored in the variable to be equivalent to the END of the
        # substring, so that it truly represents the beginning of the TEXT that
        # has been italicized (the chapter number), rather than the beginning of
        # the HTML formatting
        italics_start += 5

        # Starting from italics_start, search for the first instance of the
        # substring "</i>", which is the HTML formatting that comes after the
        # chapter ("</i>" signals the end of the italic text)
        italics_end = manga_site_data.find('</i>', italics_start)

        # Finally, we return the latest chapter, which can be found between the
        # end of the "c.<i>" substring and the beginning of the "</i>" substring
        latest_ch = manga_site_data[italics_start:italics_end]
        return latest_ch


# ------------------------- VIEW MANGA LIST FUNCTION ------------------------- #

# Function for determining which manga list screen to show
def manga_list_type(event=None):

    # Obtains the user's manga list and stores it in user_list
    user_list = get_user_list()

    # If the user's list is not empty, then display the manga list screen (also,
    # pass the user_list variable as an argument)
    if user_list != []:
        list_manga_screen(user_list)

    # Otherwise (if the list is empty), display the screen that reflects this
    else:
        list_empty_screen()


# ---------------------------- ADD MANGA FUNCTIONS --------------------------- #

# Function that handles finding the manga to be added to the user's manga list
def search_add_manga(event=None):

    # Globalization (to allow the data to be appended to the manga list)
    global add_manga_data

    # Displays the loading screen, since this process could potentially be time
    # consuming (due to the usage of the "requests" library)
    loading_screen()

    # Obtains the name of the requested manga from the entry box on the
    # add_manga screen
    requested_manga =  manga_name_entry.get()

    # Uses the "add_manga_query" function to obtain the official title, ID
    # number, and latest chapter for the requested manga, and stores it in the
    # add_manga_data variable
    add_manga_data = add_manga_query(requested_manga)

    # If the add_manga_data variable is not empty (meaning that information was
    # found for the requested manga), then display the confirmation screen for
    # adding the manga to the user's list (also, pass the manga_name variable,
    # which is the second element in add_manga_data, as an argument)
    if add_manga_data != []:
        manga_name = add_manga_data[1]
        add_confirm_screen(manga_name)

    # Otherwise (if the add_manga_data variable is empty), then display the
    # screen that reflects this
    else:
        add_invalid_screen()


# Function used to request information about the queried manga, such as the
# official title, manga ID number, and the current/latest chapter
def add_manga_query(query):

    # Stores the data obtained about the requested manga
    manga_data = []
    
    # ID number for a custom search engine (which only searches from the manga
    # website) Can be manually tested at the link below:
    # "https://cse.google.com/cse?cx=8502f8beb3e362fb6"
    SEARCH_ENGINE_ID = "8502f8beb3e362fb6"

    # Key number required to use the aforementioned custom search engine;
    # Specifically, this allows Google to identify the client making the search
    KEY = "AIzaSyCmM2qJwrKvZ_gN45WBbMLZYj3WTA3ZXXQ" 


    # Base URL for making Google searches with a custom search engine
    search_url = "https://www.googleapis.com/customsearch/v1/siterestrict"

    # Adds the key and search engine ID to the URL
    search_url += "?key=" + KEY + "&cx=" + SEARCH_ENGINE_ID

    # Adds extra parameters to the URL (for restricting the response to only
    # include one result, which will consist of the result's title and link)
    search_url += "&num=1&fields=items(title, link)"

    # Finally, adds the search query to the URL
    search_url += "&q=" + query


    # Actually performs the search using the URL created above, and stores the
    # newly obtained search result text in the variable "search_result"
    search_result = requests.get(search_url).text

    # Since we want the ID number from the URL, we first find the index of the
    # URL portion (which begins with '"link:"') within the search result text
    link_index = search_result.find('"link":')

    # Searches for the presence of the substrings "series" and "id=" within the
    # search result text
    series_exists = "series" in search_result[link_index:]
    id_exists = "id=" in search_result[link_index:]

    # Checks various things: If the link exists, if the link is for a series,
    # and if the series has an ID number; If all of these are true, then the ID
    # number can be located
    if (link_index != -1) and (series_exists == True) and (id_exists == True):

        # Finds the beginning of the ID number by using the ".find()" method to
        # locate the beginning of the "id=" substring, and adding 3 in order to
        # get the starting index of the actual number
        id_index = search_result.find("id=") + 3
        
        id_num = "" # Variable that will hold the manga's ID number
        id_finished = False # Used to end the loop when the ID number is found

        # Keeps scanning for digits of the ID number until a non-numeric
        # character is found (meaning that the end of the ID number has been
        # reached), after which the loop is ended
        while id_finished != True:

            # Determines if the character in question is a digit
            if search_result[id_index].isdigit() == True:

                # Adds the aforementioned digit to the ID number
                id_num += search_result[id_index]

                # Increases the index of the scanned character each iteration
                id_index += 1

            # Ends the loop when a non-numeric character is encountered
            else:
                id_finished = True

        # Appends the ID number to the manga_data variable
        manga_data.append(id_num)

        # Finds the beginning of the title by locating the index of the
        # '"title": "' substring, and adding 10 (the length of the substring) in
        # order to get the starting index of the actual title
        title_start_index = search_result.find('"title": "') + 10

        # Finds the end of the title by locating the index of the '",' substring
        title_end_index = search_result.find('",')

        # Stores the title(which can be found between the indexes stored in the
        # title_start_index and title_end_index variables) in the manga_title
        # variable
        manga_title = search_result[title_start_index:title_end_index]

        
        # Sometimes the search result may prepend/append the name of the manga
        # site to the title of the manga, in which case it must be removed; Two
        # if statments are used in the event that the title is both prepended
        # and appended by the site name

        if manga_title.endswith(" - Baka-Updates Manga"):

            # Takes all the characters up to the index of -21 (the length of the
            # substring containing the site name is 21 characters) from the
            # manga_title variable, and assigns these characters to the same
            # variable (effectively "removing" the last 21 characters)
            manga_title = manga_title[:-21]

        if manga_title.startswith("Baka-Updates Manga - "):

            # Takes all the characters from the index of 21 onwards (the length
            # of the substring containing the site name is 21 characters) from
            # the manga_title variable, and assigns these characters to the same
            # variable (effectively "removing" the first 21 characters)
            manga_title = manga_title[21:]

        # Appends the manga's title to the manga_data variable
        manga_data.append(manga_title)
        
        
        # Makes use of the relases_query function to also obtain the latest (or
        # current) chapter associated with the newly obtained ID number
        current_chapter = releases_query(id_num)

        # Appends the current chapter to the manga_data variable
        manga_data.append(current_chapter)
    
    # Returns the manga_data variable (containing the ID number, official title,
    # and current chapter of the requested manga respectively)
    return manga_data


# Function used to append a new manga and its corresponding data to the user's
# manga list upon confirmation
def add_to_list(event=None):

    # Opens the user's manga list file in append mode
    user_filename = "database/" + username + ".txt"
    user_file = open(user_filename, "a")

    # Joins the manga's data with the "|" character, and writes this string to
    # the file (along with a newline character)
    user_file.write("|".join(add_manga_data))
    user_file.write("\n")
    
    # Closes the file when finished
    user_file.close()
    
    # Displays the success screen after successfully writing to the file
    success_screen()


# -------------------------- REMOVE MANGA FUNCTIONS -------------------------- #

# Function for determining which remove manga screen to show
def remove_manga_type(event=None):

    # Obtains the user's manga list and stores it in user_list
    user_list = get_user_list()

    # If the user's list is not empty, then display the remove manga screen
    # (also, pass the user_list variable as an argument)
    if user_list != []:
        remove_manga_screen(user_list)

    # Otherwise (if the list is empty), display the screen that reflects this
    else:
        remove_empty_screen()


# Function that handles the removal of a manga from the user's manga list
def remove_from_list(event=None):

    # Destroys the frame (on the remove_manga_screen)
    frame.destroy()
    
    # Obtains the user's manga list and stores it in user_list
    user_list = get_user_list()

    # Variable to store the new manga list (after deletions)
    new_list = []

    # Loops from 0 up to the number of elements in the intvars_list variable
    for i in range (len(intvars_list)):

        # If the IntVar at the index of i is equal to 0 (meaning the
        # corresponding checkbutton has not been selected), add it to the
        # new_list variable (thus, mangas that have been selected will not be
        # added to the new manga list)
        if intvars_list[i].get() == 0:
            new_list.append(user_list[i])

    # If there are no changes between the user's manga list and the new manga
    # list (meaning that nothing was deleted), then display a screen that
    # reflects the fact that the user's selection was invalid
    if user_list == new_list:
        remove_invalid_screen()

    # Otherwise (if deletions were indeed made), update the manga list using the
    # "update_list" function (also, pass the new_list variable as an argument)
    # and display the success screen
    else:
        update_list(new_list)    
        success_screen()


# Function to delete the pre-existing frame and proceed to the cancelled screen
def del_frame_cancelled(event=None):
    
    frame.destroy()
    cancelled_screen()


# -------------------------- MISCELLANEOUS FUNCTIONS ------------------------- #

# Function to obtain a record of the user's manga list
def get_user_list():

    # Variable to hold the record of the user's manga list
    user_records = []

    # Opens the user's manga list file in read mode and reads a line from the
    # aforementioned file
    user_filename = "database/" + username + ".txt"
    user_file = open(user_filename, "r")
    user_data_read = user_file.readline()
    
    # Continues to loop until an empty line is found (which denotes that the end
    # of the file has been reached)
    while user_data_read != "":

        # Strips the newline character from the line that has been read, and
        # splits it (by the "|" character) into a list
        user_data_read = user_data_read.strip()
        user_data_read = user_data_read.split("|")

        # Appends the list to record stores in the user_records variable
        user_records.append(user_data_read)

        # Read a new line from the user's manga list file
        user_data_read = user_file.readline()
    
    # Closes the file when finished, and returns the user_records variable
    user_file.close()
    return user_records


# Function to update an existing manga list with a new list
def update_list(new_list):

    # Opens the user's manga list file in write mode
    user_filename = "database/" + username + ".txt"
    user_file = open(user_filename, "w")

    # Iterates through the items in the new list, joins each one with the "|"
    # character, and writes this string to the file (along with a newline
    # character) 
    for i in new_list:
        user_file.write("|".join(i))
        user_file.write("\n")
    
    # Closes the file when finished
    user_file.close()


# Function to delete the pre-existing frame and proceed to the home screen
def del_frame_home(event=None):
    
    frame.destroy()
    home_screen()


# ---------------------------------------------------------------------------- #
#                           VISUAL/FRONTEND FUNCTIONS                          #
# ---------------------------------------------------------------------------- #

def login_screen(event=None):
    
    # Globalizations (so that the credentials can be validated)
    global user_entry
    global pass_entry

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the login screen backdrop
    canvas.create_image(0, 0, image=BG_LOGIN, anchor="nw")

    # ------------------------ USER/PASS ENTRY FIELDS ------------------------ #

    # Username entry box created as a standard Tkinter widget
    user_entry = tkinter.Entry(width=23,relief="flat", bd=0,
                               font=("Century Gothic", 11))

    # Username entry widget is placed using a canvas window object
    canvas.create_window(692, 411, window=user_entry)


    # Password entry box created as a standard Tkinter widget; Text is
    # obfuscated using the bullet-point symbol
    pass_entry = tkinter.Entry(width=23, relief="flat", show="•",
                               bd=0, font=("Century Gothic", 11))

    # Password entry widget is placed using a canvas window object
    canvas.create_window(692, 449, window=pass_entry)

    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent login button over the area of the backdrop in which
    # the visual button is present
    canvas.create_image(665, 525, image=BTN_LOGIN, tags="login")
    
    # Binds the image to a command, so that the aforementioned command is
    # executed when clicked on (similar to an actual button widget); In this
    # case, the image is being bound to the "validate_credentials" function
    canvas.tag_bind("login", "<ButtonPress-1>", validate_login)
    

    # Creates transparent quit button
    canvas.create_image(942, 634, image=BTN_QUIT, tags="quit")
    
    # Binds quit button to the "thanks_screen" function
    canvas.tag_bind("quit", "<ButtonPress-1>", thanks_screen)


def home_screen(event=None):

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Generates random number (from 0 to 9) to determine which version of the
    # home screen will be displayed to the user
    home_version = random.randrange(10)

    # Displays the home scren backdrop (displays the version specified by the
    # index number stored in variable "home_version" above)
    canvas.create_image(0, 0, image=HOME_BACKDROPS[home_version],anchor="nw")

    # --------------------------- LOGGED IN MESSAGE -------------------------- #

    # Displays the username in an appropriate "Logged in as" message in the
    # bottom left area of the screen
    canvas.create_text(882, 633.5, font=("Century Gothic", 10),
                       text=("Logged in as " + username), anchor="e")
    
    # -------------------------- LOGOUT/INFO BUTTONS ------------------------- #

    # Creates transparent logout button
    canvas.create_image(917, 634, image=BTN_LOGOUT_INFO, tags="logout")

    # Binds logout button to the "login_screen" function
    canvas.tag_bind("logout", "<ButtonPress-1>", login_screen)


    # Creates transparent info button
    canvas.create_image(964, 634, image=BTN_LOGOUT_INFO, tags="info")

    # Binds info button to the "info_screen" function
    canvas.tag_bind("info", "<ButtonPress-1>", info_screen)

    # ---------------------------- SIDEBAR BUTTONS --------------------------- #

    # Creates transparent button to search for new manga releases
    canvas.create_image(162, 256, image=BTN_SIDEBAR, tags="side_releases")
    
    # Binds side_releases button to the "search_releases" function
    canvas.tag_bind("side_releases", "<ButtonPress-1>", search_releases)


    # Creates transparent button to view manga list
    canvas.create_image(162, 360, image=BTN_SIDEBAR, tags="side_view_list")
    
    # Binds side_view_list button to the "manga_list_type" function
    canvas.tag_bind("side_view_list", "<ButtonPress-1>", manga_list_type)


    # Creates transparent button to add new manga to manga list
    canvas.create_image(162, 463, image=BTN_SIDEBAR, tags="side_add_manga")
    
    # Binds side_add_manga button to the "add_manga_screen" function
    canvas.tag_bind("side_add_manga", "<ButtonPress-1>", add_manga_screen)


    # Creates transparent button to remove manga from manga list
    canvas.create_image(162, 566, image=BTN_SIDEBAR, tags="side_remove_manga")
    
    # Binds side_remove_manga button to the "remove_manga_type" function
    canvas.tag_bind("side_remove_manga", "<ButtonPress-1>", remove_manga_type)


def info_screen(event=None):
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the info screen backdrop
    canvas.create_image(0, 0, image=BG_INFO, anchor="nw")

    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to return to home screen
    canvas.create_image(589, 523, image=BTN_HOME, tags="info_home")
    
    # Binds info_home button to the "home_screen" function
    canvas.tag_bind("info_home", "<ButtonPress-1>", home_screen)


    # Creates transparent button to go to credit screen
    canvas.create_image(764, 523, image=BTN_CREDIT, tags="credit")
    
    # Binds credit button to the "credit_screen" function
    canvas.tag_bind("credit", "<ButtonPress-1>", credit_screen)


def credit_screen(event=None):

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the credit screen backdrop
    canvas.create_image(0, 0, image=BG_CREDIT, anchor="nw")

    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to return to home screen
    canvas.create_image(665, 539, image=BTN_HOME, tags="credit_home")

    # Binds credit_home button to the "home_screen" function
    canvas.tag_bind("credit_home", "<ButtonPress-1>", home_screen)


def releases_screen(new_releases):
    
    global frame # Globalization (to enable deletion from other functions)

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the releases screen backdrop
    canvas.create_image(0, 0, image=BG_RELEASES, anchor="nw")

    # ---------------------------- FRAME CREATION ---------------------------- #
    
    # Creates a frame in the window and places it at the appropriate coordinates
    frame = tkinter.Frame(window)
    frame.place(x=515, y=294)

    # Scrollable region height calculation (scales with the number of items that
    # need to be displayed)
    region_height = len(new_releases)*30 - 10

    # Creates a canvas within the frame, specifying both the visible dimensions
    # and the dimensions/coordinates of the scrollable region
    frame_canvas = tkinter.Canvas(frame,width=300, height=170, bg="white",
                             scrollregion=(0,0,300,region_height),
                             highlightthickness=0)

    # If there are more than 6 items to be displayed, configure a vertical
    # scrollbar on the frame that can be used to scroll the canvas within
    if len(new_releases) > 6:
        scrollable = tkinter.Scrollbar(frame, orient="vertical",
                                       command=frame_canvas.yview)
        scrollable.pack(side="right",fill="y")
        frame_canvas.configure(yscrollcommand=scrollable.set)

    # Packs the canvas to fill the space provided
    frame_canvas.pack(fill="both")

    # Initial y-position for the first displayed item
    y_position = 10

    # Iterates through each element in the new_releases list
    for i in new_releases:

        # The first item in each element (the manga name) is assigned to the
        # manga_name variable
        manga_name = i[0]

        # The last item in each element (the newest chapter) is assigned to the
        # new_chapter variable
        new_chapter = i[-1]

        # If the length of the manga's name is over 25 characters long, then
        # trim the name to only show to first 25 characters and append "..."
        if len(manga_name) > 25:
            manga_name = manga_name[:25] + "..."

        # If the length of the newest chapter is over 8 characters long, then
        # trim the chapter to only show to first 8 characters and append "..."
        if len(new_chapter) > 8:
            new_chapter = new_chapter[:8] + "..."
        
        # Displays the string stored in manga_text (consisting of the manga name
        # and newest chapter) on the canvas within the frame
        manga_text = manga_name + " (c. " + new_chapter + ")"
        frame_canvas.create_text(150, y_position, text=manga_text,
                                 font=("Century Gothic", 11))
        
        # Increases the y-position for displaying items each iteration
        y_position += 30
    
    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to delete the frame and return to home screen
    canvas.create_image(664, 512, image=BTN_HOME, tags="releases_home")

    # Binds releases_home button to the "del_frame_home" function
    canvas.tag_bind("releases_home", "<ButtonPress-1>", del_frame_home)


def releases_no_new_screen():

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the no new releases screen backdrop
    canvas.create_image(0, 0, image=BG_RELEASES_NO_NEW, anchor="nw")

    # After 5 seconds, returns to the home screen
    canvas.after(5000, home_screen)


def releases_empty_screen():

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the releases (empty list) screen backdrop
    canvas.create_image(0, 0, image=BG_RELEASES_EMPTY, anchor="nw")

    # After 5 seconds, returns to the home screen
    canvas.after(5000, home_screen)


def list_manga_screen(manga_list):
    
    global frame # Globalization (to enable deletion from other functions)

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the manga list screen backdrop
    canvas.create_image(0, 0, image=BG_LIST_MANGA, anchor="nw")

    # ---------------------------- FRAME CREATION ---------------------------- #

    # Creates a frame in the window and places it at the appropriate coordinates
    frame = tkinter.Frame(window)
    frame.place(x=515, y=285)

    # Scrollable region height calculation (scales with the number of items that
    # need to be displayed)
    region_height = len(manga_list)*30 - 10

    # Creates a canvas within the frame, specifying both the visible dimensions
    # and the dimensions/coordinates of the scrollable region
    frame_canvas = tkinter.Canvas(frame,width=300, height=170, bg="white",
                             scrollregion=(0,0,300,region_height),
                             highlightthickness=0)

    # If there are more than 6 items to be displayed, configure a vertical
    # scrollbar on the frame that can be used to scroll the canvas within
    if len(manga_list) > 6:
        scrollable = tkinter.Scrollbar(frame, orient="vertical",
                                       command=frame_canvas.yview)
        scrollable.pack(side="right",fill="y")
        frame_canvas.configure(yscrollcommand=scrollable.set)

    # Packs the canvas to fill the space provided
    frame_canvas.pack(fill="both")

    # Initial y-position for the first displayed item
    y_position = 10 # y-pos

    # Iterates through each element in the manga list
    for i in manga_list:

        # The second item in each element (the manga name) is assigned to the
        # manga_name variable
        manga_name = i[1]

        # The last item in each element (the last read chapter) is assigned to
        # the last_read variable
        last_chapter = i[-1]

        # If the length of the manga's name is over 25 characters long, then
        # trim the name to only show to first 25 characters and append "..."
        if len(manga_name) > 25:
            manga_name = manga_name[:25] + "..."

        # If the length of the newest chapter is over 8 characters long, then
        # trim the chapter to only show to first 8 characters and append "..."
        if len(last_chapter) > 8:
            last_chapter = last_chapter[:8] + "..."
        
        # Displays the string stored in manga_text (consisting of the manga name
        # and last read chapter) on the canvas within the frame
        manga_text = manga_name + " (c. " + last_chapter + ")"
        frame_canvas.create_text(150, y_position, text=manga_text, 
                            font=("Century Gothic", 11))

        # Increases the y-position for displaying items each iteration
        y_position += 30

    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to delete the frame and return to home screen
    canvas.create_image(665, 511, image=BTN_HOME, tags="releases_home")

    # Binds releases_home button to the "del_frame_home" function
    canvas.tag_bind("releases_home", "<ButtonPress-1>", del_frame_home)


def list_empty_screen():
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the empty manga list screen backdrop
    canvas.create_image(0, 0, image=BG_LIST_EMPTY, anchor="nw")

    # After 5 seconds, returns to the home screen
    canvas.after(5000, home_screen)


def add_manga_screen(event=None):

    # Globalization (Allows other functions to access the variable)
    global manga_name_entry
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the add manga screen backdrop
    canvas.create_image(0, 0, image=BG_ADD_MANGA, anchor="nw")

    # ------------------------ MANGA NAME ENTRY FIELD ------------------------ #

    # Manga name entry box created as a standard Tkinter widget
    manga_name_entry = tkinter.Entry(width=24,relief="flat", bd=0,
                               font=("Century Gothic", 11))

    # Manga name entry widget is placed using a canvas window object
    canvas.create_window(741, 378, window=manga_name_entry)

    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to proceed with adding manga
    canvas.create_image(583, 489, image=BTN_REMOVE_ADD, tags="add_manga")

    # Binds add_manga_home button to the "search_add_manga" function
    canvas.tag_bind("add_manga", "<ButtonPress-1>", search_add_manga)


    # Creates transparent button to cancel operation & return to the home screen
    canvas.create_image(754, 489, image=BTN_CANCEL, tags="add_manga_home")

    # Binds add_manga_home button to the "cancelled_screen" function
    canvas.tag_bind("add_manga_home", "<ButtonPress-1>", cancelled_screen)

    
def add_confirm_screen(manga_title):

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the add manga confirmation screen backdrop
    canvas.create_image(0, 0, image=BG_ADD_CONFIRM, anchor="nw")

    # ---------------------------- MANGA NAME TEXT --------------------------- #

    # Displays the name of the manga that is to be added to the manga list
    canvas.create_text(665, 328, text=manga_title, font=("Century Gothic", 14))

    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to confirm the addition of the above manga to
    # the user's manga list
    canvas.create_image(615, 514, image=BTN_CONFIRM, tags="add_confirm_yes")

    # Binds add_confirm_yes button to the "cancelled_screen" function
    canvas.tag_bind("add_confirm_yes", "<ButtonPress-1>", add_to_list)

    # Creates transparent button to cancel the operation and return to the add
    # manga screen
    canvas.create_image(716, 514, image=BTN_CONFIRM, tags="add_confirm_no")

    # Binds add_confirm_no button to the "add_cancelled_screen" function
    canvas.tag_bind("add_confirm_no", "<ButtonPress-1>", add_cancelled_screen)


def add_invalid_screen():

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the cancelled screen backdrop
    canvas.create_image(0, 0, image=BG_ADD_INVALID, anchor="nw")

    # After 5 seconds, returns to the add manga screen
    canvas.after(5000, add_manga_screen)


def add_cancelled_screen(event=None):
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the cancelled screen backdrop
    canvas.create_image(0, 0, image=BG_ADD_CANCELLED, anchor="nw")

    # After 5 seconds, returns to the add manga screen
    canvas.after(5000, add_manga_screen)


def remove_manga_screen(manga_list):

    # Globalized to enable deletion from other functions
    global frame

    # Globalized to allow other functions to see what manga were selected
    global intvars_list

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the remove manga screen backdrop
    canvas.create_image(0, 0, image=BG_REMOVE_MANGA, anchor="nw")

    # ---------------------------- FRAME CREATION ---------------------------- #

    # Creates a frame in the window and places it at the appropriate coordinates
    frame = tkinter.Frame(window)
    frame.place(x=515, y=298)

    # Scrollable region height calculation (scales with the number of items that
    # need to be displayed)
    region_height = len(manga_list)*41+5
    frame_canvas = tkinter.Canvas(frame, width=300, height=170, bg="white",
                             scrollregion=(0,0,300,region_height),
                             highlightthickness=0)

    # Creates another frame for displaying the checkbuttons, and places it
    # within frame_canvas using a canvas window object
    checkbtn_frame = tkinter.Frame(frame_canvas, bg="white")
    frame_canvas.create_window(0,0, window=checkbtn_frame, anchor='nw')

    # If there are more than 4 items to be displayed, configure a vertical
    # scrollbar on the frame that can be used to scroll the canvas within
    if len(manga_list) > 4:
        scrollable = tkinter.Scrollbar(frame, orient="vertical",
                                       command=frame_canvas.yview)
        scrollable.pack(side="right",fill="y")
        frame_canvas.configure(yscrollcommand=scrollable.set)

    # Packs the canvas to fill the space provided
    frame_canvas.pack(fill="both")

    # Counter variable used to keep track of each IntVar's index
    # in order to associate each one with a checkbutton
    counter = 0

    # Variable to hold the list of IntVars for each checkbutton
    intvars_list = []

    # Iterates through each element in the manga list
    for i in manga_list:

        # The second item in each element (the manga name) is assigned to the
        # manga_text variable
        manga_text = i[1]

        # If the length of the manga's name is over 25 characters long, then
        # trim the name to only show to first 25 characters and append "..."
        if len(manga_text) > 25:
            manga_text = manga_text[:25] + "..."

        # Appends an IntVar to the intvars_list variable each iteration, which
        # will be associated with the checkbutton created during each iteration
        intvars_list.append(tkinter.IntVar())
        
        # Displays the string stored in manga_text (consisting of the manga
        # name) next to a checkbutton on the checkbtn_frame
        manga_checkbutton = tkinter.Checkbutton(checkbtn_frame, text=manga_text,
                                                variable=intvars_list[counter],
                                                font=("Century Gothic", 11),
                                                activebackground="white",
                                                bg="white", )
        
        # Packs & anchors checkbutton to the west/left side, along with 5 px of
        # padding both above and below the checkbutton
        manga_checkbutton.pack(anchor="w", pady=5)

        # Increments the counter variable by 1 for each iteration
        counter += 1
        
    # -------------------------------- BUTTONS ------------------------------- #

    # Creates transparent button to remove the manga
    canvas.create_image(583, 511, image=BTN_REMOVE_ADD, tags="remove_manga")

    # Binds remove_manga button to the "remove_from_list" function
    canvas.tag_bind("remove_manga", "<ButtonPress-1>", remove_from_list)

    # Creates transparent button to delete the frame and proceed to the
    # cancelled screen
    canvas.create_image(755, 511, image=BTN_CANCEL, tags="remove_cancelled")

    # Binds remove_cancelled button to the "del_frame_cancelled" function
    canvas.tag_bind("remove_cancelled", "<ButtonPress-1>", del_frame_cancelled)

    
def remove_empty_screen():
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the remove manga empty list screen backdrop
    canvas.create_image(0, 0, image=BG_REMOVE_EMPTY, anchor="nw")

    # After 5 seconds, returns to the home screen
    canvas.after(5000, home_screen)

    
def remove_invalid_screen():
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the remove manga invalid selection screen backdrop
    canvas.create_image(0, 0, image=BG_REMOVE_INVALID, anchor="nw")

    # After 5 seconds, calls the "remove_manga_type" function
    canvas.after(5000, remove_manga_type)


def cancelled_screen(event=None):
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the cancelled screen backdrop
    canvas.create_image(0, 0, image=BG_CANCELLED, anchor="nw")

    # After 5 seconds, returns to the home screen
    canvas.after(5000, home_screen)


def success_screen():
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the success screen backdrop
    canvas.create_image(0, 0, image=BG_SUCCESS, anchor="nw")

    # After 5 seconds, returns to the home screen
    canvas.after(5000, home_screen)


def loading_screen():
    
    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the loading screen backdrop
    canvas.create_image(0, 0, image=BG_LOADING, anchor="nw")

    # Updates the canvas to display the image (required because this function is
    # called during calculations/queries that can block the creation of the
    # image unless explicitly told to update)
    canvas.update()


def thanks_screen(event=None):

    # Clears canvas to allow for this screen's elements to be displayed
    canvas.delete("all")

    # Displays the thanks screen backdrop
    canvas.create_image(0, 0, image=BG_THANKS, anchor="nw")

    # Closes the window after 3 seconds
    canvas.after(3000, window.destroy)


# ---------------------------------------------------------------------------- #
#                                 MAIN FUNCTION                                #
# ---------------------------------------------------------------------------- #
    
def main():

    # -------------------------- SCOPE DECLARATIONS -------------------------- #

    # When the window, canvas, and PhotoImages are created in this "main()"
    # function, the default behaviour is that they are only available locally
    # within the function unless otherwise specified (hence the need for global
    # statements); However, all three of the above elements (windows, canvases,
    # and PhotoImages) can be used and modified in other functions once they
    # have been globalized in the main function (in other words, a global
    # declaration does not need to be made inside every function that makes use
    # of these elements)

    global window
    global canvas
    global BG_ADD_CANCELLED
    global BG_ADD_CONFIRM
    global BG_ADD_INVALID
    global BG_ADD_MANGA
    global BG_CANCELLED
    global BG_CREDIT
    global BG_INFO
    global BG_LIST_EMPTY
    global BG_LIST_MANGA
    global BG_LOADING
    global BG_LOGIN
    global BG_RELEASES
    global BG_RELEASES_EMPTY
    global BG_RELEASES_NO_NEW
    global BG_REMOVE_EMPTY
    global BG_REMOVE_INVALID
    global BG_REMOVE_MANGA
    global BG_SUCCESS
    global BG_THANKS
    global BTN_CANCEL
    global BTN_CONFIRM
    global BTN_CREDIT
    global BTN_HOME
    global BTN_LOGIN
    global BTN_LOGOUT_INFO
    global BTN_QUIT
    global BTN_REMOVE_ADD
    global BTN_SIDEBAR
    global HOME_BACKDROPS

    # --------------------- WINDOW/CANVAS INITIALIZATION --------------------- #

    window = tkinter.Tk() # Creates the Tkinter window
    window.title("Chapter Check") # Sets the window title
    window.iconbitmap("assets/logo.ico") # Sets the window icon
    window.geometry("1000x667+50+50") # Sets the window dimensions
    window.resizable(False,False) # Sets the window to be a fixed size
    window.configure(bg="white") # Sets the window's background colour to white

    # Creates and packs the primary canvas for the application
    canvas = tkinter.Canvas(window, bg="white", width="1000",
                            height="666", highlightthickness=0)
    canvas.pack()

    # ------------------ PHOTOIMAGE CONSTANT INITIALIZATION ------------------ #
    
    # Backdrops (stored as Tkinter PhotoImages)
    BG_ADD_CANCELLED = tkinter.PhotoImage(file="assets/backdrops/bg_add_cancelled.ppm")
    BG_ADD_CONFIRM = tkinter.PhotoImage(file="assets/backdrops/bg_add_confirm.ppm")
    BG_ADD_INVALID = tkinter.PhotoImage(file="assets/backdrops/bg_add_invalid.ppm")
    BG_ADD_MANGA = tkinter.PhotoImage(file="assets/backdrops/bg_add_manga.ppm")
    BG_CANCELLED = tkinter.PhotoImage(file="assets/backdrops/bg_cancelled.ppm")
    BG_CREDIT = tkinter.PhotoImage(file="assets/backdrops/bg_credit.ppm")
    BG_INFO = tkinter.PhotoImage(file="assets/backdrops/bg_info.ppm")
    BG_LIST_EMPTY = tkinter.PhotoImage(file="assets/backdrops/bg_list_empty.ppm")
    BG_LIST_MANGA = tkinter.PhotoImage(file="assets/backdrops/bg_list_manga.ppm")
    BG_LOADING = tkinter.PhotoImage(file="assets/backdrops/bg_loading.ppm")
    BG_LOGIN = tkinter.PhotoImage(file="assets/backdrops/bg_login.ppm")
    BG_RELEASES = tkinter.PhotoImage(file="assets/backdrops/bg_releases.ppm")
    BG_RELEASES_EMPTY = tkinter.PhotoImage(file="assets/backdrops/bg_releases_empty.ppm")
    BG_RELEASES_NO_NEW = tkinter.PhotoImage(file="assets/backdrops/bg_releases_no_new.ppm")
    BG_REMOVE_EMPTY = tkinter.PhotoImage(file="assets/backdrops/bg_remove_empty.ppm")
    BG_REMOVE_INVALID = tkinter.PhotoImage(file="assets/backdrops/bg_remove_invalid.ppm")
    BG_REMOVE_MANGA = tkinter.PhotoImage(file="assets/backdrops/bg_remove_manga.ppm")
    BG_SUCCESS = tkinter.PhotoImage(file="assets/backdrops/bg_success.ppm")
    BG_THANKS = tkinter.PhotoImage(file="assets/backdrops/bg_thanks.ppm")

    # Home screen backdrops (10 different versions)
    BG_HOME_V0 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v0.ppm")
    BG_HOME_V1 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v1.ppm")
    BG_HOME_V2 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v2.ppm")
    BG_HOME_V3 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v3.ppm")
    BG_HOME_V4 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v4.ppm")
    BG_HOME_V5 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v5.ppm")
    BG_HOME_V6 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v6.ppm")
    BG_HOME_V7 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v7.ppm")
    BG_HOME_V8 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v8.ppm")
    BG_HOME_V9 = tkinter.PhotoImage(file="assets/backdrops/bg_home_v9.ppm")

    # Transparent buttons (also stored as Tkinter PhotoImages)
    BTN_CANCEL = tkinter.PhotoImage(file="assets/buttons/btn_cancel.gif")
    BTN_CONFIRM = tkinter.PhotoImage(file="assets/buttons/btn_confirm.gif")
    BTN_CREDIT = tkinter.PhotoImage(file="assets/buttons/btn_credit.gif")
    BTN_HOME = tkinter.PhotoImage(file="assets/buttons/btn_home.gif")
    BTN_LOGIN = tkinter.PhotoImage(file="assets/buttons/btn_login.gif")
    BTN_LOGOUT_INFO = tkinter.PhotoImage(file="assets/buttons/btn_logout_info.gif")
    BTN_QUIT = tkinter.PhotoImage(file="assets/buttons/btn_quit.gif")
    BTN_REMOVE_ADD = tkinter.PhotoImage(file="assets/buttons/btn_remove_add.gif")
    BTN_SIDEBAR = tkinter.PhotoImage(file="assets/buttons/btn_sidebar.gif")
    
    # Array with all home screen backdrops (note that the index numbers
    # correspond with the backdrop numbers)
    HOME_BACKDROPS = [BG_HOME_V0, BG_HOME_V1, BG_HOME_V2, BG_HOME_V3, BG_HOME_V4,
                      BG_HOME_V5, BG_HOME_V6, BG_HOME_V7, BG_HOME_V8, BG_HOME_V9]

    # ---------------------- INITIAL SCREEN AND MAINLOOP --------------------- #

    # Calls the initial login screen when the program first starts
    login_screen()

    window.mainloop() # Tkinter window mainloop

main() # Calls main function and starts the program

# ------------------------------ END OF PROGRAM ------------------------------ #
