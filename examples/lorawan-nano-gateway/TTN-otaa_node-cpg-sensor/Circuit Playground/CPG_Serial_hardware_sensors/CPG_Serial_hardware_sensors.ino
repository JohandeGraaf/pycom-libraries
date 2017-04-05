#include <Adafruit_CircuitPlayground.h>
#include <Wire.h>
#include <SPI.h>


#define TEMP_INPUT  A0  //  - A0  = temperature sensor / thermistor
#define SOUND_INPUT  A4  //  - A4  = sound sensor / microphone
#define LIGHT_INPUT  A5  //  - A5  = light sensor
 
String Data = "";

void setup() {
  CircuitPlayground.begin();  
  // initialize serial ports
  Serial.begin(9600);    // USB serial port 0
  Serial1.begin(9600);       // serial port 1, TX/RX
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }  
  
  Serial.println("Setup complete");
}

byte rx_byte = 0;        // stores received byte
int x = 0;
String returnvalue = "";

void loop() {
  while (Serial1.available())
    {
        
        char character = Serial1.read(); // Receive a single character from the software serial port
        if (isDigit(character)) {
          Data.concat(character); // Add the received character to the receive buffer, wait for end of line
        }
        if (character == '\n')
        {
            int x = Data.toInt(); 
            Serial.print("Received: ");
            Serial.println(x);            

            if(x > 0 && x <= 10) {
              uint16_t tempvalue = analogRead(TEMP_INPUT);
              Serial.print("TEMP_INPUT: ");            
              Serial.println(tempvalue, DEC);
              String tempstring = String(tempvalue, HEX);
              if (tempvalue < 256) tempstring = "0" + tempstring;
              if (tempvalue < 16) tempstring = "0" + tempstring;

              uint16_t soundvalue = analogRead(SOUND_INPUT);
              Serial.print("SOUND_INPUT: ");            
              Serial.println(soundvalue, DEC);
              String soundstring = String(soundvalue, HEX);
              if (soundvalue < 256) soundstring = "0" + soundstring;
              if (soundvalue < 16) soundstring = "0" + soundstring;
              
              uint16_t lightvalue = analogRead(LIGHT_INPUT);
              Serial.print("LIGHT_INPUT: ");            
              Serial.println(lightvalue, DEC);
              String lightstring = String(lightvalue, HEX);
              if (lightvalue < 256) lightstring = "0" + lightstring;
              if (lightvalue < 16) lightstring = "0" + lightstring;        
                  
              returnvalue = tempstring + soundstring + lightstring; 
     
              CircuitPlayground.clearPixels();
              for (int i=0; i < x; i++){
                CircuitPlayground.setPixelColor(i, 0x0000FF);
              }
            } else {
              Serial.println("Received unknown input");
              CircuitPlayground.setPixelColor(0, 0xFF0000);    
              returnvalue =  String('000000000');
            }
            
            Serial1.println(returnvalue);
            Serial.print(" Returned: ");
            Serial.println(returnvalue);              
 
            // Clear receive buffer so we're ready to receive the next line
            
            Data = "";
        }
    }
  }

