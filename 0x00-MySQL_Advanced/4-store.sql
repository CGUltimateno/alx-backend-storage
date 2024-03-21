-- Write a SQL script that creates a trigger that
-- decreases the quantity of an item
-- after adding a new order.
DELIMITER $$

CREATE TRIGGER update_quantity
AFTER INSERT
ON orders FOR EACH ROW
BEGIN
    DECLARE item varchar(255);
    DECLARE quantity int;
        SET item = NEW.item_name;
        SET quantity = NEW.number;
        UPDATE items
        SET quantity = quantity - qty
        WHERE name = item;
END;
$$

DELIMITER ;