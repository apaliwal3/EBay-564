SELECT COUNT(DISTINCT u.UserID) AS num_users
FROM User u 
JOIN Item i ON u.UserID = i.SellerID 
WHERE u.Rating > 1000;