# Guía para Convertir Documentación a PDF o DOCX

## Opción 1: Usando Microsoft Word (Más Fácil)

### Pasos:
1. Abrir Word
2. Ir a **Archivo** > **Abrir**
3. Seleccionar el archivo `.md` (DOCUMENTACION_TECNICA.md o MANUAL_DE_USUARIO.md)
4. Word abrirá el archivo con formato
5. Ir a **Archivo** > **Guardar como**
6. Seleccionar formato:
   - **PDF** para documento final
   - **Word (.docx)** para seguir editando
7. Guardar

### Ventajas:
- No requiere instalación adicional
- Interfaz familiar
- Permite editar antes de exportar
- Mantiene el formato

---

## Opción 2: Usando Google Docs (Online, Gratis)

### Pasos:
1. Ir a https://docs.google.com
2. Crear un nuevo documento
3. Ir a **Archivo** > **Importar**
4. Subir el archivo `.md`
5. Esperar que procese
6. Ir a **Archivo** > **Descargar como**
7. Seleccionar **PDF** o **Microsoft Word (.docx)**

### Ventajas:
- Completamente online
- Gratis
- Fácil compartir
- Accesible desde cualquier dispositivo

---

## Opción 3: Usando Pandoc (Profesional)

### Instalación:
1. Descargar Pandoc desde: https://pandoc.org/installing.html
2. Instalar siguiendo el asistente

### Convertir a PDF:
```powershell
# En PowerShell, en la carpeta docs/
pandoc DOCUMENTACION_TECNICA.md -o DOCUMENTACION_TECNICA.pdf
pandoc MANUAL_DE_USUARIO.md -o MANUAL_DE_USUARIO.pdf
```

### Convertir a DOCX:
```powershell
pandoc DOCUMENTACION_TECNICA.md -o DOCUMENTACION_TECNICA.docx
pandoc MANUAL_DE_USUARIO.md -o MANUAL_DE_USUARIO.docx
```

### Con Tabla de Contenidos:
```powershell
pandoc DOCUMENTACION_TECNICA.md -o DOCUMENTACION_TECNICA.pdf --toc --toc-depth=3
```

### Ventajas:
- Conversión profesional
- Gran control sobre el formato
- Soporta muchos formatos
- Automatizable

---

## Opción 4: Herramientas Online

### Sitios Recomendados:

1. **Dillinger** (https://dillinger.io/)
   - Pegar el contenido
   - Exportar a PDF o HTML
   - Gratis y sin registro

2. **MarkdownToPDF** (https://www.markdowntopdf.com/)
   - Subir archivo .md
   - Descargar PDF
   - Rápido y simple

3. **CloudConvert** (https://cloudconvert.com/)
   - Soporta MD → PDF, DOCX, HTML
   - Permite configuración avanzada
   - Gratis hasta cierto límite

---

## Recomendaciones por Caso de Uso

### Para Imprimir:
- **Formato:** PDF
- **Herramienta:** Word o Pandoc
- **Configuración:**
  - Márgenes: 2.5 cm todos los lados
  - Fuente: 11-12 pt
  - Interlineado: 1.15

### Para Editar/Personalizar:
- **Formato:** DOCX (Word)
- **Herramienta:** Word
- **Ventaja:** Puedes agregar logo, cambiar colores, ajustar formato

### Para Distribuir Digitalmente:
- **Formato:** PDF
- **Herramienta:** Cualquiera
- **Ventaja:** Se ve igual en todos los dispositivos

### Para Web/Intranet:
- **Formato:** HTML
- **Herramienta:** Pandoc
- **Comando:**
  ```powershell
  pandoc MANUAL_DE_USUARIO.md -o manual.html --standalone --css=style.css
  ```

---

## Mejoras de Formato Opcionales

### Agregar Portada (en Word):
1. Insertar página en blanco al inicio
2. Agregar:
   - Logo del hotel
   - Título del documento
   - Versión
   - Fecha
   - Nombre de la empresa

### Agregar Numeración de Páginas:
1. En Word: **Insertar** > **Número de página**
2. Seleccionar posición (abajo centro es común)

### Agregar Encabezados y Pies:
1. **Insertar** > **Encabezado**
2. Agregar nombre del documento
3. **Insertar** > **Pie de página**
4. Agregar información de contacto

### Crear Índice Automático (Word):
1. Colocar cursor donde quieres el índice
2. **Referencias** > **Tabla de contenido**
3. Seleccionar estilo
4. Word generará el índice automáticamente

---

## Problemas Comunes y Soluciones

### "Word no abre el archivo .md"
**Solución:** 
- Cambiar extensión temporal a .txt
- Abrir en Word
- Guardar como .docx

### "Se pierden los formatos al convertir"
**Solución:**
- Usar Pandoc en lugar de conversores online
- O editar en Word después de abrir

### "El PDF se ve raro"
**Solución:**
- Ajustar márgenes en Word antes de exportar
- Usar Pandoc con plantilla personalizada

### "Quiero agregar imágenes"
**Solución:**
- Abrir el .md en Word
- Insertar imágenes donde desees
- Guardar como PDF

---

## Scripts de Conversión Automática

### Convertir Ambos Documentos a PDF:
```powershell
# Guardar como convert_all.ps1
cd docs

# Documentación Técnica
pandoc DOCUMENTACION_TECNICA.md -o DOCUMENTACION_TECNICA.pdf `
  --toc --toc-depth=3 `
  -V geometry:margin=2.5cm `
  -V fontsize=11pt

# Manual de Usuario
pandoc MANUAL_DE_USUARIO.md -o MANUAL_DE_USUARIO.pdf `
  --toc --toc-depth=3 `
  -V geometry:margin=2.5cm `
  -V fontsize=11pt

Write-Host "Conversion completada!" -ForegroundColor Green
```

### Convertir a DOCX:
```powershell
# Guardar como convert_to_docx.ps1
cd docs

pandoc DOCUMENTACION_TECNICA.md -o DOCUMENTACION_TECNICA.docx
pandoc MANUAL_DE_USUARIO.md -o MANUAL_DE_USUARIO.docx

Write-Host "Archivos DOCX creados!" -ForegroundColor Green
```

---

## Mi Recomendación

**Para uso inmediato:**
1. Abrir los archivos .md en Microsoft Word
2. Revisar y ajustar formato si necesario
3. Guardar como PDF

**Para uso profesional:**
1. Instalar Pandoc
2. Usar los scripts de conversión incluidos arriba
3. Personalizar con logo y portada en Word
4. Distribuir los PDFs finales

---

Ambos documentos están en:
- **Documentación Técnica:** `docs/DOCUMENTACION_TECNICA.md`
- **Manual de Usuario:** `docs/MANUAL_DE_USUARIO.md`
