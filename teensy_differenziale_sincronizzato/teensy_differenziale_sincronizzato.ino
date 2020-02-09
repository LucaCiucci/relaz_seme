#include <ADC.h>

const int readPin0P = A10;
const int readPin0N = A11;
const int readPin1P = A12;
const int readPin1N = A13;

const int chargePin = 15;
const int dischargePin = 16;
const int pulsePin = 13;

ADC *adc = new ADC(); // adc object

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(readPin0P, INPUT);
  pinMode(readPin0N, INPUT);
  pinMode(readPin1P, INPUT);
  pinMode(readPin1N, INPUT);
  
  Serial.begin(9600);

  adc->setAveraging(1); // set number of averages
  adc->setResolution(12);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  adc->setAveraging(1, ADC_1);
  adc->setResolution(12, ADC_1);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED, ADC_1); // change the conversion speed
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED, ADC_1); // change the sampling speed

  delay(3000);
  Serial.println(adc->analogRead(readPin0P, ADC_0));
  Serial.println(adc->analogRead(readPin0N, ADC_0));
  Serial.println(adc->analogRead(readPin1P, ADC_1));
  Serial.println(adc->analogRead(readPin1N, ADC_1));
  Serial.println(ADC_ERROR_VALUE);
  Serial.println(adc->startSynchronizedContinuousDifferential(readPin0P, readPin0N, readPin1P, readPin1N));
  adc->stopSynchronizedContinuous();
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED_BUILTIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  delay(100);
}
