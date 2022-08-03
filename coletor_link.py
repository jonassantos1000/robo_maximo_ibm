from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class ColetorDeLink():
    def __init__(self):
        self._browser = None

    #Abre o navegador caso ainda não esteja aberto e faz a requisição no link passado por parametro
    def requisicao_browser(self, link):
        if self._browser == None:
            self._browser = webdriver.Chrome(ChromeDriverManager().install())
        self._browser.get(link)
        time.sleep(3)
        return self._browser

    #Realiza a autenticação no site
    def login(self,link):
        browser =  self.requisicao_browser(link)

        #colocar e-mail da ibm
        username = browser.find_element(By.XPATH, "//*[@id='username']").send_keys("###########");
        time.sleep(2)
        browser.find_element(By.XPATH,"//*[@id='continue-button']").click()
        time.sleep(2)

        #colocar senha da ibm
        password = browser.find_element(By.XPATH, "//*[@id='password']").send_keys("###########");
        time.sleep(2)
        login_attempt = browser.find_element(By.XPATH, "//*[@id='signinbutton']").click()
        time.sleep(3)
        self.extrair_lista_links()

    #Faz a extração das listas de links para saber em qual pagina os videos estão presente
    def extrair_lista_links(self):
        for link in self.listagem_links_curso():
            result = link.split(';')
            link = result[0]
            curso = result[1]
            self.conteudo = self.requisicao_browser(link).page_source
            soup = BeautifulSoup(self.conteudo,"html5lib")
            lista = soup.find_all('a', {"class": ""})

            for tag in lista:
                link_video = tag.get('href')
                video = link_video.find('//learn')
                quiz = link_video.find('quiz')
                if(video != -1 and quiz == -1):
                   self.extrair_link_video(link_video,curso)

        self._browser.close()

    #Faz a extração do link real do video, onde o video esta sendo armazenado e grava no arquivo txt.
    def extrair_link_video(self, link, curso):
        result =  self.requisicao_browser(link).page_source
        soup = BeautifulSoup(result, "html5lib").find("video")
        time.sleep(1)
        if(soup != None):
            curso= curso.replace("\n","")
            with open(f'./links/{curso}.txt', 'a+', encoding='utf-8') as arquivo:
                arquivo.write(soup.get('src').replace(" ", "%20"))
                arquivo.write('\n')

    #Pega a lista de curso que deseja extrair os videos
    def listagem_links_curso(self):
        lista = []
        with open('lista_curso.txt', 'r', encoding='utf-8') as arquivo:
            for link in arquivo:
                lista.append(link)
        return lista


coletor = ColetorDeLink()
coletor.login("https://learn.ibm.com/course/view.php?id=6667")