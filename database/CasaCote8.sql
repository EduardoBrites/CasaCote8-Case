-- Gerado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   em:        2025-10-03 16:39:15 BRT
--   site:      Oracle Database 11g
--   tipo:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE CLIENTE 
    ( 
     ID_CLI      NUMBER (6)  NOT NULL , 
     NOME_CLI    VARCHAR2 (150) , 
     TEL_CLI     NUMBER (13) , 
     CPFCNPJ_CLI NUMBER (14) , 
     EMAIL_CLI   VARCHAR2 (150) 
    ) 
;

ALTER TABLE CLIENTE 
    ADD CONSTRAINT CLIENTE_PK PRIMARY KEY ( ID_CLI ) ;

CREATE TABLE FORNECEDOR 
    ( 
     ID_FORNEC      NUMBER (6)  NOT NULL , 
     CPFCNPJ_FORNEC NUMBER (14) , 
     TEL_FORNEC     NUMBER (13) , 
     NOME_FORNEC    VARCHAR2 (70) , 
     EMAIL_FORNEC   VARCHAR2 (150) 
    ) 
;

ALTER TABLE FORNECEDOR 
    ADD CONSTRAINT FORNECEDOR_PK PRIMARY KEY ( ID_FORNEC ) ;

CREATE TABLE PRODUTO 
    ( 
     ID_PRODUTO           NUMBER (6)  NOT NULL , 
     NOME_PRODUTO         VARCHAR2 (150) , 
     COR_PRODUTO          VARCHAR2 (15) , 
     COLECAO_PRODUTO      VARCHAR2 (50) , 
     BORDADO_PRODUTO      CHAR (1) , 
     CORLINHA_PRODUTO     VARCHAR2 (15) , 
     OBSERVACAO_PRODUTO   VARCHAR2 (300) , 
     PRECOUNI_PRODUTO     NUMBER (8,2) , 
     FORNECEDOR_ID_FORNEC NUMBER (6)  NOT NULL 
    ) 
;

ALTER TABLE PRODUTO 
    ADD CONSTRAINT PRODUTO_PK PRIMARY KEY ( ID_PRODUTO, FORNECEDOR_ID_FORNEC ) ;

CREATE TABLE PROJETO 
    ( 
     ID_PROJ        NUMBER (6)  NOT NULL , 
     PRAZO_PROJ     DATE , 
     CLIENTE_ID_CLI NUMBER (6)  NOT NULL 
    ) 
;

ALTER TABLE PROJETO 
    ADD CONSTRAINT PROJETO_PK PRIMARY KEY ( ID_PROJ ) ;

CREATE TABLE PROJETO_PRODUTO 
    ( 
     PROJETO_ID_PROJ              NUMBER (6)  NOT NULL , 
     PRODUTO_ID_PRODUTO           NUMBER (6)  NOT NULL , 
     PRODUTO_FORNECEDOR_ID_FORNEC NUMBER (6)  NOT NULL , 
     QUANTIDADE_PRODUTO           NUMBER (7) 
    ) 
;

ALTER TABLE PROJETO_PRODUTO 
    ADD CONSTRAINT PedidoProduto_PK PRIMARY KEY ( PROJETO_ID_PROJ, PRODUTO_ID_PRODUTO, PRODUTO_FORNECEDOR_ID_FORNEC ) ;

ALTER TABLE PRODUTO 
    ADD CONSTRAINT PRODUTO_FORNECEDOR_FK FOREIGN KEY 
    ( 
     FORNECEDOR_ID_FORNEC
    ) 
    REFERENCES FORNECEDOR 
    ( 
     ID_FORNEC
    ) 
;

ALTER TABLE PROJETO 
    ADD CONSTRAINT PROJETO_CLIENTE_FK FOREIGN KEY 
    ( 
     CLIENTE_ID_CLI
    ) 
    REFERENCES CLIENTE 
    ( 
     ID_CLI
    ) 
;

ALTER TABLE PROJETO_PRODUTO 
    ADD CONSTRAINT PROJETO_PRODUTO_PRODUTO_FK FOREIGN KEY 
    ( 
     PRODUTO_ID_PRODUTO,
     PRODUTO_FORNECEDOR_ID_FORNEC
    ) 
    REFERENCES PRODUTO 
    ( 
     ID_PRODUTO,
     FORNECEDOR_ID_FORNEC
    ) 
;

ALTER TABLE PROJETO_PRODUTO 
    ADD CONSTRAINT PROJETO_PRODUTO_PROJETO_FK FOREIGN KEY 
    ( 
     PROJETO_ID_PROJ
    ) 
    REFERENCES PROJETO 
    ( 
     ID_PROJ
    ) 
;



-- Relatório do Resumo do Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                             5
-- CREATE INDEX                             0
-- ALTER TABLE                              9
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
