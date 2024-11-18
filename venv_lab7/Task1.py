"""Task1 of lab7, variant 2"""

browser_history = ["gmail", "Amazon", "X", "Fortran", "Steam", "Oracle"]

website_list = []
POINTER = 0
def print_browser():
    """prints webpage"""
    print("---------------------------------------------")
    for _i in range(14):
        print("|                                            |")
    print("---------------------------------------------")
    
def print_browser_history(pagename):
    """shows website history"""
    print(f"@ /{pagename + ".com"}   x\\ +")
    print_browser()

def print_browser_current_pages():
    """shows website pages"""
    _line = "@ "
    _fits = False
    while not _fits:
        _l = _line
        for page in website_list:
            _l += f"/{page}.com   \\ "
        if len(_l) > 50 and len(website_list) > 1:
            website_list.pop(0)
        else:
            break
    for page in website_list:
        _line += f"/{page}.com   \\ "
    _line += "+"
    print(_line)
    print_browser()

while True:
    print("What would you like to do? search/history/exit")
    request = input()
    if request == "search":
        search = input()
        website_list.append(search)
        print_browser_current_pages()
        browser_history.insert(0, search)
    elif request == "history":
        POINTER = 0
        while True:
            print_browser_history(browser_history[POINTER])
            print("next/previous/exit")
            request = input()
            if request == "next":
                POINTER += 1
            elif request == "previous":
                POINTER -= 1
            elif request == "exit":
                break
            if POINTER < 0:
                POINTER += 1
                print("earliest entry, can't go back")
            if POINTER > (len(browser_history) - 1):
                POINTER -= 1
                print("bottom of history reached")
    elif request == "exit":
        break
