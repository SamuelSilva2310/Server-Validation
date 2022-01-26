class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ColoredMessage:

    def __init__(self):
        self.bcolors = bcolors()

    def success(self,msg="OK"):
        return self.bcolors.OKGREEN + msg + self.bcolors.ENDC
    
    def fail(self,msg="!!"):
        return self.bcolors.FAIL + msg + self.bcolors.ENDC

class Message:
    
    def __init__(self):
        self.width = 100
        self.colored_message = ColoredMessage()
        self.filler_char = "-"
        self.content = ""

    def add_section(self,header,content):
        self.add_header(header)
        for result in content:
            if result["passed"]:
                content = f"[{self.colored_message.success()}] {result['message']}"   
            else:
                content = f"[{self.colored_message.fail()}] {result['message']}" 
            self.add_content(content)



    def add_content(self, content):
        self.content += "\n"
        self.content += content


    def add_header(self, header):
        self.content += "\n\n"
        self.content += header.title().center(self.width, self.filler_char)
    
    def get_content(self):
        return self.content



# message = Message()
# # result = {
# #     "passed": True,
# #     "messages": [
# #             {"message1" : False},
# #             {"message2" : True}
# #             ]
# #         }

# result = [{"passed": True,"message": "This is a message"},
#           {"passed": False,"message": "This is another"}]


# # result = [{"teste123": True},{"teste123": False},{"teste123": False},{"abs": True}]
# message.add_section("Titulo", result)

# print(message.content)

