CREATE DATABASE IF NOT EXISTS omnipotente;
USE omnipotente;

CREATE TABLE zonas(
	cod_pstl varchar(6) NOT NULL PRIMARY KEY ,
    estado varchar(30),
    colonia varchar(30),
    densidad_poblacion DECIMAL(10,2),
    indice_marginacion DECIMAL(5,2)
);

CREATE TABLE seccion(
	id_seccion int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    coord_inicio_x DECIMAL(10,7) NOT NULL,  -- Longitud
    coord_inicio_y DECIMAL(10,7) NOT NULL,  -- Latitud
    coord_fin_x DECIMAL(10,7) NOT NULL,
    coord_fin_y DECIMAL(10,7) NOT NULL,
    cod_pstl varchar(6),
    nombre_calle varchar(30),
    FOREIGN KEY (cod_pstl) REFERENCES zonas(cod_pstl)
);

CREATE TABLE reportes(
	id_reporte int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_seccion int,
    fecha datetime,
    tipo ENUM('Asalto','Secuestro','Extorsion','riña','Fuga de agua','falta de alumbrado') NOT NULL, -- podria crecer a más
    reporte text,
    FOREIGN KEY (id_seccion) REFERENCES seccion(id_seccion)
);


-- drop database omnipotente;
-- drop table reportes;
select id_seccion as id , tipo , count(tipo) as reportes from reportes  group by id_seccion,tipo having reportes >= 3;

SELECT 
  sec.id_seccion, 
  sec.coord_inicio_x, 
  sec.coord_inicio_y, 
  sec.coord_fin_x, 
  sec.coord_fin_y, 
  sec.nombre_calle, 
  COUNT(rep.tipo) AS reportes
FROM seccion AS sec
LEFT JOIN reportes AS rep
  ON sec.id_seccion = rep.id_seccion
  AND (rep.tipo = 'Extorsion' or rep.tipo = 'Secuestro' )
GROUP BY sec.id_seccion
HAVING reportes > 3;

 -- #cursor.execute("SELECT sec.id_seccion, sec.coord_inicio_x, sec.coord_inicio_y, sec.coord_fin_x, sec.coord_fin_y, sec.nombre_calle, rep.tipo, COUNT(rep.tipo) AS reportes FROM seccion AS sec LEFT JOIN reportes AS rep ON sec.id_seccion = rep.id_seccion GROUP BY sec.id_seccion, rep.tipo;")
