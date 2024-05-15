<?php 

session_start();

	include("connection.php");
	include("functions.php");


	if($_SERVER['REQUEST_METHOD'] == "POST")
	{
		//something was posted
		$user_name = $_POST['user_name'];
		$pass = $_POST['password'];

		if(!empty($user_name) && !empty($pass) && !is_numeric($user_name))
		{

			//read from database
			$query = "select * from clogin where user_name = '$user_name' limit 1";
			$result = mysqli_query($con, $query);

			if($result)
			{
				if($result && mysqli_num_rows($result) > 0)
				{

					$user_data = mysqli_fetch_assoc($result);
					
					if($user_data['pass'] === $pass)
					{

						$_SESSION['customer_id'] = $user_data['customer_id'];
						header("Location: customer_test.php");
						die;
					}
				}
			}
			
			echo "wrong username or password!";
		}else
		{
			echo "wrong username or password!";
		}
	}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CustomerLogin</title>
    <link rel="stylesheet" href="loginCstyles.css">
</head>
<body>

    <div class="loginbox">

        <img src="image/customerAvatar.png" class="avatar">
         <h1>CUSTOMER LOGIN HERE</h1>

         <form method="POST">
             <p>Username</p>
             <input type="text" name="user_name" placeholder="Enter Username" required>
             <p>Password</p>
             <input type="password" name="password" placeholder="Enter Password" required>
             <input type="submit" name="" value="Login"></a>
             <p></p>
         </form>

    </div>
</body>
</html>