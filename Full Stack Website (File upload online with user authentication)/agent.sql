-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 16, 2022 at 05:40 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `agent`
--

-- --------------------------------------------------------

--
-- Table structure for table `alogin`
--

CREATE TABLE `alogin` (
  `id` bigint(20) NOT NULL,
  `agent_id` bigint(20) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pass` varchar(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alogin`
--

INSERT INTO `alogin` (`id`, `agent_id`, `user_name`, `email`, `pass`, `date`) VALUES
(6, 375742775695329021, 'agent', 'agent@gmail.com', '123456789', '2021-12-09 12:25:26');

-- --------------------------------------------------------

--
-- Table structure for table `clogin`
--

CREATE TABLE `clogin` (
  `id` bigint(20) NOT NULL,
  `customer_id` bigint(20) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `pass` varchar(50) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clogin`
--

INSERT INTO `clogin` (`id`, `customer_id`, `user_name`, `email`, `pass`, `date`) VALUES
(5, 4443944, 'customer', 'customer@gmail.com', '12345', '2021-12-09 12:18:44'),
(6, 369588346997, 'customer', 'customer@gmail.com', '12345', '2021-12-09 12:22:45');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles1`
--

CREATE TABLE `vehicles1` (
  `username` varchar(20) NOT NULL,
  `carbrand` varchar(20) NOT NULL,
  `carmodel` varchar(50) NOT NULL,
  `purchasedate` date NOT NULL,
  `enginetype` varchar(50) NOT NULL,
  `RCcopy` text NOT NULL,
  `DL` text NOT NULL,
  `PPC` text NOT NULL,
  `NCB` text NOT NULL,
  `claimedpolicy` text NOT NULL,
  `lapsedpolicy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vehicles1`
--

INSERT INTO `vehicles1` (`username`, `carbrand`, `carmodel`, `purchasedate`, `enginetype`, `RCcopy`, `DL`, `PPC`, `NCB`, `claimedpolicy`, `lapsedpolicy`) VALUES
('customer', '123456abc', 'mdncvt6345', '2021-12-13', 'model 5678gb', 'Screenshot 2021-12-08 at 8.45.50 PM.png', 'Screenshot 2021-12-08 at 8.45.50 PM.png', 'Screenshot 2021-12-08 at 8.45.50 PM.png', 'Screenshot 2021-12-08 at 8.45.50 PM.png', 'Screenshot 2021-12-08 at 8.45.50 PM.png', 'Screenshot 2021-12-08 at 8.45.50 PM.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alogin`
--
ALTER TABLE `alogin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`user_name`),
  ADD KEY `agent_id` (`agent_id`),
  ADD KEY `date` (`date`);

--
-- Indexes for table `clogin`
--
ALTER TABLE `clogin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `user_name` (`user_name`),
  ADD KEY `date` (`date`);

--
-- Indexes for table `vehicles1`
--
ALTER TABLE `vehicles1`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alogin`
--
ALTER TABLE `alogin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `clogin`
--
ALTER TABLE `clogin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
