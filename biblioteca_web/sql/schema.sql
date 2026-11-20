-- Tabela `Usuario`
-- Armazena os dados dos usuários da biblioteca.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Usuario` (
  `CPF` VARCHAR(11) NOT NULL,
  `nome` VARCHAR(255) NOT NULL,
  `telefone` VARCHAR(20) NULL,
  `email` VARCHAR(255) NOT NULL,
  `limite_emprestimo` INT NOT NULL DEFAULT 5,
  `senha` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`CPF`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabela `Funcionario`
-- Armazena os dados dos funcionários.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Funcionario` (
  `ID_funcionario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `cargo` VARCHAR(100) NOT NULL,
  `telefone` VARCHAR(20) NULL,
  `email` VARCHAR(255) NOT NULL,
  `CPF` VARCHAR(11) NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`ID_funcionario`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
  UNIQUE INDEX `CPF_UNIQUE` (`CPF` ASC)
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabela `Item_acervo`
-- Catálogo de todos os itens da biblioteca.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Item_acervo` (
  `ID_item` INT NOT NULL AUTO_INCREMENT,
  `titulo` VARCHAR(255) NOT NULL,
  `autor` VARCHAR(255) NULL,
  `ano` YEAR NULL,
  `tipo_item` VARCHAR(50) NOT NULL,
  `status_item` VARCHAR(50) NOT NULL DEFAULT 'Disponível',
  `ID_funcionario` INT NOT NULL,
  PRIMARY KEY (`ID_item`),
  INDEX `fk_Item_acervo_Funcionario_idx` (`ID_funcionario` ASC),
  CONSTRAINT `fk_Item_acervo_Funcionario`
    FOREIGN KEY (`ID_funcionario`)
    REFERENCES `Funcionario` (`ID_funcionario`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabela `Emprestimo`
-- Registra cada transação de empréstimo.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Emprestimo` (
  `ID_emprestimo` INT NOT NULL AUTO_INCREMENT,
  `data_emprest` DATE NOT NULL,
  `data_dev` DATE NOT NULL,
  `data_dev_real` DATE NULL,
  `status` VARCHAR(50) NOT NULL,
  `multa` DECIMAL(10,2) NULL DEFAULT 0.00,
  `ID_funcionario` INT NOT NULL,
  `CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`ID_emprestimo`),
  INDEX `fk_Emprestimo_Funcionario_idx` (`ID_funcionario` ASC),
  INDEX `fk_Emprestimo_Usuario_idx` (`CPF` ASC),
  CONSTRAINT `fk_Emprestimo_Funcionario`
    FOREIGN KEY (`ID_funcionario`)
    REFERENCES `Funcionario` (`ID_funcionario`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Emprestimo_Usuario`
    FOREIGN KEY (`CPF`)
    REFERENCES `Usuario` (`CPF`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabela `Reserva`
-- Armazena as reservas de itens feitas pelos usuários.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Reserva` (
  `ID_reserva` INT NOT NULL AUTO_INCREMENT,
  `data_reserva` DATE NOT NULL,
  `status_reserva` VARCHAR(50) NOT NULL,
  `data_limite_retirada` DATE NULL,
  `CPF` VARCHAR(11) NOT NULL,
  `ID_item` INT NOT NULL,
  PRIMARY KEY (`ID_reserva`),
  INDEX `fk_Reserva_Usuario_idx` (`CPF` ASC),
  INDEX `fk_Reserva_Item_acervo_idx` (`ID_item` ASC),
  CONSTRAINT `fk_Reserva_Usuario`
    FOREIGN KEY (`CPF`)
    REFERENCES `Usuario` (`CPF`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Reserva_Item_acervo`
    FOREIGN KEY (`ID_item`)
    REFERENCES `Item_acervo` (`ID_item`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;


-- -----------------------------------------------------
-- Tabela `Movimentacao`
-- Tabela associativa que liga os itens a um empréstimo.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Movimentacao` (
  `ID_emprestimo` INT NOT NULL,
  `ID_item` INT NOT NULL,
  `tipo` VARCHAR(50) NULL,
  `data_movimentacao` DATE NOT NULL,
  PRIMARY KEY (`ID_emprestimo`, `ID_item`),
  INDEX `fk_Movimentacao_Item_acervo_idx` (`ID_item` ASC),
  CONSTRAINT `fk_Movimentacao_Emprestimo`
    FOREIGN KEY (`ID_emprestimo`)
    REFERENCES `Emprestimo` (`ID_emprestimo`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Movimentacao_Item_acervo`
    FOREIGN KEY (`ID_item`)
    REFERENCES `Item_acervo` (`ID_item`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;