# pdf_extractor

Script que lee un archivo PDF y devuelve su texto completo.

## Librería utilizada

Se evaluaron tres opciones:

| Librería   | Pros                                          | Contras                                      | Veredicto  |
|------------|-----------------------------------------------|----------------------------------------------|------------|
| PyPDF2     | Muy conocida, mucha documentación             | Deprecada, reemplazada por pypdf             | ❌ No usar |
| pymupdf    | Muy rápida, gran precisión                    | Requiere binarios del sistema, más compleja  | ⚠️ Opcional |
| pdfplumber | Simple, excelente extracción de texto/tablas  | Más lenta que pymupdf en PDFs grandes        | ✅ Elegida |

Se eligió **pdfplumber** por su simplicidad y calidad de extracción.

## Cómo correr los tests

1. Colocar un archivo PDF de ejemplo en la carpeta `/tests` con el nombre `sample.pdf`
2. Ejecutar:

```bash
pytest tests/ -v
```

> Sin el `sample.pdf`, los tests que dependen de un PDF real se saltean automáticamente. Los demás pasan igual.
