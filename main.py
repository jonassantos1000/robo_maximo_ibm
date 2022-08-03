import urllib.request
import re
import os
from datetime import datetime

contador = 1

def download(link, curso):
    link_video = link
    diretorio = get_diretorio(link_video, curso)
    urllib.request.urlretrieve(link_video, diretorio)

def get_diretorio(link_video,curso):
    padrao = "\w{1,50}.mp4"
    curso = curso.replace(".txt", "")

    #cria a pasta do video caso não exista
    if not os.path.isdir(f'./video/{curso}'):
        os.mkdir(f'./video/{curso}')
    return f'./video/{curso}/Aula {contador} - '+re.search(padrao, link_video).group()

# faz download dos videos
for file in os.listdir("./links"):
    if file.endswith(".txt"):
        with open('./links/'+os.path.join(file), 'r', encoding='utf-8') as arquivo:
            for link in arquivo:
                download(link, file)
                contador = contador + 1
        contador = 1
