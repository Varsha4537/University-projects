
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Dashboard</title>
    <link rel="stylesheet" href="customerstyles.css">
</head>
<body>
    <div class="container"></div>
    <div class="log">
        
        <div class="exit">
           
           <div class="home"> <a href="home.php">HOME</a> </div>
           <div class="logout"> <a href="logout.php">LOGOUT</a> </div>
        </div>
       <div class="heading">
           <h1>CUSTOMER DASHBOARD</h1>
       </div>

       <div class="vehicle">
           <p class=heading2>VEHICLE DETAILS</p>
           
               <form id="VehicleDetails" method= "POST" action='' enctype="multipart/form-data">
                  <p>Enter username</P>
                   <input type="text" class="input-field" name="username">
                   <p>Enter Car brand</p>
                   <input type="text" class="input-field" name="carbrand"> 
                   <p>Enter Car model</p>
                   <input type="text" class="input-field" name="carmodel">
                   <p>Enter Vehicle Purchase Date</p>
                   <input type="date" class="input-field" name="purchasedate">
                   <p>Enter Engine Type</p>
                   <input type="text" class="input-field" name="enginetype">
                   <p>Upload the RC copy, DL, PPC, NCB, Claimed Policy and Lapsed policy</p>
                   <input type='file' name='file[]' id='file' multiple>
                   <a href="uploaded.php"> <input type='submit' name='submit' value='upload'>
               </form>
            </div>

    </div>
</div>
</body>
</html>

<?php
 $dbhost = "localhost";
 $dbuser = "root";
 $dbpass = "";
 $db = "agent";
 $conn = new mysqli($dbhost, $dbuser, $dbpass,$db);
       
   if (isset($_POST['submit']))
   {
    $username=$_POST['username'];	
    $carbrand=$_POST['carbrand'];	
    $carmodel=$_POST['carmodel'];	
    $purchasedate=$_POST['purchasedate'];	
    $enginetype=$_POST['enginetype'];	
    /*$sql="INSERT INTO vehicles(username) VALUES('$username')";
    $sql="INSERT INTO vehicles(carbrand) VALUES('$carbrand')";
    $sql="INSERT INTO vehicles(carmodel) VALUES('$carmodel')";
    $sql="INSERT INTO vehicles(purchasedate) VALUES('$purchasedate')";
    $sql="INSERT INTO vehicles(enginetype) VALUES('$enginetype')";*/
    
   /* foreach($_FILES['files']['name'] as $key=>$val){
        $rand=rand('11111111','99999999');
        $file=$rand.'_'.$val;
        move_uploaded_file($_FILES['files']['tmp_name'][$key],'doc/'.$val);
        $sql= "INSERT INTO vehicles(files) VALUES('".$file."')";   
    }*/
    $fileCount=count($_FILES['file']['name']);
    for($i=0;$i<$fileCount;$i++)
   	 {
   		 $fileName=$_FILES['file']['name'][$i];
		$sql="INSERT INTO vehicles1(username,carbrand,carmodel,purchasedate,enginetype,RCcopy,DL,PPC,NCB,claimedpolicy,lapsedpolicy) VALUES ('$username','$carbrand','$carmodel','$purchasedate','$enginetype','$fileName','$fileName','$fileName','$fileName','$fileName','$fileName')";
	     //$sql = "INSERT INTO vehicle(RCcopy,DL,PPC,NCB,claimedpolicy,lapsedpolicy) VALUES ('$fileName','$fileName','$fileName','$fileName','$fileName','$fileName')";
	    if($conn->query($sql) === TRUE){
	    	echo "File uploaded successfully";
	    }else{
		    echo "error";
	    }
    
	    move_uploaded_file($_FILES['file']['tmp_name'][$i], 'upload/'.$fileName);
    }
    
   } 
?>