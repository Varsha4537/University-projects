
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Dashboard</title>
    <link rel="stylesheet" href="agent.css">
</head>
<body>
    <div class="container"></div>
    <div class="log"> 
        
        <div class="exit">
           
           <div class="home"> <a href="home.php">HOME</a> </div>
           <div class="logout"> <a href="logout.php">LOGOUT</a> </div>
        </div>
        <div class="heading">
           <h1>AGENT DASHBOARD</h1>
           
        </div>

       <div class="vehicle">
           <p class=heading2>CUSTOMER DETAILS</p>

           
                   
        </div>
        <style>
table {
border-collapse: collapse;
width: 100%;
color: #588c7e;
font-family: monospace;
font-size: 15px;
text-align: left;
}
th {
background-color: #588c7e;
color: white;
}
tr:nth-child(even) {background-color: #f2f2f2}
</style>
<table>
<tr>
<th>username</th>
<th>carbrand</th>
<th>carmodel</th>
<th>purchasedate</th>
<th>enginetype</th>
<th>RCcopy</th>
<th>DL</th>
<th>PPC</th>
<th>NCB</th>
<th>claimedpolicy</th>
<th>lapsedpolicy</th>
</tr>

<?php
$conn = mysqli_connect("localhost", "root", "", "agent");
// Check connection
if ($conn->connect_error) {
die("Connection failed: " . $conn->connect_error);
}
$sql = "SELECT username, carbrand, carmodel, purchasedate, enginetype, RCcopy, DL, PPC, NCB, claimedpolicy, lapsedpolicy FROM vehicles1";
$result = $conn->query($sql);
if ($result->num_rows > 0) {
// output data of each row
while($row = $result->fetch_assoc()) {
echo "<tr><td>" . $row["username"]. "</td><td>" . $row["carbrand"] . "</td><td>" . $row["carmodel"]. "</td><td>". $row["purchasedate"]. "</td><td>". $row["enginetype"]. "</td><td>". $row["RCcopy"]. "</td><td>". $row["DL"]. "</td><td>". $row["PPC"]. "</td><td>". $row["NCB"]. "</td><td>". $row["claimedpolicy"]. "</td><td>". $row["lapsedpolicy"]. "</td></tr>";
}
echo "</table>";
} else { echo "0 results"; }
$conn->close();
?>
</table>
    </div>
</div>
</body>
</html>