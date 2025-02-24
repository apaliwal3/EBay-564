SELECT COUNT(DISTINCT IC.CategoryName) AS NumCategories
FROM Item_Category IC
JOIN Bid B ON IC.ItemID = B.ItemID
WHERE B.Amount > 100;