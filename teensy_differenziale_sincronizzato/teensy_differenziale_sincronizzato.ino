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
  //adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  //adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::LOW_SPEED);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::LOW_SPEED);

  adc->setAveraging(1, ADC_1);
  adc->setResolution(12, ADC_1);
  //adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED, ADC_1); // change the conversion speed
  //adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED, ADC_1); // change the sampling speed
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::LOW_SPEED, ADC_1); // change the conversion speed
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::LOW_SPEED, ADC_1); // change the sampling speed

  delay(3000);
  Serial.println(adc->startSynchronizedContinuousDifferential(readPin0P, readPin0N, readPin1P, readPin1N));
  //adc->stopSynchronizedContinuous();
}

ADC::Sync_result result;

int myClamp(int x)
{
  if (x > 4095)
    return 0;
  return x;
}
#define N 1000

void loop() {
  // put your main code here, to run repeatedly:

  while(!adc->isComplete());
  result = adc->readSynchronizedContinuous();
  result.result_adc0 = (uint16_t)result.result_adc0;
  result.result_adc1 = (uint16_t)result.result_adc1;
  //Serial.print(result.result_adc0);
  //Serial.print("\t");
  Serial.println(myClamp(result.result_adc1));

  unsigned long long t0 = micros();
  for (int i = 0; i < N; i++)
  {
    while(!adc->isComplete());
    result = adc->readSynchronizedContinuous();
    result.result_adc0 = (uint16_t)result.result_adc0;
    result.result_adc1 = (uint16_t)result.result_adc1;
  }
  Serial.println((float)(micros()-t0) / N);
  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(10);
  digitalWrite(LED_BUILTIN, LOW);
  delay(10);
}
