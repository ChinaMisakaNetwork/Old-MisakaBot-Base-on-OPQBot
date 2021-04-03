$msg = $argv[1];
$qq = $argv[2];
$grp = $argv[3];
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
  if (($picurl != 0) && ($picbase != 0)){
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
    $playload = array(
      "toUser" => $to,
      "sendToType" => 1,
      "sendMsgType" => "TextMsg",
      "content" => $msg
    )
    $payload_raw = json_encode($payload);
    $response = Http_Request("POST", $url, $payload_raw);
    return $response;
  }
}
