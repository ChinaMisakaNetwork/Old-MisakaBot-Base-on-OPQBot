// Edit The Following Part
$host = 'host ip';
$user = 'db username';
$pass = 'passwd';
$db = 'db name';
// Do not edit the following part
$charset = 'utf8';
function read($sql){
  $conn = new mysqli($host, $user, $pass);
  $conn->select_db($db);
  $result = $conn->query($sql);
  return $result;
  $conn->close();
}
function read_fetch_array($sql, $mode = MYSQLI_BOTH){
  $conn = new mysqli($host, $user, $pass);
  $conn->select_db($db);
  $result = $conn->query($sql);
  $arr = array()
  if ($result ->num_rows > 0){
    while($row = $result->fetch_array($mode)){
      array_push($arr, $row);
    }
  }
  $conn->close();
  return $arr;
}
function write($sql){
  $conn = new mysqli($host, $user, $pass);
  $conn->select_db($db);
  $conn->query($sql);
  $conn->close();
}
