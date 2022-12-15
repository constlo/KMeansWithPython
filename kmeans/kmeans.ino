#include "pisteet.h"

int xPin= A0, yPin = A1, zPin=A2;
int xVal, yVal, zVal;
int trigPin = 2;
int num;

float distances[4];
float smallestDist;
int smallestIndex;
int dir;

void setup() {
  // put your setup code here, to run once:
  pinMode(trigPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // Käynnistä mittaus, jos painonappia painetaan:
    
    if (Serial.available() > 0)
    {
      num = Serial.parseInt();
      for(int i = 0; i < 1000; i++){
      xVal = analogRead(xPin);
      delay(10);
      yVal = analogRead(yPin);
      delay(10);
      zVal = analogRead(zPin);
      delay(10);
  
      //Määrittele etäisyydet 4 centroidiin. Suunta on se, joka on lähinnä centroidia.
      for(int i = 0; i < 4; i++)
      {
        double delta_x = ((double)pisteet[i][0] - (double)xVal);
        double delta_y = ((double)pisteet[i][1] - (double)yVal);
        double delta_z = ((double)pisteet[i][2] - (double)zVal);
        distances[i] = sqrt(pow(delta_x, 2) + pow(delta_y, 2) + pow(delta_z, 2));
  
        //Koska mittaus tehdään vain kerran, voidaan pienin luku tarkastaa switch-loopilla.
        switch(i)
        {
          case 0:
            smallestIndex = 0;
            smallestDist = distances[0];
            dir = 1;
            break;
          case 1:
            if(distances[i] < distances[0])
            {
              smallestIndex = i;
              smallestDist = distances[i];
              dir = 4;
            }
            break;
          case 2:
            if(distances[i] < distances[0] && distances[i] < distances[1] )
            {
              smallestIndex = i;
              smallestDist = distances[i];
              dir = 3;
            }
            break;
          case 3:
            if(distances[i] < distances[0] && distances[i] < distances[1] && distances[i] < distances[2])
            {
              smallestIndex = i;
              smallestDist = distances[i];
              dir = 2;
            }
            break;
        }
      }
      Serial.print(xVal);
      Serial.print(",");
      Serial.print(yVal);
      Serial.print(",");
      Serial.print(zVal);
      Serial.print(",");
      Serial.print(dir);
      Serial.print(",");
      Serial.println(num);
      }
     delay(10000);
    }
}
