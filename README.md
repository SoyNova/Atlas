# 🚀 Atlas Autoclicker v1.0 Release  
**Publicación Oficial | Fecha: [Inserte Fecha]**  

---

## 📦 **Descargas**  
| Plataforma | Archivo | Checksum (SHA-256) |  
|------------|---------|--------------------|  
| Windows    | [AtlasAutoclicker_v1.0.exe](https://ejemplo.com/descarga) | `a1b2c3d4...` |  

---

## 🆕 **Novedades**  
### Características Principales  
- **Sistema de Autodestrucción Mejorado**:  
  - Eliminación de registros USN Journal y Prefetch.  
  - Cifrado AES-256 de logs antes de borrado.  
- **Modo Anti-Detección v2**:  
  - Jitter aumentado a ±4px (mejor imitación de movimiento humano).  
  - Delay aleatorio ajustado a distribución gaussiana.  
- **Soporte para Perfiles**:  
  - Guarda configuraciones de CPS y preferencias por usuario.  

### Correcciones  
- Solucionado: Reinicio involuntario tras usar `Destruct`.  
- Parcheado: Fuga de memoria en hilos de clic derecho.  

---

## ⚠️ **Problemas Conocidos**  
- En sistemas con Windows 11 22H2, se requiere ejecutar en modo compatibilidad (Windows 8).  
- El slider de CPS derecho puede mostrar valores incorrectos al superar 30 CPS.  

---

## 📥 **Instalación**  
1. Descarga el ejecutable desde [Assets](#).  
2. Verifica el checksum:  
   ```powershell  
   Get-FileHash .\AtlasAutoclicker_v1.0.exe -Algorithm SHA256  
