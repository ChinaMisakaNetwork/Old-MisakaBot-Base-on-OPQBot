require 'sql.php';
$msg = base64_decode($argv[1]);
$qq = base64_decode($argv[2]);
$grp = base64_decode($argv[3]);
$config = fopen("../../../config.json", "r");
$configarr = fread($config,filesize("../../../config.json"));
fclose($config);
$serverurl = $configarr -> {"server"};
$botqq = $configarr -> {"botqq"};
$tsut = $configarr -> {"TextShutupTime"};
$wt = $configarr -> {"WarningTimes"};
$logg = $configarr -> {"loggroup"};
function Http_Request($method, $url, $json=null, $data=null){
  if (!is_null($json)){
    $opts = array('http' =>
      array(
        'method'  => $method,
        'header'  => 'Content-Type: application/json',
        'content' => $json
      )
    );
  }
  else if (!is_null($data)){
    $opts = array('http' =>
      array(
        'method'  => $method,
        'header'  => 'Content-Type: application/x-www-form-urlencoded',
        'content' => $data
      )
    );
  }
  else {
    $opts = array('http' =>
      array(
        'method'  => $method
      )
    );
  }
  $context  = stream_context_create($opts);
  $result = file_get_contents($url, false, $context);
  return $result;
}
function UserMsg($msg, $to, $picurl=0, $picbase=0){
  global $serverurl;
  global $botqq;
  $url = $serverurl + "/v1/LuaApiCaller?qq=" + strval($botqq) + "&funcname=SendMsg";
  if (($picurl != 0) || ($picbase != 0)){
    $payload = array(
      "toUser" => $to,
      "sendToType" => 1,
      "sendMsgType" => "PicMsg",
      "content" => $msg,
      "picUrl" => $picurl,
      "picBase64Buf" => $picbase
    );
    $payload_raw = json_encode($payload);
    $response = Http_Request("POST", $url, $payload_raw);
    return $response;
  } else {
    $payload = array(
      "toUser" => $to,
      "sendToType" => 1,
      "sendMsgType" => "TextMsg",
      "content" => $msg
    );
    $payload_raw = json_encode($payload);
    $response = Http_Request("POST", $url, $payload_raw);
    return $response;
  }
}
function GroupMsg($msg, $to, $picurl=0, $picbase=0){
  global $serverurl;
  global $botqq;
  $url = $serverurl + "/v1/LuaApiCaller?qq=" + strval($botqq) + "&funcname=SendMsg";
  if (($picurl != 0) || ($picbase != 0)){
    $payload = array(
      "toUser" => $to,
      "sendToType" => 2,
      "sendMsgType" => "PicMsg",
      "content" => $msg,
      "picUrl" => $picurl,
      "picBase64Buf" => $picbase
    );
    $payload_raw = json_encode($payload);
    $response = Http_Request("POST", $url, $payload_raw);
    return $response;
  } else {
    $payload = array(
      "toUser" => $to,
      "sendToType" => 2,
      "sendMsgType" => "TextMsg",
      "content" => $msg
    );
    $payload_raw = json_encode($payload);
    $response = Http_Request("POST", $url, $payload_raw);
    return $response;
  }
}
function SetShutUpUser($qq, $time, $groupid){
  global $serverurl;
  global $botqq;
  $url = $serverurl + "/v1/LuaApiCaller?qq=" + strval($botqq) + "&funcname=OidbSvc.0x570_8";
  $payload = array(
    "GroupId" => $groupid,
    "ShutUpUserID" => $qq,
    "ShutTime" => $time
  );
  $payload_raw = json_encode($payload);
  $response = Http_Request("POST", $url, $payload_raw);
  return $response;
}
function TemporaryMsg($msg, $to, $groupid, $picbase=0, $picurl=0){
  global $serverurl;
  global $botqq;
  $url = $serverurl + '/v1/LuaApiCaller?qq=' + strval($botqq) + '&funcname=SendMsg';
  if (($picbase != 0) || ($picurl != 0)){
    $payload = array(
      "toUser" => $to,
      "groupid" => $groupid,
      "sendToType" => 3,
      "sendMsgType" => "PicMsg",
      "content" => $msg,
      "picUrl" => $picurl,
      "picBase64Buf" => $picbase
    );
    $response = Http_Request("POST", $url, json_encode($payload));
  }
  else {
    $payload = array(
      "toUser" => $to,
      "groupid" => $groupid,
      "sendToType" => 3,
      "sendMsgType" => "TextMsg",
      "content" => $msg
    );
    $response = Http_Request("POST", $url, json_encode($payload));
  }
  return $response;
}
function Announce($groupid, $title, $text, bool $Pinned, bool $Usewindow, bool $tonewuser){
  global $serverurl;
  global $botqq;
  $url = $serverurl + "/v1/Group/Announce?qq=" + strval($qq);
  if ($Pinned){
    $Pinned = 1;
  }
  else {
    $Pinned = 0;
  }
  
  if ($Usewindow) {
    $Type = 10;
  }
  else if ($tonewuser) {
    $Type = 20;  
  }
  else {
    $Type = 0;
  }
  $payload = array(
    "GroupId" => $groupid,
    "Title" => $title,
    "Text" => $text,
    "Pinned" => $Pinned,
    "Type" => $Type
  );
  $response = Http_Request("POST", $url, json_encode($payload));
  return $response;
}
function CheHui($GroupID, $MsgSeq, $MsgRandom){
  global $serverurl;
  global $botqq;
  $url = $serverurl + '/v1/LuaApiCaller?qq=' + strval(qq) + "&funcname=PbMessageSvc.PbMsgWithDraw";
  $payload = array(
    "GroupID" => $GroupID,
    "MsgSeq" => $MsgSeq,
    "MsgRandom" => $MsgRandom
  );
  $response = Http_Request("POST", $url, json_encode($payload));
  return $response;
}
function GetUserBilibili(int $qq){
  $qq = strval($qq);
  $result = $read_fetch_array('select * from bilibili where QQ="'+$qq+'";');
  if (sizeof($result) < 1){
    return null;
  }
  else {
    return array("csrf" => $result[0][1], "cookie" => $result[0][2]);
  }
}
