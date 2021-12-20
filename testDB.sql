PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE PRODUCT(
   id         INTEGER PRIMARY KEY  AUTOINCREMENT,
   item	      TEXT    NOT NULL,
   price      INT     NOT NULL,
   quantity    INT    NOT NULL
);
INSERT INTO PRODUCT VALUES(1,'aaa',20,98);
INSERT INTO PRODUCT VALUES(2,'bbb',30,95);
INSERT INTO PRODUCT VALUES(3,'ccc',25,96);
INSERT INTO PRODUCT VALUES(4,'ddd',45,95);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('PRODUCT',4);
COMMIT;
