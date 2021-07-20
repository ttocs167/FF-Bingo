from bs4 import BeautifulSoup as bs
import json
import uuid

class htmlCreator:
    def generate_html_file(self, jsonObject):
        soup = self.__getTemplateFileData()
        jsonData = json.loads(jsonObject)
        self.__appendDivs(soup, jsonData)
        self.__saveFile(soup)


    def __saveFile(self, soup):
        myuuid = uuid.uuid4()
        resultFilename = "./output_folder/bingo-{}.html".format(myuuid) 
        with open(resultFilename, "w") as file:
            file.write(str(soup))



    def __appendDivs(self, soup, jsonObject):
        container = soup.div
        freeSpaceLocation = self.__getFreeSpaceLocation(jsonObject)

        for i in range(0, 25):
            tag = soup.new_tag("div")
            tag["class"] = "grid-item"
            tag["id"] = "element{}".format(i)
            if i is not freeSpaceLocation:
                tag.string = jsonObject['spaces'][i]
            else:
                tag["class"] += " free-item"
                tag.string = jsonObject['free_spaces'][0]
    
            container.append(tag)


    def __getFreeSpaceLocation(self, jsonObject):
        print(jsonObject)
        x, y = jsonObject['free space coordinates']

        return x + y * 5


    def __getTemplateFileData(self):
        with open("./resources/templates/websiteTemplate.html") as file:
            txt = file.read()
            return bs(txt, "lxml")
