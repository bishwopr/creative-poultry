

--adding given warehouse table
UPDATE warehouse (warehouse_id, email, phone_number, capacity_space, occupied_space, no_of_loading_bays, no_of_doors, extra_description, postcode) VALUES
(1, 'LavertonNorth@info.com', 1234890, 5000, 2000, 4, 2, 'Extra space available on the mezzanine level', 3000),
(2, 'Campbelltown@atyd.com', 23456781, 8000, 6000, 6, 4, 'Has a dedicated area for temperature-controlled storage', 2000),
(3, 'loganpark@atyd.com', 3456012, 10000, 8000, 10, 6, 'Ideal for storing large machinery and equipment', 4000);

-- Add the warehouse_name column to the warehouse table
ALTER TABLE warehouse ADD COLUMN warehouse_name VARCHAR(255);

-- Update the warehouse_name for each warehouse
UPDATE warehouse
SET warehouse_name = CASE
    WHEN warehouse_id = 1 THEN 'Laverton North'
    WHEN warehouse_id = 2 THEN 'Campbelltown'
    WHEN warehouse_id = 3 THEN 'Logan Park'
   
    ELSE 'Unknown'
    END;






#To add a geom_office POINT column of 3 dimensions:

ALTER TABLE warehouse ADD COLUMN geom_office GEOMETRY(PointZ, 4326);

#To add a geom_warehouse POLYGON column of 2 dimensions:

ALTER TABLE warehouse ADD COLUMN geom_warehouse GEOMETRY(Polygon, 4326);

#add a geom_weighbridge LINESTRING column of 2 dimensions:

ALTER TABLE warehouse ADD COLUMN geom_weighbridge GEOMETRY(LineString, 4326);


	--for Laverton North

#For geom_office column:

UPDATE warehouse SET geom_office = ST_SetSRID(ST_MakePoint(144.781744, -37.826901, 27) 4326)
WHERE warehouse_id = [id_of_Laverton_North_warehouse];

#For geom_weighbridge column:
UPDATE warehouse 
SET geom_weighbridge = ST_SetSRID(ST_GeomFromText('LINESTRING(144.749414 -37.825150, 144.749592 -37.825157)'), 4326)
WHERE warehouse_id = 1;


#For geom_warehouse column:

UPDATE warehouse SET geom_warehouse = ST_GeomFromText(('POLYGON((144.781116, -37.824855, 144.780843, -37.826916, 144.782018, -37.827019, 144.782320, -37.824960, 144.781116, -37.824855))', 4326));
    WHERE warehouse_id = 1;




--For Campbelltown

UPDATE warehouse 
SET geom_office = ST_SetSRID(ST_MakePoint(150.806228, -34.055744, 76), 4326)
WHERE warehouse_id = 2;

UPDATE warehouse 
SET geom_weighbridge = ST_SetSRID(ST_GeomFromText('LINESTRING(150.790276 -34.064902, 150.790578 -34.064934)'), 4326)
WHERE warehouse_id = 2;

UPDATE warehouse 
SET geom_warehouse = ST_SetSRID(ST_GeomFromText('POLYGON((150.804330 -34.055280, 150.804631 -34.055905, 150.804980 -34.055797, 150.805050 -34.055945, 150.805475 -34.055820, 150.805550 -34.056002, 150.806881 -34.055598, 150.806447 -34.054650, 150.804330 -34.055280))'), 4326)
WHERE warehouse_id = 2;



--For Logan Park



UPDATE warehouse SET geom_office = ST_SetSRID(ST_MakePoint(153.193537, -27.683932, 10), 4326),
WHERE warehouse_id = 3;


UPDATE warehouse SET geom_weighbridge = ST_SetSRID(ST_GeomFromText('LINESTRING(153.185471 -27.676645, 153.185533 -27.676771)'), 4326)
WHERE warehouse_id = 3;


UPDATE warehouse SET geom_warehouse = ST_SetSRID(ST_GeomFromText('POLYGON((153.193238 -27.682795, 153.193020 -27.683750, 153.193568 -27.683843, 153.193795 -27.682894, 153.193238 -27.682795))'), 4326)
    WHERE warehouse_id = 3;




--Show the name of each of the warehouses with their office and warehouse coordinates. Use theSt_AsText function to show the coordinates in a readable (longitude and latitude) format;

SELECT warehouse_name, ST_AsText(geom_office) AS office_coordinates, ST_AsText(geom_warehouse) AS warehouse_coordinates
FROM warehouse;

-- c. Show the name and the centre point (use the ST_asText and ST_Centroid functions for this) of each factory in degrees of longitude and latitude;

SELECT warehouse_name, ST_AsText(ST_Centroid(geom_warehouse)) AS center_point
FROM warehouse;

/*Show the name, area of each factory in metres squared (label this column “Areas(m2)”) and its
perimeter in metres (label this column as “Perimeter(metres)”) . You will need to transform
(ST_Transform) your SRID for Laverton North to 7855 and to 7856 for Campbelltown and Logan
Park;*/



SELECT warehouse_name,
       ST_Area(ST_Transform(geom_warehouse, CASE WHEN warehouse_id = 1 THEN 7855 WHEN warehouse_id = 2 THEN 7856 WHEN warehouse_id = 3 THEN 7856 END)) AS "Area(m²)",
       ST_Perimeter(ST_Transform(geom_warehouse, CASE WHEN warehouse_id = 1 THEN 7855 WHEN warehouse_id = 2 THEN 7856 WHEN warehouse_id = 3 THEN 7856 END)) AS "Perimeter(m)"
FROM warehouse
WHERE warehouse_id = 1 OR warehouse_id = 2 OR warehouse_id = 3;

/*e. Show the name of the warehouse, the length in metres of its accompanying weighbridge – label as
“Weighbridge length(metres)” - and the distance between the office and the weighbridge (in
metres) – label as “Distance from Office to Weighbridge”. Again, you will need to transform your
SRID for Laverton to 7855 and to 7856 for Campbelltown and Logan Park;*/

SELECT warehouse_name,
       ST_Length(ST_Transform(geom_weighbridge, CASE WHEN warehouse_id = 1 THEN 7855 WHEN warehouse_id = 2 THEN 7856 WHEN warehouse_id = 3 THEN 7856 END)) AS "Weighbridge length(m)",
       ST_Distance(ST_Transform(geom_office, CASE WHEN warehouse_id = 1 THEN 7855 WHEN warehouse_id = 2 THEN 7856 WHEN warehouse_id = 3 THEN 7856 END), ST_Transform(geom_weighbridge, CASE WHEN warehouse_id = 1 THEN 7855 WHEN warehouse_id = 2 THEN 7856 WHEN warehouse_id = 3 THEN 7856 END)) AS "Distance from Office to Weighbridge"
FROM warehouse
WHERE warehouse_id = 1 OR warehouse_id = 2 OR warehouse_id = 3;


 --ST_Within spatial relationship function   
SELECT w1.warehouse_name, ST_AsText(w1.geom_office) AS office_point
FROM warehouse w1
INNER JOIN warehouse w2 ON w1.warehouse_id = w2.warehouse_id
WHERE ST_Within(w1.geom_office, w2.geom_warehouse);

--  calculate the sphere distance and spheroid distance between the Campbelltown and Logan Park factory offices
SELECT
  ST_DistanceSphere(w1.geom_office, w2.geom_office) / 1000 AS sphere_distance_km,
  ST_DistanceSpheroid(w1.geom_office, w2.geom_office, 'SPHEROID["WGS 84",6378137,298.257223563]') / 1000 AS spheroid_distance_km
FROM warehouse w1
JOIN warehouse w2
  ON w1.warehouse_name = 'Campbelltown'
  AND w2.warehouse_name = 'Logan Park';
