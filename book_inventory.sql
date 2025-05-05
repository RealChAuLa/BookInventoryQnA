-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 05, 2025 at 12:02 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `book_inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `authors`
--

CREATE TABLE `authors` (
  `author_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `bio` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `authors`
--

INSERT INTO `authors` (`author_id`, `name`, `bio`) VALUES
(1, 'J.K. Rowling', 'British author, best known for the Harry Potter series.'),
(2, 'George Orwell', 'English novelist, essayist, journalist and critic.'),
(3, 'J.R.R. Tolkien', 'English writer, poet, philologist, and academic, best known for The Lord of the Rings.'),
(4, 'Agatha Christie', 'English writer known for her sixty-six detective novels and fourteen short story collections.'),
(5, 'Harper Lee', 'Author of the classic novel To Kill a Mockingbird.');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `book_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author_id` int(11) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`book_id`, `title`, `author_id`, `genre`, `price`, `stock_quantity`) VALUES
(1, 'Harry Potter and the Sorcerer\'s Stone', 1, 'Fantasy', 19.99, 100),
(2, '1984', 2, 'Dystopian', 14.99, 200),
(3, 'The Hobbit', 3, 'Fantasy', 25.99, 150),
(4, 'Murder on the Orient Express', 4, 'Mystery', 12.99, 120),
(5, 'Harry Potter and the Chamber of Secrets', 1, 'Fantasy', 19.99, 90),
(6, 'Animal Farm', 2, 'Satire', 9.99, 180),
(7, 'The Lord of the Rings: The Fellowship of the Ring', 3, 'Fantasy', 29.99, 80),
(8, 'The Lord of the Rings: The Two Towers', 3, 'Fantasy', 29.99, 75),
(9, 'The Lord of the Rings: The Return of the King', 3, 'Fantasy', 29.99, 70),
(10, 'And Then There Were None', 4, 'Mystery', 15.99, 110),
(11, 'To Kill a Mockingbird', 1, 'Fiction', 15.99, 10);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `order_date` date NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `book_id`, `order_date`, `quantity`, `total_amount`) VALUES
(1, 1, '2024-11-01', 2, 39.98),
(2, 2, '2024-11-02', 5, 74.95),
(3, 3, '2024-11-03', 3, 77.97),
(4, 4, '2024-11-04', 4, 51.96),
(5, 5, '2024-11-05', 1, 19.99),
(6, 6, '2024-11-06', 7, 69.93),
(7, 7, '2024-11-07', 2, 59.98),
(8, 8, '2024-11-08', 3, 89.97),
(9, 9, '2024-11-09', 1, 29.99),
(10, 10, '2024-11-10', 4, 63.96),
(11, 11, '2024-11-22', 1, 15.99);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authors`
--
ALTER TABLE `authors`
  ADD PRIMARY KEY (`author_id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`book_id`),
  ADD KEY `author_id` (`author_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `book_id` (`book_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `authors`
--
ALTER TABLE `authors`
  MODIFY `author_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`author_id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
