
const int readPin = A9;
const int readPin2 = A3;

const int chargePin = 15;
const int dischargePin = 16;
const int pulsePin = 13;

#include <ADC.h>

ADC *adc = new ADC(); // adc object

void setup() {
  // put your setup code here, to run once:

  pinMode(pulsePin, OUTPUT);
  pinMode(readPin, INPUT);
  pinMode(readPin2, INPUT);
  pinMode(chargePin, OUTPUT);
  pinMode(dischargePin, OUTPUT);
  pinMode(pulsePin, OUTPUT); digitalWrite(pulsePin, HIGH);

  Serial.begin(9600);

  /*while(1)
  {
    digitalWrite(chargePin, HIGH);
    delay(5000);
    digitalWrite(chargePin, LOW);
    //delay(5000);
    digitalWrite(dischargePin, HIGH);
    delay(2000);
    digitalWrite(dischargePin, LOW);
    //delay(5000);
  }*/

  adc->setAveraging(1); // set number of averages
  adc->setResolution(12);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  adc->setAveraging(1, ADC_1);
  adc->setResolution(12, ADC_1);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED, ADC_1); // change the conversion speed
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED, ADC_1); // change the sampling speed

  adc->startSynchronizedContinuous(readPin, readPin2);

  /*Serial.println("CHARGING...");
  digitalWrite(chargePin, HIGH);
  delay(10000);
  digitalWrite(chargePin, LOW);*/

  /*for (int i = 10; i > 0; i--)
  {
    Serial.println(i);
    delay(1000);
  }*/

  Serial.println("DISCHARGING...");
  digitalWrite(dischargePin, HIGH);
  delay(10000);
  digitalWrite(dischargePin, LOW);
}

ADC::Sync_result result;

#define N 100
int sensorValues[N][2];

void loop() { 

  digitalWrite(chargePin, HIGH);
  delay(1000);
  digitalWrite(chargePin, LOW);

  //Serial.println("ACQUIRING...");
  unsigned long long t0 = micros();
  digitalWrite(pulsePin, LOW);
  delayMicroseconds(50);
  for (int i = 0; i < N; i++)
  {
    while(!adc->isComplete());
    result = adc->readSynchronizedContinuous();
    sensorValues[i][0] = result.result_adc0 = (uint16_t)result.result_adc0;
    sensorValues[i][1] = result.result_adc1 = (uint16_t)result.result_adc1;
  }
  digitalWrite(pulsePin, HIGH);

  //Serial.println("DATA:");
  for (int i = 0; i < N; i++)
  {
    Serial.print(sensorValues[i][0]);
    Serial.print("\t");
    Serial.println(sensorValues[i][1]);
  }
  //Serial.print("time (us): ");
  //Serial.println((int)(micros() - t0));
  //Serial.println(float(micros() - t0) / 255);
  //delay(2000);

  /*while(!adc->isComplete());
  result = adc->readSynchronizedContinuous();
  result.result_adc0 = (uint16_t)result.result_adc0;
  result.result_adc1 = (uint16_t)result.result_adc1;
  Serial.println(result.result_adc0);
  delay(10);*/
}
