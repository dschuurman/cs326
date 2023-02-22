<html>
<head>
   <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
<h2>Raspberry Pi Temperature Cloud Data</h2>
<div id='chart_div'></div>

<?PHP
# Open SQL cloud database
 $host = "hostname";
 $user = "username";
 $pass = "password";
 $db = "database";
 $con = pg_connect("host=$host dbname=$db user=$user password=$pass")
	 or die ("Could not connect to SQL server\n");
?>

<script>
var data = [{
   x: [
<?PHP
   # Use PHP to query database and build JavaScript array
   $query = 'SELECT * FROM temperaturedata';
   $result = pg_query($con,$query) or die('Query failed');
   $array = pg_fetch_all($result);
   foreach ($array as $row) {
      echo "    '" . $row['datetime'] . "',\n";
   }
 
?>
   ],
   y: [
<?PHP       
   foreach ($array as $row) {
      echo "    " . $row['temperature'] . ",\n";
   }
?>
   ],
   type: 'scatter'
}];

var layout = {
    xaxis: { title: 'Date and time' },
    yaxis: { title: 'Temperature (degrees C)' }
};

Plotly.newPlot('chart_div', data, layout );
</script>
</body>
</html>
