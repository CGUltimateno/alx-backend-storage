-- Write a SQL script that creates a trigger that
-- decreases the quantity of an item
-- after adding a new order.
CREATE TRIGGER update_quantity
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    DECLARE item varchar(255);
    DECLARE quantity int;
        SET item = NEW.item;
        SET qty = NEW.quantity;
        UPDATE items
        SET quantity = quantity - qty
        WHERE name = item;
END;
