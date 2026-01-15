# SIGHO - Manual de Usuario

## Sistema Integrado de Gestión Hotelera

**Versión:** 1.0.0  
**Fecha:** Diciembre 2025

---

## Tabla de Contenidos

1. [Bienvenido a SIGHO](#1-bienvenido-a-sigho)
2. [Inicio Rápido](#2-inicio-rápido)
3. [Acceso al Sistema](#3-acceso-al-sistema)
4. [Dashboard Principal](#4-dashboard-principal)
5. [Gestión de Reservas](#5-gestión-de-reservas)
6. [Gestión de Habitaciones](#6-gestión-de-habitaciones)
7. [Gestión de Huéspedes](#7-gestión-de-huéspedes)
8. [Procesamiento de Pagos](#8-procesamiento-de-pagos)
9. [Mantenimiento](#9-mantenimiento)
10. [Inventario](#10-inventario)
11. [Reportes](#11-reportes)
12. [Administración de Usuarios](#12-administración-de-usuarios)
13. [Configuración](#13-configuración)
14. [Preguntas Frecuentes](#14-preguntas-frecuentes)

---

## 1. Bienvenido a SIGHO

### 1.1 ¿Qué es SIGHO?

SIGHO (Sistema Integrado de Gestión Hotelera) es una solución completa para la administración de hoteles que le permite:

- Gestionar reservas de habitaciones
- Administrar información de huéspedes
- Procesar pagos en múltiples monedas
- Controlar el estado de habitaciones
- Gestionar mantenimiento e inventario
- Generar reportes detallados
- Y mucho más...

### 1.2 Beneficios del Sistema

- **Fácil de usar:** Interfaz intuitiva y amigable
- **Completo:** Todas las funciones necesarias en un solo lugar
- **Seguro:** Sistema de usuarios con roles y permisos
- **Rápido:** Acceso instantáneo a la información
- **Confiable:** Base de datos robusta y segura

---

## 2. Inicio Rápido

### 2.1 Requisitos

Para usar SIGHO necesita:
- Computadora con Windows 10 o superior
- Permisos de administrador (solo para instalación)
- Conexión a internet (solo para instalación inicial)

### 2.2 Instalación

1. Abra la carpeta del sistema SIGHO
2. Haga doble clic en `install_sigho.ps1`
3. Espere a que complete la instalación (2-5 minutos)
4. Cuando vea "Instalación completada exitosamente", cierre la ventana

### 2.3 Iniciar el Sistema

1. En la carpeta de SIGHO, haga doble clic en `start_sigho.ps1`
2. Espere unos segundos a que aparezca la ventana de login
3. Use las credenciales proporcionadas por el administrador

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

> **Nota:** Cambie la contraseña después del primer acceso por seguridad.

---

## 3. Acceso al Sistema

### 3.1 Pantalla de Login

![Pantalla de Login](login.png)

Al iniciar SIGHO verá la pantalla de login donde debe ingresar:

1. **Usuario:** Su nombre de usuario asignado
2. **Contraseña:** Su contraseña personal

Haga clic en "Iniciar Sesión" o presione Enter.

### 3.2 Tipos de Usuario

SIGHO tiene diferentes tipos de usuario según el rol:

#### Administrador
- Acceso completo a todas las funciones
- Gestión de usuarios
- Configuración del sistema

#### Gerente
- Gestión general del hotel
- Acceso a reportes completos
- Supervisión de operaciones

#### Recepcionista
- Gestión de reservas
- Check-in y check-out
- Información de huéspedes

#### Mantenimiento
- Reportes de mantenimiento
- Estado de habitaciones
- Inventario de suministros

#### Inventario
- Gestión de inventario
- Movimientos de stock
- Proveedores

### 3.3 Cerrar Sesión

Para cerrar sesión de forma segura:

1. Haga clic en su nombre de usuario (esquina superior derecha)
2. Seleccione "Cerrar Sesión"
3. Confirme la acción

---

## 4. Dashboard Principal

### 4.1 Descripción General

Al iniciar sesión verá el Dashboard principal que muestra:

- **Estadísticas del día:** Ocupación, ingresos, reservas
- **Resumen de habitaciones:** Disponibles, ocupadas, en limpieza
- **Reservas recientes:** Últimas reservas realizadas
- **Tareas pendientes:** Mantenimientos, pagos pendientes

### 4.2 Navegación

El menú lateral izquierdo contiene accesos a todas las secciones:

- **Dashboard:** Pantalla principal
- **Reservas:** Gestión de reservas
- **Habitaciones:** Estado y administración de cuartos
- **Huéspedes:** Base de datos de clientes
- **Pagos:** Procesamiento de pagos
- **Mantenimiento:** Reportes y seguimiento
- **Inventario:** Control de suministros
- **Reportes:** Informes y estadísticas
- **Usuarios:** Administración de usuarios (solo admin)
- **Configuración:** Ajustes del sistema

---

## 5. Gestión de Reservas

### 5.1 Crear una Nueva Reserva

1. Haga clic en **"Reservas"** en el menú lateral
2. Haga clic en el botón **"Nueva Reserva"**
3. Complete el formulario:

   **Información del Huésped:**
   - Busque un huésped existente o cree uno nuevo
   - Nombre completo
   - Documento de identidad
   - Teléfono y email

   **Detalles de la Reserva:**
   - Fecha de entrada (check-in)
   - Fecha de salida (check-out)
   - Tipo de habitación
   - Número de adultos
   - Número de niños
   - Solicitudes especiales (opcional)

   **Información de Pago:**
   - Moneda (VES, USD, EUR)
   - El sistema calculará automáticamente el precio total

4. Haga clic en **"Crear Reserva"**
5. El sistema generará un código de confirmación automáticamente

### 5.2 Búsqueda de Reservas

Puede buscar reservas de varias formas:

- Por código de confirmación
- Por nombre del huésped
- Por número de habitación
- Por fecha de entrada/salida
- Por estado (confirmada, check-in, completada, cancelada)

### 5.3 Check-in

Para realizar el check-in de una reserva:

1. Busque la reserva en el listado
2. Haga clic en **"Check-in"**
3. Verifique los datos del huésped
4. Confirme la habitación asignada
5. Haga clic en **"Confirmar Check-in"**
6. La habitación cambiará a estado "Ocupada"

### 5.4 Check-out

Para realizar el check-out:

1. Busque la reserva activa
2. Haga clic en **"Check-out"**
3. Verifique que no haya pagos pendientes
4. Agregue notas finales si es necesario
5. Haga clic en **"Confirmar Check-out"**
6. La habitación cambiará a estado "Limpieza"

### 5.5 Modificar una Reserva

Para cambiar los datos de una reserva:

1. Seleccione la reserva
2. Haga clic en **"Editar"**
3. Modifique los datos necesarios
4. Haga clic en **"Guardar Cambios"**

> **Nota:** Solo se pueden modificar reservas que no tengan check-in.

### 5.6 Cancelar una Reserva

Para cancelar una reserva:

1. Seleccione la reserva
2. Haga clic en **"Cancelar"**
3. Ingrese el motivo de la cancelación
4. Confirme la cancelación
5. Si hubo pagos, se procesará el reembolso correspondiente

---

## 6. Gestión de Habitaciones

### 6.1 Ver Estado de Habitaciones

La vista de habitaciones le muestra:

- Número de habitación
- Tipo de habitación
- Piso
- Estado actual
- Última actualización

Estados posibles:
- **Disponible:** Lista para ocupar
- **Ocupada:** Con huésped
- **Limpieza:** En proceso de limpieza
- **Mantenimiento:** Requiere reparación
- **Fuera de servicio:** No disponible

### 6.2 Cambiar Estado de Habitación

1. Seleccione la habitación
2. Haga clic en **"Cambiar Estado"**
3. Seleccione el nuevo estado
4. Agregue notas si es necesario
5. Confirme el cambio

### 6.3 Ver Detalles de Habitación

Haga clic en cualquier habitación para ver:

- Información completa del tipo de habitación
- Amenidades incluidas
- Precio por noche en todas las monedas
- Historial de reservas
- Historial de mantenimiento

### 6.4 Tipos de Habitación

Los tipos de habitación incluyen:

#### Individual
- Capacidad: 1 persona
- Cama sencilla
- Precio base: $25 USD

#### Doble
- Capacidad: 2 personas
- Cama matrimonial
- Balcón
- Precio base: $40 USD

#### Triple
- Capacidad: 3 personas
- Tres camas
- Minibar
- Balcón
- Precio base: $60 USD

#### Suite Junior
- Capacidad: 2 personas
- Sala de estar
- Minibar
- Balcón
- Precio base: $75 USD

#### Suite Presidencial
- Capacidad: 4 personas
- Sala de estar
- Cocina
- Minibar
- Balcón
- Precio base: $150 USD

Todas las habitaciones incluyen:
- WiFi gratuito
- TV por cable
- Aire acondicionado

---

## 7. Gestión de Huéspedes

### 7.1 Registrar Nuevo Huésped

1. Vaya a la sección **"Huéspedes"**
2. Haga clic en **"Nuevo Huésped"**
3. Complete el formulario:

   **Información Personal:**
   - Nombre
   - Apellido
   - Tipo de documento (CI, Pasaporte, RIF)
   - Número de documento
   - Fecha de nacimiento
   - Nacionalidad

   **Información de Contacto:**
   - Teléfono principal
   - Teléfono alternativo (opcional)
   - Email
   - Dirección
   - Ciudad
   - Estado
   - País

4. Haga clic en **"Guardar"**

### 7.2 Buscar Huéspedes

Puede buscar huéspedes por:
- Nombre o apellido
- Número de documento
- Email
- Teléfono

### 7.3 Ver Historial del Huésped

Al seleccionar un huésped puede ver:
- Reservas anteriores
- Pagos realizados
- Preferencias registradas
- Notas especiales

### 7.4 Actualizar Información

1. Seleccione el huésped
2. Haga clic en **"Editar"**
3. Actualice los datos necesarios
4. Guarde los cambios

---

## 8. Procesamiento de Pagos

### 8.1 Registrar un Pago

1. Vaya a **"Pagos"**
2. Haga clic en **"Nuevo Pago"**
3. Seleccione la reserva
4. Ingrese los detalles:

   **Información del Pago:**
   - Monto
   - Moneda (VES, USD, EUR)
   - Método de pago:
     * Efectivo
     * Tarjeta de crédito
     * Tarjeta de débito
     * Transferencia bancaria
     * Pago móvil

   **Datos Adicionales (según método):**
   - Número de referencia
   - Banco
   - Número de cuenta
   - Notas

5. Haga clic en **"Procesar Pago"**
6. El sistema generará un comprobante automáticamente

### 8.2 Ver Historial de Pagos

Puede filtrar pagos por:
- Fecha
- Estado (completado, pendiente, cancelado, reembolsado)
- Método de pago
- Moneda
- Reserva

### 8.3 Pagos Parciales

SIGHO permite pagos parciales:

1. El sistema muestra el balance pendiente
2. Puede registrar múltiples pagos hasta completar el monto
3. Una vez pagado completamente, la reserva se marca como "Pagada"

### 8.4 Reembolsos

Para procesar un reembolso:

1. Seleccione el pago a reembolsar
2. Haga clic en **"Reembolsar"**
3. Ingrese el monto a reembolsar (total o parcial)
4. Agregue el motivo del reembolso
5. Confirme la operación

---

## 9. Mantenimiento

### 9.1 Crear Reporte de Mantenimiento

1. Vaya a **"Mantenimiento"**
2. Haga clic en **"Nuevo Reporte"**
3. Complete el formulario:

   **Información del Reporte:**
   - Habitación afectada
   - Título del problema
   - Descripción detallada
   - Tipo de mantenimiento:
     * Preventivo
     * Correctivo
     * Emergencia
   - Prioridad:
     * Baja
     * Media
     * Alta
     * Crítica

   **Planificación:**
   - Fecha programada (opcional)
   - Costo estimado
   - Moneda

4. Haga clic en **"Crear Reporte"**

### 9.2 Gestión de Reportes

Los reportes pasan por varios estados:

1. **Pendiente:** Recién creado, esperando asignación
2. **Asignado:** Asignado a un técnico
3. **En Progreso:** El técnico está trabajando
4. **Completado:** Trabajo finalizado
5. **Cancelado:** No se realizará

### 9.3 Asignar Mantenimiento

1. Seleccione un reporte pendiente
2. Haga clic en **"Asignar"**
3. Seleccione el técnico responsable
4. Confirme la asignación

### 9.4 Iniciar Trabajo

Para comenzar un trabajo:

1. Seleccione el reporte asignado
2. Haga clic en **"Iniciar"**
3. El estado cambia a "En Progreso"
4. La habitación se marca en mantenimiento

### 9.5 Completar Mantenimiento

Al finalizar el trabajo:

1. Seleccione el reporte en progreso
2. Haga clic en **"Completar"**
3. Ingrese:
   - Costo real
   - Notas de resolución
   - Materiales utilizados
4. Confirme la finalización
5. La habitación vuelve a estado "Disponible"

---

## 10. Inventario

### 10.1 Agregar Item al Inventario

1. Vaya a **"Inventario"**
2. Haga clic en **"Nuevo Item"**
3. Complete los datos:

   **Información del Item:**
   - Código del item
   - Nombre
   - Descripción
   - Categoría:
     * Amenidades
     * Limpieza
     * Alimentos y bebidas
     * Mantenimiento
     * Oficina
   - Unidad de medida (unidad, litro, kilo, etc.)

   **Control de Stock:**
   - Cantidad actual
   - Cantidad mínima (para alertas)
   - Cantidad máxima
   - Costo unitario
   - Moneda

   **Proveedor:**
   - Nombre del proveedor
   - Contacto
   - Ubicación de almacenamiento

4. Haga clic en **"Guardar"**

### 10.2 Registrar Entrada de Stock

Para ingresar mercancía:

1. Seleccione el item
2. Haga clic en **"Entrada"**
3. Ingrese:
   - Cantidad
   - Motivo (compra, donación, ajuste)
   - Referencia del documento
   - Notas
4. Confirme la operación

### 10.3 Registrar Salida de Stock

Para registrar uso de items:

1. Seleccione el item
2. Haga clic en **"Salida"**
3. Ingrese:
   - Cantidad
   - Motivo (uso, venta, pérdida, ajuste)
   - Referencia
   - Notas
4. Confirme la operación

### 10.4 Alertas de Stock

SIGHO genera alertas automáticas cuando:
- Un item está por debajo del mínimo (necesita reabastecimiento)
- Un item está agotado

Las alertas se muestran en el Dashboard.

### 10.5 Ajuste de Inventario

Para corregir errores o hacer conteos físicos:

1. Seleccione el item
2. Haga clic en **"Ajustar"**
3. Ingrese la cantidad real actual
4. Indique el motivo del ajuste
5. Confirme

---

## 11. Reportes

### 11.1 Tipos de Reportes

SIGHO ofrece varios tipos de reportes:

#### Reporte de Ocupación
- Porcentaje de ocupación por período
- Habitaciones más/menos reservadas
- Ingresos por tipo de habitación
- Tendencias de ocupación

#### Reporte de Ingresos
- Ingresos totales por período
- Desglose por moneda
- Métodos de pago utilizados
- Comparaciones mes a mes

#### Reporte de Huéspedes
- Huéspedes nuevos vs recurrentes
- Nacionalidades más frecuentes
- Estadías promedio
- Preferencias de habitación

#### Reporte de Mantenimiento
- Reportes por estado
- Tiempo promedio de resolución
- Costos de mantenimiento
- Habitaciones con más incidencias

#### Reporte de Inventario
- Items con stock bajo
- Valor total del inventario
- Movimientos del período
- Items más utilizados

### 11.2 Generar un Reporte

1. Vaya a **"Reportes"**
2. Seleccione el tipo de reporte
3. Configure los filtros:
   - Rango de fechas
   - Filtros específicos según el reporte
4. Haga clic en **"Generar Reporte"**
5. El reporte se mostrará en pantalla

### 11.3 Exportar Reportes

Los reportes se pueden exportar en varios formatos:

1. Haga clic en **"Exportar"**
2. Seleccione el formato:
   - PDF
   - Excel
   - CSV
3. Elija la ubicación para guardar
4. El archivo se descargará automáticamente

---

## 12. Administración de Usuarios

> **Nota:** Esta sección solo está disponible para usuarios Administradores.

### 12.1 Crear Nuevo Usuario

1. Vaya a **"Usuarios"**
2. Haga clic en **"Nuevo Usuario"**
3. Complete el formulario:

   **Información del Usuario:**
   - Nombre completo
   - Nombre de usuario (único)
   - Email (único)
   - Contraseña temporal
   - Rol:
     * Administrador
     * Gerente
     * Recepcionista
     * Mantenimiento
     * Inventario
     * Visor

4. Haga clic en **"Crear Usuario"**
5. El usuario recibirá sus credenciales

### 12.2 Modificar Usuario

1. Seleccione el usuario
2. Haga clic en **"Editar"**
3. Modifique los datos necesarios
4. Guarde los cambios

### 12.3 Desactivar/Activar Usuario

Para desactivar temporalmente un usuario:

1. Seleccione el usuario
2. Haga clic en **"Desactivar"**
3. Confirme la acción

El usuario no podrá acceder al sistema hasta que lo reactive.

### 12.4 Cambiar Contraseña

Para cambiar la contraseña de un usuario:

1. Seleccione el usuario
2. Haga clic en **"Cambiar Contraseña"**
3. Ingrese la nueva contraseña
4. Confirme el cambio

### 12.5 Ver Actividad del Usuario

Puede revisar:
- Último acceso
- Historial de sesiones
- Acciones realizadas (log de auditoría)

---

## 13. Configuración

### 13.1 Configuración de la Apariencia

Puede personalizar:

- **Tema:** Claro u Oscuro
- **Color principal:** Seleccione entre varios colores
- **Tamaño de fuente:** Pequeño, Mediano, Grande

### 13.2 Configuración del Hotel

Configure la información de su hotel:

- Nombre del hotel
- Dirección
- Teléfono
- Email de contacto
- Sitio web
- Logo (opcional)

### 13.3 Configuración de Monedas

Establezca:
- Moneda principal
- Monedas aceptadas
- Tasas de cambio (se actualizan manualmente)

### 13.4 Configuración de Impuestos

Configure:
- Porcentaje de impuesto sobre habitaciones
- Porcentaje de servicio
- Otros cargos adicionales

### 13.5 Preferencias del Sistema

Ajuste:
- Idioma de la interfaz
- Formato de fecha y hora
- Zona horaria
- Unidades de medida

### 13.6 Copias de Seguridad

Es importante realizar copias de seguridad periódicas:

1. Vaya a **"Configuración"** > **"Respaldo"**
2. Haga clic en **"Crear Copia de Seguridad"**
3. Seleccione la ubicación para guardar
4. Espere a que complete el proceso

**Recomendación:** Realice copias semanales y guárdelas en una ubicación segura externa.

### 13.7 Restaurar desde Copia

Si necesita restaurar datos:

1. Vaya a **"Configuración"** > **"Respaldo"**
2. Haga clic en **"Restaurar"**
3. Seleccione el archivo de respaldo
4. Confirme la restauración
5. El sistema se reiniciará

> **Advertencia:** La restauración sobrescribirá todos los datos actuales.

---

## 14. Preguntas Frecuentes

### ¿Cómo cambio mi contraseña?

1. Haga clic en su nombre de usuario
2. Seleccione "Mi Perfil"
3. Haga clic en "Cambiar Contraseña"
4. Ingrese su contraseña actual y la nueva
5. Guarde los cambios

### ¿Qué hago si olvido mi contraseña?

Contacte al administrador del sistema para que le asigne una nueva contraseña temporal.

### ¿Puedo eliminar una reserva?

Las reservas no se pueden eliminar, solo cancelar. Esto mantiene el historial completo para auditoría.

### ¿Cómo proceso un pago en efectivo en diferentes monedas?

SIGHO maneja múltiples monedas. Simplemente seleccione la moneda del pago al registrarlo y el sistema llevará el registro correcto.

### ¿Qué hago si el sistema no responde?

1. Verifique su conexión al servidor
2. Reinicie la aplicación
3. Si el problema persiste, contacte al soporte técnico

### ¿Los datos están seguros?

Sí. SIGHO utiliza:
- Encriptación de contraseñas
- Sesiones seguras
- Base de datos local protegida
- Sistema de permisos por rol

### ¿Puedo acceder desde otra computadora?

El frontend debe instalarse en cada computadora. El backend puede ser compartido en red local (configuración avanzada).

### ¿Cómo imprimo un comprobante de pago?

1. Vaya al pago deseado
2. Haga clic en "Ver Detalles"
3. Haga clic en "Imprimir Comprobante"
4. Se abrirá la ventana de impresión de Windows

### ¿Puedo personalizar los precios de las habitaciones?

Sí. Los administradores pueden editar los tipos de habitación y ajustar precios en cualquier momento.

### ¿El sistema genera facturas automáticamente?

Sí. Al registrar un pago, el sistema genera automáticamente un comprobante con código único.

---

## Soporte Técnico

Si tiene problemas o preguntas no resueltas en este manual:

**Email:** soporte@sigho.com  
**Teléfono:** +58 424 1234567  
**Horario:** Lunes a Viernes, 8:00 AM - 6:00 PM

---

## Glosario de Términos

- **Check-in:** Entrada del huésped al hotel
- **Check-out:** Salida del huésped del hotel
- **Código de confirmación:** Identificador único de cada reserva
- **Dashboard:** Pantalla principal con resumen de información
- **Huésped:** Cliente del hotel
- **Inventario:** Control de suministros y materiales
- **JWT:** Token de seguridad para autenticación
- **Ocupación:** Porcentaje de habitaciones ocupadas
- **Reserva:** Apartado de habitación para fechas específicas
- **Token:** Clave temporal de acceso al sistema

---

**¡Gracias por usar SIGHO!**

Esperamos que este sistema facilite la gestión de su hotel y mejore la experiencia de sus huéspedes.

---

**Fin del Manual de Usuario**
