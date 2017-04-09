var puckID = '690d'; // change!!

// Are we busy?
var busy = false;

// The device, if we're connected
var connected = false;

// The 'tx' characteristic, if connected
var txCharacteristic = false;

function pad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length-size);
}


function getHEXValue() {
    light = Puck.light() * 1000;
    lightHEX = Math.round(light).toString(16);
    lightHEX = pad(lightHEX,3);
    
    temperature = E.getTemperature() * 10;
    temperatureHEX = Math.round(temperature).toString(16);
    temperatureHEX = pad(temperatureHEX,3);    

    battery = NRF.getBattery() * 100;
    batteryHEX = Math.round(battery).toString(16);
    batteryHEX = pad(batteryHEX,3);        
    
    return lightHEX+temperatureHEX+batteryHEX;
}

// Function to call 'toggle' on the other Puck
function sendToggle() {
  if (!busy) {
    busy = true;
    if (!connected) {
      NRF.requestDevice({ filters: [{ name: 'LoPy01' }] }).then(function(device) {
        return device.gatt.connect();
      }).then(function(d) {
        digitalPulse(LED3, 1, 1500); // light blue       
        connected = d;
        return d.getPrimaryService("36353433-3231-3039-3837-363534333231");
      }).then(function(s) {
        return s.getCharacteristic("36353433-3231-3039-3837-363534336261");
      }).then(function(c) {
        hexValue = puckID + getHEXValue();
        console.log(hexValue);
        c.writeValue(hexValue);
        busy = false;

      }).then(function() {
        if (connected) connected.disconnect();
        connected=false;
        digitalPulse(LED2, 1, 1000); // light green                
      }).catch(function() {
        if (connected) connected.disconnect();
        connected=false;
        digitalPulse(LED1, 1, 1000); // light red if we had a problem
        busy = false;
      });
    } else {
      console.log("already connected!");
      if (connected) connected.disconnect();
      connected=false;      
      busy = false;
    }
  } else {
      console.log("already busy!");
      if (connected) connected.disconnect();
      connected=false;      
      busy = false;
  }
}

// Call this function when the button is pressed
setWatch(sendToggle, BTN, { edge:"rising", debounce:50, repeat: true });
