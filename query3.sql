SELECT COUNT(*) AS num_auctions_with_four_categories
FROM (
    SELECT ItemID
    FROM Item_Category
    GROUP BY ItemID
    HAVING COUNT(CategoryName) = 4
) AS four_category_items;