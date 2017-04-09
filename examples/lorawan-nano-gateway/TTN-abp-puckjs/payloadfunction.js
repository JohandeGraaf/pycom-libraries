function Decoder(bytes, port) {
  
  var decoded = {};
  var str = '';
  for (var i = 0; i < bytes.length; i += 1)
    str += String.fromCharCode(parseInt(bytes[i]));

  decoded.byteslength = bytes.length;
  decoded.raw = bytes;
  decoded.hexstring = str;  
  decoded.puckid = str.substring(0, 4);
  decoded.light = parseInt(str.substring(4, 7), 16)/1000;
  decoded.temperature = parseInt(str.substring(7, 10), 16)/10;
  decoded.battery = parseInt(str.substring(10, 13), 16)/100;

  return decoded;
}
