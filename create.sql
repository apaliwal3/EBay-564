DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Item_Category;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS User;

CREATE TABLE User (
    UserID TEXT PRIMARY KEY,
    Rating INTEGER,
    Location TEXT,
    Country TEXT
);

CREATE TABLE Category (
    CategoryName TEXT PRIMARY KEY
);

CREATE TABLE Item (
    ItemID INTEGER PRIMARY KEY,
    Name TEXT,
    Currently REAL,
    Buy_Price REAL,
    First_Bid REAL,
    Number_of_Bids INTEGER,
    Location TEXT,
    Country TEXT,
    Started DATETIME,
    Ends DATETIME,
    Description TEXT,
    SellerID TEXT,
    FOREIGN KEY (SellerID) REFERENCES User(UserID)
);

CREATE TABLE Item_Category (
    ItemID INTEGER,
    CategoryName TEXT,
    PRIMARY KEY (ItemID, CategoryName),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (CategoryName) REFERENCES Category(CategoryName)
);

CREATE TABLE Bid (
    ItemID INTEGER,
    BidderID TEXT,
    Time DATETIME,
    Amount REAL,
    PRIMARY KEY (ItemID, BidderID, Time),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (BidderID) REFERENCES User(UserID)
);