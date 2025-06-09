import re

def limpiar_texto(texto):
    # Asegura formato de precios tipo "$35.900 a $430.800"
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*(hasta|a)\s*(\d{2,3}\.\d{3})', r'$\1 a $\3', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})hasta(\d{2,3}\.\d{3})', r'$\1 a $\2', texto)
    texto = re.sub(r'(\d{2,3}\.\d{3})\s*-\s*(\d{2,3}\.\d{3})', r'$\1 a $\2', texto)
    return texto

# Ruta del archivo original
ruta_entrada = "cltiene_data.txt"
# Ruta del nuevo archivo limpio
ruta_salida = "cltiene_data_limpio.txt"

# Leer y limpiar el texto
with open(ruta_entrada, "r", encoding="utf-8") as archivo:
    contenido = archivo.read()

contenido_limpio = limpiar_texto(contenido)

# Guardar el nuevo archivo limpio
with open(ruta_salida, "w", encoding="utf-8") as archivo:
    archivo.write(contenido_limpio)

print("✅ Archivo limpio guardado como:", ruta_salida)
