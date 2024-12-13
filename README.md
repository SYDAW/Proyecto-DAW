# BookVerse

## Descripción del Proyecto

### Introducción

El proyecto **BookVerse** consiste en el desarrollo de una biblioteca/librería digital accesible a través de una aplicación web. BookVerse realizará las mismas funciones que una biblioteca tradicional, pero toda la gestión se llevará a cabo en línea, permitiendo ver el catálogo completo de libros disponibles.

### Objetivos de la Plataforma

La plataforma permitirá a los usuarios realizar las siguientes acciones:

- **Consulta y búsqueda de libros**: 
  - Los usuarios podrán explorar el catálogo digital a través de un sistema de búsqueda intuitivo que permitirá filtrar los resultados por título, autor, género, etc.
  
- **Reserva de libros físicos o digitales**: 
  - A través de la aplicación, los usuarios tendrán la opción de reservar tanto ejemplares físicos disponibles en la biblioteca como libros digitales. Este sistema de reservas asegurará que los usuarios puedan acceder a los libros deseados en un momento posterior, optimizando el tiempo de visita a la biblioteca o facilitando el acceso desde cualquier lugar.

- **Compra de libros digitales o físicos**: 
  - Los usuarios podrán adquirir libros tanto en formato físico como digital.

- **Lectura en línea (opcional)**: 
  - Se integrará un visor de libros electrónicos para permitir la lectura en línea si el tiempo lo permite.

### Características Adicionales

- **Registro y gestión de usuarios**: 
  - Los usuarios podrán crear cuentas, gestionar sus perfiles, revisar su historial de reservas y compras.
  
- **Cesta de compra**: 
  - Un carrito donde los usuarios podrán agregar o eliminar libros antes de realizar la compra.

- **Sección de libros reservados**: 

  En esta sección, el usuario podrá visualizar todos los libros que tenga reservados, junto con       los   plazos correspondientes. Las condiciones para los libros reservados son las siguientes:

  1. **Libros físicos**:
      - Los usuarios dispondrán de 30 días para devolver los libros físicos, tras lo cual, si no los devuelven, serán sancionados.
      - Para reservar libros físicos, se requerirá un depósito como fianza, que será reembolsado tras la devolución en buenas condiciones.

  2. **Libros digitales**:
      - Los usuarios tendrán acceso a los libros digitales durante un periodo de 25 días. Una vez pasado este plazo, el acceso al libro se deshabilitará automáticamente.
    
- **Panel de administración**:

    Área para administradores con herramientas para gestionar el catálogo, reservas, compras, y         sanciones.
  
  1. **Gestión del catálogo de libros**:
      - Posibilidad de añadir, editar o eliminar libros del catálogo digital.
        
  2. **Gestión de las reservas de libros de los usuarios**:
      - Supervisar y administrar las reservas realizadas por los usuarios, tanto de libros físicos como digitales.

  3. **Gestión de reseñas**:
      - Revisar, moderar y eliminar reseñas realizadas por los usuarios para garantizar contenido adecuado y relevante.
      
   4. **Gestión de compras**:
      - Visualizar y administrar todas las compras realizadas por los usuarios, ya sean de libros físicos o digitales.
  

- **Sistema de comentarios y valoraciones**: 
  - Los usuarios podrán dejar reseñas y valoraciones de los libros.

## Justificación del Proyecto

La creación de **BookVerse** responde a la necesidad de modernizar las bibliotecas y librerías tradicionales. Con el avance de la tecnología y la digitalización, las plataformas como BookVerse ofrecen una gestión eficiente de los recursos bibliográficos y una experiencia personalizada para los usuarios. Los cambios en los hábitos de lectura, con la creciente popularidad de los libros digitales y el comercio electrónico, también justifican la creación de esta plataforma.

BookVerse permitirá a los lectores acceder a una extensa colección de libros físicos y digitales desde la comodidad de su hogar, mejorando su experiencia mediante la opción de leer en línea, gestionar su cuenta personal y adquirir libros de manera sencilla.

## Alcance del Proyecto

El alcance de **BookVerse** abarca las siguientes áreas clave:

1. **Plataforma web**:
   - Búsqueda y consulta de libros filtrando por título, autor y género.
   - Reserva de libros físicos y compra de libros digitales o físicos.
   
2. **Gestión de usuarios**:
   - Registro de cuentas personales, administración de reservas, compras y comentarios.
   
3. **Lectura en línea (opcional)**:
   - Implementación de un visor de libros electrónicos si el tiempo lo permite.

4. **Panel de administración**:
   - Gestión del catálogo, reservas, compras y sanciones de usuarios.

5. **Funcionalidades adicionales**:
   - Carrito de compras.
   - Sistema de comentarios y valoraciones.

6. **Desarrollo técnico**:
   - Desarrollo del frontend y backend, integración con una base de datos para la gestión de la información.

## Valoración de Alternativas Existentes en el Mercado

Existen diversas alternativas en el mercado, tanto en el ámbito de bibliotecas digitales como en tiendas online de libros:

- **Amazon Kindle**: Líder en la venta de libros electrónicos, pero centrado más en ventas que en la experiencia de una biblioteca pública.
  
- **Google Books**: Permite la compra de libros digitales y lectura online, pero no ofrece reservas de libros físicos.
  
- **Goodreads**: Plataforma de reseñas y comunidad lectora, sin opción de compra o reserva directa de libros.
  
- **OverDrive/Libby**: Ofrece préstamos de libros electrónicos y audiolibros mediante bibliotecas públicas, pero no incluye venta ni reserva de libros físicos.

**BookVerse** se distingue por integrar la reserva de libros físicos, la compra de libros digitales o físicos, y la lectura en línea, brindando una experiencia unificada para bibliotecas y librerías.

## Stack Tecnológico Elegido

El desarrollo de **BookVerse** utilizará las siguientes tecnologías:

### Frontend:
- **HTML** y **CSS**: Para la creación y diseño de la interfaz de usuario.
- **JavaScript**: Para añadir interactividad y mejorar la experiencia del usuario.
- **Boostrap5**: Framework de diseño front-end que facilita la creación de diseños modernos, responsivos y consistentes.

### Backend:
- **Django**: Framework de Python que facilitará la estructura sólida y segura de la plataforma.
- **Python**: Lenguaje de programación para la lógica del backend.

### Base de Datos:
- **SQLite3**: Sistema de gestión de bases de datos ligero que viene ya incluidas en la aplicación. Se utilizará para almacenar y gestionar toda la información de libros, usuarios y transacciones de manera sencilla y eficiente durante el desarrollo inicial del proyecto.

### Despliegue de la aplicación web:
- **Pythonanywhere**: Sistema de gestión de bases de datos ligero que viene ya incluidas en la aplicación. Se utilizará para almacenar y gestionar toda la información de libros, usuarios y transacciones de manera sencilla y eficiente durante el desarrollo inicial del proyecto.

## Objetivos del Proyecto

El objetivo principal de **BookVerse** es proporcionar una plataforma digital que funcione tanto como una biblioteca y una librería, permitiendo a los usuarios acceder de manera eficiente y cómoda a una gran variedad de libros físicos y digitales.

### Objetivos Específicos:

1. **Facilitar el acceso a libros**: 
   - Proporcionar una interfaz intuitiva para que los usuarios puedan buscar, explorar, reservar y comprar libros físicos y digitales.

2. **Mejorar la experiencia de los lectores**: 
   - Integrar funcionalidades que mejoren la experiencia del lector, como la capacidad de dejar comentarios, valoraciones y recomendaciones para otros usuarios.

3. **Ofrecer la posibilidad de leer en línea**: 
   - Si el tiempo lo permite, integrar una funcionalidad que permita la lectura de libros electrónicos directamente desde la plataforma.

4. **Promover la compra de libros**: 
   - Crear una sección para que los usuarios puedan comprar libros (físicos y digitales) a través de una cesta de compra, con opciones de envío a domicilio.

5. **Fomentar una comunidad activa**: 
   - Permitir que los usuarios interactúen a través de valoraciones, reseñas y recomendaciones para crear un entorno participativo en torno a la lectura.

## Requisitos del Sistema

### Requisitos Funcionales

1. **Registro y autenticación de usuarios**:
   - Los usuarios podrán registrarse, iniciar sesión y gestionar su perfil.
   - Podrán editar sus datos, cambiar su contraseña, ver sus libros reservados y su historial de compras.

2. **Búsqueda y filtrado de libros**:
   - Los usuarios podrán buscar libros por título, autor, género, entre otros filtros disponibles.

3. **Reserva de libros físicos y digitales**:
    - Los usuarios podrán reservar un máximo de 6 libros en total, combinando libros físicos y digitales.
    - De los libros reservados:
      - Físicos: Los libros deberán ser devueltos en un plazo de 30 días. Si no se devuelven a tiempo, se aplicará una sanción, ya que previamente se les solicitará una fianza.
      - Digitales: Los usuarios podrán reservar libros digitales, los cuales estarán disponibles durante un máximo de 25 días. Una vez pasado este plazo, el acceso será revocado automáticamente.
    - El sistema registrará todas las reservas y bloqueará los libros que no estén disponibles, ya sea en formato físico o digital.

4. **Compra de libros (físicos y digitales)**:
   - Los usuarios podrán añadir libros a una cesta de compra.
   - El sistema permitirá pagos seguros y gestionará el envío de libros físicos.

5. **Lectura en línea de libros electrónicos (opcional)**:
   - Los usuarios podrán leer libros electrónicos a través de un visor integrado en la plataforma.

6. **Sistema de comentarios y valoraciones**:
   - Los usuarios podrán dejar comentarios y valoraciones sobre los libros que hayan leído o comprado.

7. **Gestión de catálogo de libros (para administradores)**:
   - Los administradores podrán añadir, editar y eliminar libros del catálogo.
   - Tendrán una sección donde podrán ver todas las compras que han realizado los usuarios.
   - El sistema gestionará las reservas y sanciones de los usuarios, asegurando el cumplimiento de las normas de préstamo.
   - Administrar las reseñas realizadas por los usuarios sobre los libros, incluyendo opciones para aprobar, editar o eliminar contenido inapropiado.

### Requisitos No Funcionales

1. **Escalabilidad**:
   - El sistema debe gestionar un número creciente de usuarios y libros sin afectar el rendimiento de la plataforma.

2. **Seguridad**:
   - Se debe garantizar la protección de los datos de los usuarios y asegurar la seguridad de las transacciones de compra.

3. **Disponibilidad**:
   - La plataforma debe estar operativa 24/7, permitiendo el acceso en cualquier momento.

4. **Compatibilidad**:
   - La plataforma debe adaptarse a diferentes dispositivos y navegadores.

5. **Facilidad de uso**:
   - La interfaz debe ser intuitiva, permitiendo que usuarios no técnicos puedan utilizarla sin problemas.

### Requisitos de Interfaz

1. **Interfaz de búsqueda de libros**:
   - Debe incluir un campo de búsqueda con opciones de filtrado por autor, género y título.
   - Los resultados se mostrarán de forma clara, con miniaturas de las portadas y botones de "Reservar" o "Comprar".

2. **Panel de usuario**:
   - Los usuarios podrán ver su historial de reservas y compras, además de gestionar sus datos personales.
   - El diseño debe ser organizado y mostrar las fechas de vencimiento de las reservas.

3. **Cesta de compra**:
   - Debe ser accesible desde cualquier parte de la plataforma, mostrando un resumen de los libros seleccionados, sus precios y un botón para proceder al pago.

4. **Panel de administración**:
   - Para los administradores, debe haber un panel sencillo con opciones de gestión de libros, reservas, reseñas y compras, organizado en secciones claras.

## Casos de Uso Más Importantes

A continuación, se describen algunos de los casos de uso más relevantes para el sistema **BookVerse**.

### Caso de Uso 1: Búsqueda y Consulta de Libros

**Descripción**:  
Un usuario busca un libro en la plataforma utilizando la barra de búsqueda. El sistema permite filtrar los resultados por diferentes criterios como autor, título y género. El usuario revisa la lista de resultados y selecciona un libro para ver los detalles.

**Precondiciones**:  
El usuario está registrado o no registrado, pero tiene acceso a la interfaz de búsqueda.

**Flujo Principal**:
1. El usuario introduce palabras clave en el campo de búsqueda.
2. El sistema muestra los resultados relevantes.
3. El usuario aplica filtros adicionales si lo desea.
4. El usuario selecciona un libro de la lista para ver detalles como sinopsis, precio o disponibilidad de reserva.

**Postcondiciones**:  
El usuario ha visualizado los detalles del libro.

---

### Caso de Uso 2: Reserva de Libro Físico

**Descripción**:  
Un usuario registrado selecciona un libro físico disponible para su reserva. El sistema verifica que el usuario no haya alcanzado el límite de 4 libros reservados y, si es válido, realiza la reserva.

**Precondiciones**:
- El usuario está autenticado.
- El libro está disponible para reserva.

**Flujo Principal**:
1. El usuario selecciona el libro deseado.
2. El sistema verifica la disponibilidad del libro.
3. El sistema comprueba que el usuario no haya alcanzado el límite de 4 reservas.
4. El sistema confirma la reserva y actualiza el estado del libro a "Reservado".

**Postcondiciones**:  
El usuario ha reservado el libro y recibe la confirmación.

---

### Caso de Uso 3: Compra de Libro Digital

**Descripción**:  
Un usuario registrado decide comprar un libro digital. Le da al botón de comprar, procede al pago, y el sistema valida la transacción antes de aceptar la compra.

**Precondiciones**:
- El usuario está autenticado.
- El libro está disponible para su compra.

**Flujo Principal**:
1. El usuario selecciona un libro digital y le da al botón de comprar.
2. El usuario procede al pago.
3. El sistema valida el pago a través de la pasarela de pago.
4. El sistema permite la compra y el libro es enviado por correo electrónico.

**Postcondiciones**:  
El usuario ha realizado la compra y el libro se le enviará por correo electrónico.

### Modelo Relacional
![ER-BookVerse drawio](https://github.com/user-attachments/assets/a44af7ec-74cc-42a8-9177-5cdd14cf7775)



