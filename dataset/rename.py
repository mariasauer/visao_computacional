import os
import glob

# Pega todos os arquivos de imagem na pasta atual
arquivos = glob.glob('*.jpg') + glob.glob('*.jpeg') + glob.glob('*.png')

# Ordena para garantir que a sequência faça sentido
arquivos.sort()

contador = 1
for arquivo in arquivos:
    # Pula arquivos que já estejam renomeados corretamente
    if arquivo.startswith('animal_'):
        continue
        
    extensao = os.path.splitext(arquivo)[1].lower()
    novo_nome = f"animal_{contador}{extensao}"
    
    # # Se o nome novo já existir (por uma rodada anterior), tenta o próximo número
    # while os.path.exists(novo_nome):
    #     contador += 1
    #     novo_nome = f"animal_{contador}{extensao}"
        
    os.rename(arquivo, novo_nome)
    print(f"Renomeou: {arquivo} -> {novo_nome}")
    contador += 1
    
print("Renomeação concluída!")