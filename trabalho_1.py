import cv2
import os

pasta_imagens = 'caminho/para/sua/pasta_de_fotos'
dataset_processado = []

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')): #ve se é imagem
        
        caminho_completo = os.path.join(pasta_imagens, nome_arquivo)
        img_original = cv2.imread(caminho_completo)
        
        if img_original is not None: #leu mesmo
            img_recortada = img_original[0:512, 0:512]
            #para cinza
            img_cinza = cv2.cvtColor(img_recortada, cv2.COLOR_BGR2GRAY)
            dataset_processado.append(img_cinza)

print(f"Todas as imasgens foram processadas. Total de imagens processadas: {len(dataset_processado)}")