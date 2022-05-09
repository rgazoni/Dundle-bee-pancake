
USE Storage;



DELIMITER ;;
CREATE OR REPLACE PROCEDURE `move_gondula`(IN _ID_PROD INT,
								IN _Quantidade INT,
                                OUT resultado INT)
BEGIN
IF (EXISTS (SELECT * FROM estoque 
		    INNER JOIN produto
            ON fk_Produto_ID_PROD = ID_PROD
		    WHERE ID_PROD = _ID_PROD))
	THEN
    BEGIN
		SET @quantidade_estoque = (SELECT Quantidade
								  FROM estoque
                                  WHERE fk_Produto_ID_PROD = _ID_PROD);
		IF (@quantidade_estoque > _Quantidade OR @quantidade_estoque = _Quantidade)
        THEN
        BEGIN
			IF (NOT EXISTS (SELECT * FROM gondula 
							WHERE fk_Produto_ID_PROD = _ID_PROD))
			THEN
            BEGIN
				INSERT INTO gondula (Quantidade, fk_Produto_ID_PROD)
				VALUES ( 0, _ID_PROD);
            END;
            END IF;
            SET @quantidade_gondula = (SELECT Quantidade
								  FROM gondula
                                  WHERE fk_Produto_ID_PROD = _ID_PROD);
            UPDATE gondula 
            SET Quantidade = @quantidade_gondula+_Quantidade
            WHERE fk_Produto_ID_PROD = _ID_PROD;
            UPDATE estoque 
            SET Quantidade = @quantidade_estoque - _Quantidade
            WHERE fk_Produto_ID_PROD = _ID_PROD;
            SET resultado = 1;
        END;
        ELSE 
        BEGIN
			SET resultado = 0;
        END;
        END IF;
    END;
    END IF;
END ;;
DELIMITER ;

DELIMITER ;;
CREATE OR REPLACE PROCEDURE `recebe_produto`(IN _ID_PROD INT,
								   IN _ID_CATEGORIA INT,
                                   IN _Quantidade INT,
                                   IN _Data_fabricacao DATE,
                                   IN _Data_vencimento DATE,
                                   IN _lote INT,
                                   IN _origem VARCHAR(50), 
                                   OUT result int)
BEGIN
IF EXISTS (SELECT * FROM categorias 
		  WHERE ID_CATEGORIA = _ID_CATEGORIA)
THEN 
	IF 
		NOT EXISTS (SELECT * FROM produto 
					  INNER JOIN categorias 
					  ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA 
					  WHERE ID_PROD = _ID_PROD AND
                        Data_fabricacao = _Data_fabricacao AND
                        Data_vencimento = _Data_vencimento AND
                        lote = _lote AND
                        origem = _origem)
					  
		THEN 
			BEGIN
            SET @ID_AUX = (SELECT max(ID_PROD)+1 FROM produto);
			INSERT INTO produto (ID_PROD, fk_Categorias_ID_CATEGORIA, Quantidade,
								Data_fabricacao, Data_vencimento, lote, origem)
			VALUES (@ID_AUX, _ID_CATEGORIA, _Quantidade,
					_Data_fabricacao, _Data_vencimento, _lote, _origem);
			INSERT INTO estoque (Quantidade, fk_Produto_ID_PROD)
			VALUES ( _Quantidade, @ID_AUX);
			set result := 1;
			END;
	ELSE 
		BEGIN
			SET @quantidade_prod = (SELECT Quantidade FROM produto WHERE ID_PROD = _ID_PROD);
			UPDATE produto 
            SET Quantidade = @quantidade_prod +_Quantidade
			WHERE ID_PROD = _ID_PROD;
            SET @quantidade_estoque = (SELECT Quantidade FROM estoque WHERE fk_Produto_ID_PROD = _ID_PROD);
            UPDATE estoque 
            SET Quantidade =@quantidade_estoque+_Quantidade
			WHERE fk_Produto_ID_PROD = _ID_PROD;
            set result := 1;
		END;
	END IF;
    ELSE  
    BEGIN
		set result := 0;
    END;
END IF;
END ;;
DELIMITER ;

DELIMITER ;;
CREATE OR REPLACE PROCEDURE `saida_caixa`(IN _ID_PROD INT,
								IN _Quantidade INT,
                                OUT resultado INT)
BEGIN
IF (EXISTS (SELECT * FROM gondula 
		    INNER JOIN produto
            ON fk_Produto_ID_PROD = ID_PROD
		    WHERE ID_PROD = _ID_PROD))
	THEN
    BEGIN
		SET @quantidade_gondula = (SELECT Quantidade
								  FROM gondula
                                  WHERE fk_Produto_ID_PROD = _ID_PROD);
        SET @quantidade_produto = (SELECT Quantidade
								  FROM produto
                                  WHERE ID_PROD = _ID_PROD);                          
		IF (@quantidade_gondula > _Quantidade OR @quantidade_gondula = _Quantidade)
        THEN
        BEGIN
            UPDATE gondula 
            SET Quantidade = @quantidade_gondula-_Quantidade
            WHERE fk_Produto_ID_PROD = _ID_PROD;
            UPDATE produto 
            SET Quantidade = @quantidade_produto-_Quantidade
            WHERE ID_PROD = _ID_PROD;
            SET resultado = 1;
        END;
        ELSE 
        BEGIN
			SET resultado = 0;
        END;
        END IF;
    END;
    ELSE
    BEGIN
		SET resultado = 0;
    END;
    END IF;
END ;;
DELIMITER ;