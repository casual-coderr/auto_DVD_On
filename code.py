#include <DS3231.h>
#include <ir_Lego_PF_BitStreamEncoder.h>
#include <boarddefs.h>
#include <IRremoteInt.h>
#include <IRremote.h>

int RECV_PIN = 2;                                               
int system_state=0; int led_status=0; 
int relay_1=5;
int r_count=0; //remote control counter
int t_count_on=0; //timer control counter
int t_count_off=0;

const int OnHour = 04;
const int OnMin = 45;
const int OffHour = 07;
const int OffMin = 00;

DS3231  rtc(SDA, SCL);
Time t;
IRrecv irrecv(RECV_PIN);                                        
decode_results results;
                                         // define variable "results" as decoded results from IR library 'irrecv.decode' command

void setup()
{
  Serial.begin(9600);
  rtc.begin(); 
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(relay_1, OUTPUT);                                     // define pin 5 as output pin
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10, OUTPUT);
  digitalWrite(8, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(10, HIGH);
  digitalWrite(relay_1, HIGH);
  irrecv.enableIRIn();                     // working for receiving IR signals 
}

void loop() 
{
  //IR MODULE PART
  if (irrecv.decode(&results)) {                                // check whether any infrared signal available
    Serial.print(r_count); Serial.print(" - ");                   // print the count value and system state for croschecking the output
    Serial.print(system_state); Serial.print(" - ");
    Serial.println(results.value,HEX);                          // convert into HEX datat and print in the serial monitor
    switch (results.value) 
    {                                    // start comparing received data
       case 16464071:
          {                                               // check whether ON/OFF button pressed
      if(system_state==0)                                       // if system is in OFF state
        {system_state=1;
        digitalWrite(relay_1, HIGH);
        Serial.println("LIGHT OFF");
        }
        // change the system state to ON
      else if (system_state==1)                                 // if system is in ON state
        {
          system_state=0;
          digitalWrite(relay_1, LOW);
          Serial.println("LIGHT ON");
        }   
        r_count++;                                     
            }
       default: break;
    
    }
    delay(1000);                                                
  irrecv.resume();                                              // receiver is ready to receive data
  }//IR MODULE PART
  
  //TIMER CKT PART
  t = rtc.getTime();
  Serial.print(t.hour);
  Serial.print(" hour(s), ");
  Serial.print(t.min);
  Serial.print(" minute(s), ");
  Serial.print(t.sec);
  Serial.print(" Second(s)");
  Serial.println(" ");

  if(t.hour == 0 && t.min == 00)
  {
    t_count_on=0;
    t_count_off=0;
    digitalWrite(LED_BUILTIN, LOW);
  }
  
  
  if(t.hour == OnHour && t.min == OnMin && t_count_on == 0)
    {
    digitalWrite(relay_1,LOW);
    Serial.println("LIGHT ON");
    t_count_on++;
    
    }
    
    else if(t.hour == OffHour && t.min == OffMin && t_count_off == 0)
    {
      digitalWrite(relay_1,HIGH);
      Serial.println("LIGHT OFF");
      t_count_off++;
      digitalWrite(LED_BUILTIN, HIGH);
    }
    delay(1000);
  
}//loop bracket
