"""Task1 of lab7, variant 2"""

browser_history = ["gmail", "Amazon", "X", "Fortran", "XXX"]

current_website = "He"
pointer = 0
def print_browser(pagename):
    print(f"@ /{pagename + ".com"}   x\\ +")
    print("---------------------------------------------")
    for i in range(14):
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
        pointer = 0 
        while True:
            print_browser(browser_history[pointer])
            print("next/previous/exit")
            request = input()
            if request == "next":
                pointer += 1
            elif request == "previous":
                pointer -= 1
            elif request == "exit":
                break
            if pointer < 0:
                pointer += 1
                print("earliest entry, can't go back")
            if pointer > (len(browser_history) - 1):
                pointer -= 1
                print("bottom of history reached")
    elif request == "exit":
        break

    
