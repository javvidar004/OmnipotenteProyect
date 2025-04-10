CREATE DATABASE IF NOT EXISTS omnipotente;
USE omnipotente;

CREATE TABLE zonas(
	cod_pstl varchar(6) NOT NULL PRIMARY KEY ,
    estado varchar(30),
    colonia varchar(30),
    densidad_poblacion DECIMAL(10,2),
    indice_marginacion DECIMAL(5,2)
);

CREATE TABLE calles(
    id_calle int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cod_pstl varchar(6),
    nombre varchar(30),
    FOREIGN KEY (cod_pstl) REFERENCES zonas(cod_pstl)
);

CREATE TABLE seccion(
	id_seccion int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_calle int,
    coord_inicio_x DECIMAL(10,7) NOT NULL, -- Longitud
    coord_inicio_y DECIMAL(10,7) NOT NULL, -- Latitud
    coord_fin_x DECIMAL(10,7) NOT NULL,
    coord_fin_y DECIMAL(10,7) NOT NULL,
    FOREIGN KEY (id_calle) REFERENCES calles(id_calle)
);

CREATE TABLE usuarios (
    id_usuario int NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    cod_pstl varchar(6) NOT NULL,
    FOREIGN KEY (cod_pstl) REFERENCES zonas(cod_pstl)
);


CREATE TABLE reportes(
	id_reporte int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario int,
    id_seccion int,
    fecha date,
    coord_x varchar(15),
    coord_y varchar(15),
    tipo ENUM('Asalto','Fuga de agua','falta de alumbrado') NOT NULL, -- podria crecer a más
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_seccion) REFERENCES seccion(id_seccion)
);


#drop database omnipotente;

