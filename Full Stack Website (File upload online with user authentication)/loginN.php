<?php 
session_start();

	include("connection.php");
	include("functions.php");


	if($_SERVER['REQUEST_METHOD'] == "POST")
	{
		//something was posted
		$user_name = $_POST['customer_name'];
		$email=$_POST['EmailID'];
		$password = $_POST['passC'];

		if(!empty($user_name) && !empty($password) && !empty($email) && !is_numeric($user_name))
		{

			//save to database
			$customer_id = random_num(20);
			$query = "insert into clogin (customer_id,user_name,email,pass) values ('$customer_id','$user_name','$email','$password')";

			mysqli_query($con, $query);

			header("Location: loginC.php");
			die;
		}else
		{
			echo "Please enter some valid information!";
		}
	}

	if($_SERVER['REQUEST_METHOD'] == "POST")
	{
		//something was posted
		$user_name = $_POST['agent_name'];
		$email=$_POST['emailID'];
		$password = $_POST['passA'];

		if(!empty($user_name) && !empty($password) && !empty($email) && !is_numeric($user_name))
		{

			//save to database
			$agent_id = random_num(20);
			$query = "insert into alogin (agent_id,user_name,email,pass) values ('$agent_id','$user_name','$email','$password')";

			mysqli_query($con, $query);

			header("Location: loginA.php");
			die;
		}else
		{
			echo "Please enter some valid information!";
		}
	}
?>


<!DOCTYPE html>
<html>
<head>
	<title>Signup</title>
</head>
<body>
	<h1></h>
	<style type="text/css">
	.h1{
 background-color: white;
 padding-top: 50px;
 padding-bottom:50px;
 text-align: center;
 color: black;
 margin-bottom: 250px;
}

	#text{

		height: 25px;
		border-radius: 5px;
		padding: 4px;
		border: solid thin #aaa;
		width: 100%;
	}

	#button{

		padding: 10px;
		width: 100px;
		color: white;
		background-color: lightblue;
		border: none;
	}
	#login{
    display: flex;
    justify-content: space-between;
    padding: 38px;}

	#box{

		background-color: rgba(238, 140, 11, 0.897);
		margin: auto;
		width: 250px;
		padding: 50px;
		text-align:center;
		float: left;
	}
	#box1{
		background-color: rgba(238, 140, 11, 0.897);
		margin: auto;
		width: 250px;
		padding: 50px;
		text-align:center;
		float: left;
	}
	body{ 
    background-image: url("image/customer.jpg"); 
    background-size: cover;
    background-position: center;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 18px;
    margin: 0;
}
.submit-btn {
    width: 85%;
    padding: 5px 5px;
    cursor: pointer;
    display: block;
    margin: auto;
    background: linear-gradient(to right, #ff105f,#ffad06);
    border: 0;
    outline: none;
    border-radius: 30px;
}

	</style>

	<div id=login>

	<div id="box">
		
		
		<form id="CreateCustomer" class="input-group" method="POST">
                <input type="text" class="input-field" name="customer_name" placeholder="Customer Name" required>
                <input type="email" class="input-field" name="EmailID" placeholder="Email Id" required>
                <input type="text" class="input-field" name="passC" placeholder="Enter Password" required>
                <a href="customer.php"> <button type="submit" class="submit-btn" name="submit">Create Customer Account</button> </a>
            </form>
        </div>
		<div id="box1">
            <form id="CreateAgent" class="input-group" method="POST">
                <input type="text" class="input-field" name="agent_name" placeholder="Agent username" required>
                <input type="email" class="input-field" name="emailID" placeholder="Email Id" required>
                <input type="text" class="input-field" name="passA" placeholder="Enter Password" required>
                <a href="agent.php"> <button type="submit" class="submit-btn" name="submit">Create Agent Account</button> </a>
            </form>
        </div>
</div>
</body>
</html>