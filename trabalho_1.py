import cv2
import os
import numpy as np

def extrair_textura(img_cinza, banco_filtros):
    vetor_caracteristicas = []
    img_escala = img_cinza.copy()
    
    # 3 escalas
    for escala in range(3):
        
        # 8 filtros na escala atual
        for nome, kernel in banco_filtros:
            resposta = cv2.filter2D(img_escala, cv2.CV_64F, kernel)
            
            # pega o valor absoluto da resposta do filtro
            resposta_abs = np.abs(resposta)
            
            # calcula a media local da textura
            resposta_media = cv2.blur(resposta_abs, (7, 7))
            
            resposta_512 = cv2.resize(resposta_media, (512, 512))
            
            vetor_caracteristicas.append(resposta_512)
            
        # reduz a imagem pela metade com Gaussiano para a próxima iteração
        img_escala = cv2.pyrDown(img_escala)
    
    # coloca tudo junto
    mapa_textura_24d = np.dstack(vetor_caracteristicas)
    
    return mapa_textura_24d


def criar_banco_filtros():
    filtros = []
    
    ksize = 21      
    sigma = 3.0      
    # 0, 45, 90 e 135 graus em radianos
    theta_angles = [0, np.pi/4, np.pi/2, 3*np.pi/4] 
    lamda = 8.0     
    gamma = 0.5      
    psi = 0          

    # criacao dos 4 filtros de orientacao (Gabor - opencv)
    for theta in theta_angles:
        kernel_gabor = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, psi, ktype=cv2.CV_32F)
        kernel_gabor /= 1.5 * kernel_gabor.sum() 
        filtros.append(('Gabor', kernel_gabor))
        
    # 4 filtros circulares (Laplaciano do Gaussiano)
    sigmas_circulares = [1.0, 2.0, 3.0, 4.0]
    for sig in sigmas_circulares:
        k_1d = cv2.getGaussianKernel(ksize, sig)
        k_2d = k_1d * k_1d.T
        kernel_log = cv2.Laplacian(k_2d, cv2.CV_64F)
        filtros.append(('Circular_LoG', kernel_log))
        
    return filtros


# preparando as imagens
pasta_imagens = 'dataset/'
pasta_destino = 'dataset_processado'
dataset_processado = []

if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)
    print(f"Pasta '{pasta_destino}' criada :)")

nome = 1


# criando os filtros
meu_banco_de_filtros = criar_banco_filtros()
print(f"Banco de filtros criado! Total de filtros: {len(meu_banco_de_filtros)}")



for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')): #ve se é imagem
        
        caminho_completo = os.path.join(pasta_imagens, nome_arquivo)
        img_original = cv2.imread(caminho_completo)
        
        if img_original is not None: 
            
            # deixa a imagem quadrada
            h, w, _ = img_original.shape
            tamanho_quadrado = min(h, w)
            centro_y, centro_x = h // 2, w // 2
            metade_quadrado = tamanho_quadrado // 2

            # corta
            img_quadrada = img_original[
                centro_y - metade_quadrado : centro_y + metade_quadrado,
                centro_x - metade_quadrado : centro_x + metade_quadrado
            ]

            # resize e mudança de cor
            img_recortada = cv2.resize(img_quadrada, (512, 512))
            img_cinza = cv2.cvtColor(img_recortada, cv2.COLOR_BGR2GRAY)
            dataset_processado.append(img_cinza)

            # salva
            nome_novo_arquivo = f'animal_cinza_{nome}.jpg'
            caminho_salvar = os.path.join(pasta_destino, nome_novo_arquivo)
            cv2.imwrite(caminho_salvar, img_cinza)
            
            # extrai a textura para a imagem
            mapa_textura = extrair_textura(img_cinza, meu_banco_de_filtros)
            print("Textura extraída com sucesso para esta imagem!")
            
            
            # kmeans
            Z = mapa_textura.reshape((-1, 24))
            Z = np.float32(Z) 
            
            # agrupamento 
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            
            # 4 clusters fica mais visivel, 3 seria suficiente, mas 4 clusters deixa a segmentação mais clara
            K = 4
            _, label, _ = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            cores = np.array([
                [255, 0, 0],     
                [0, 255, 0],    
                [0, 0, 255],    
                [255, 255, 0],
                [255, 0, 255],   
                [0, 255, 255],   
                [0, 128, 255],   
                [128, 0, 128]
            ], dtype=np.uint8)
            
            resultado_cores = cores[label.flatten()]
            
            imagem_segmentada = resultado_cores.reshape((512, 512, 3))
            
            nome_arq_seg = f'segmentado_{nome}.jpg'
            caminho_salvar_seg = os.path.join(pasta_destino, nome_arq_seg)
            cv2.imwrite(caminho_salvar_seg, imagem_segmentada)
            

            nome += 1
            print(f"Imagem salva: {nome_novo_arquivo}")

print(f"\nTodas as imagens foram processadas :) . Total: {len(dataset_processado)}")


