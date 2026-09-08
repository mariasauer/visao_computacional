import cv2
import os

pasta_imagens = 'dataset/'
pasta_destino = 'dataset_processado'
dataset_processado = []

if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)
    print(f"Pasta '{pasta_destino}' criada com sucesso!")

nome = 1

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')): #ve se é imagem
        
        caminho_completo = os.path.join(pasta_imagens, nome_arquivo)
        img_original = cv2.imread(caminho_completo)
        
        if img_original is not None: 
            #resize da imagem pq o corte estava ruim, mas antes deixa a imagem quadrada

            h, w, _ = img_original.shape
            # menor lado da imagem
            tamanho_quadrado = min(h, w)

            # encontra o centro
            centro_y, centro_x = h // 2, w // 2
            metade_quadrado = tamanho_quadrado // 2

            # corta
            img_quadrada = img_original[
                centro_y - metade_quadrado : centro_y + metade_quadrado,
                centro_x - metade_quadrado : centro_x + metade_quadrado
            ]

            # resize da imagem
            img_recortada = cv2.resize(img_quadrada, (512, 512))
            
            #muda a cor
            img_cinza = cv2.cvtColor(img_recortada, cv2.COLOR_BGR2GRAY)
            dataset_processado.append(img_cinza)

            nome_novo_arquivo = f'animal_cinza_{nome}.jpg'
            caminho_salvar = os.path.join(pasta_destino, nome_novo_arquivo)
            cv2.imwrite(caminho_salvar, img_cinza)
            nome += 1
            print(f"Imagem salva: {nome_novo_arquivo}")

print(f"Todas as imagens foram processadas. Total de imagens processadas: {len(dataset_processado)}")