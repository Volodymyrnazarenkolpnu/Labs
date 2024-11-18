"""Task1 of lab7, variant 2"""

browser_history = ["gmail", "Amazon", "X", "Fortran", "XXX"]

CURRENT_WEBSITE = "He"
POINTER = 0
def print_browser(pagename):
    """shows website page"""
    print(f"@ /{pagename + ".com"}   x\\ +")
    print("---------------------------------------------")
    for _i in range(14):
        print("|                                            |")
    print("---------------------------------------------")
while True:
    print("What would you like to do? search/history/exit")
    request = input()
    if request == "search":
        search = input()
        print_browser(search)
        browser_history.insert(0, search)
    elif request == "history":
        POINTER = 0
        while True:
            print_browser(browser_history[POINTER])
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
