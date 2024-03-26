-- Write a SQL script that creates a trigger that
-- decreases the quantity of an item
-- after adding a new order.
DELIMITER $$

CREATE TRIGGER trgAddNewOrder
AFTER INSERT
ON orders FOR EACH ROW
BEGIN
	DECLARE item VARCHAR(255);
	DECLARE qty INT;

	SET item = NEW.item_name;
	SET qty = NEW.number;

	UPDATE items
	SET quantity = quantity - qty
	WHERE name = item;
END;
$$

DELIMITER ;