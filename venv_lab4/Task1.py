class Video:
    def __init__(self, __name = "", __author = "", __length = "", __views = "", vimeo_views = 0):
        self.__length = __length
        self.__author = __author
        self.__views = __views
        self.__name = __name
        self.vimeo_views = 0
        self.hype_index = 0
        self.description = ""
    
    def get_name(self):
        return (f"Name = {self.__name}")

    def get_vimeo_views(self):
        return (f"Vimeo_views = {self.vimeo_views}")

    def get_author(self):
        return (f"Author = {self.__author}")

    def get_views(self):
        return (f"Views = {self.__views}")
    
    def get_length(self):
        return (f"length = {self.__length}")
    
    def set_name(self, __name):
        self.__name = __name
        return (f"name is now {self.__name}")
    
    def set_vimeo_views(self, __name):
        self.vimeo_views += vimeo_views
        return (f"Vimeo_Views is now {self.vimeo_views}")

    def set_author(self, __author):
        self.__author = __author
        return (f"author is now {self.__author}")
    
    def set_views(self, __views):
        self.__views = __views
        return (f"views is now {self.__views}")
    
    def set_length(self, __length):
        self.__length = __length
        return (f"length is now {self.__length}")


    def __repr__(self):
        return f"{self.__name}, {self.__author},{self.__length}, {self.__views}"
    
    def __str__(self):
        return f"Name = {self.__name}, Author = {self.__author}, Length = {self.__length}, Views = {self.__views}"

    def __del__(self):
        return f"{self.__str__} is removed"

def Main():
    gangam = Video("gangam", "somebody", 120, -432123)
    havana = Video("havana", "camila cabello", 110, 6734123)
    creeper_aw_man = Video("creeper, aw man", "user1", 120, 432123)
    videos = [gangam, havana, creeper_aw_man]
    for vid in videos:
        print(vid.get_author())
        print(vid.get_length())
        print(vid.get_name())
        print(vid.get_views())
        vid.__str__()
    min_video = videos[0]
    for vid in videos:
        if vid.get_vimeo_views() < min_video.get_vimeo_views():
            min_video = vid
    print(min_video)
Main()