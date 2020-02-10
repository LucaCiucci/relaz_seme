#include <ADC.h>

const int readPin0P = A10;
const int readPin0N = A11;
const int readPin1P = A12;
const int readPin1N = A13;

const int out3Pin = A0;
#define OUT3FACTOR (11.0/1024.0 * 3.3  / 4)
const int chargePin = 15;
const int dischargePin = 16;
const int pulsePin = 13;

ADC *adc = new ADC(); // adc object

////////////////////////////////////////////////////////////////
float getCapVoltage(void);
bool chargeToVoltage(float voltage, double maxSeconds = 20);
bool acquisizione(void);
bool acquisizione(float capVoltage);
void printData(void);

int *ch1Data = NULL, *ch2Data = NULL;
const int nAcq = 10;

void setup() {
  // put your setup code here, to run once:
  pinMode(readPin0P, INPUT);
  pinMode(readPin0N, INPUT);
  pinMode(readPin1P, INPUT);
  pinMode(readPin1N, INPUT);
  pinMode(out3Pin, INPUT);
  pinMode(chargePin, OUTPUT);
  pinMode(dischargePin, OUTPUT);
  pinMode(pulsePin, OUTPUT); digitalWrite(pulsePin, HIGH);

  ch1Data = new int[nAcq];
  ch2Data = new int[nAcq];
  
  Serial.begin(9600);

  adc->setAveraging(1);
  adc->setResolution(10);
  adc->setAveraging(1, ADC_1);
  adc->setResolution(10, ADC_1);

  delay(4000);
  
}

int myClamp(int x)
{
  if (x > 4095)
    return x - 65535;
  return x;
}

void loop() {
  // put your main code here, to run repeatedly:

  /*for (float v = 0.2; v <= 4.0; v += 0.01)
  {
    acquisizione(v);
    printData();
    delay(100);
  }*/
  for (int i = 0; i < 1000; i++)
  {
    digitalWrite(chargePin, HIGH);
    delay(10);
    digitalWrite(chargePin, LOW);
    acquisizione();
  }

  digitalWrite(dischargePin, HIGH);
  delay(1000);
  digitalWrite(dischargePin, LOW);

  /*for (int i = 0; true; i++)
  {
    delay(10);
    Serial.println(getCapVoltage());
  }*/


}

////////////////////////////////////////////////////////////////
float getCapVoltage(void)
{
  //return OUT3FACTOR * adc->analogRead(out3Pin, ADC_0);
  delay(1);
  return 11.0 * 3.3 * adc->adc0->analogRead(out3Pin) / adc->adc0->getMaxValue();
}

////////////////////////////////////////////////////////////////
bool chargeToVoltage(float voltage, double maxSeconds)
{
  unsigned long t0 = millis();
  if (getCapVoltage() < voltage)
  {
    digitalWrite(chargePin, HIGH);
    while (getCapVoltage() < voltage)
      if (millis() - t0 > maxSeconds * 1000)
      {
        digitalWrite(chargePin, LOW);
        return false;
      }
    digitalWrite(chargePin, LOW);
  }
  if (getCapVoltage() > voltage)
  {
    digitalWrite(dischargePin, HIGH);
    while (getCapVoltage() > voltage)
      if (millis() - t0 > maxSeconds * 1000)
      {
        digitalWrite(dischargePin, LOW);
        return false;
      }
    digitalWrite(dischargePin, LOW);
  }

  delay(10);
  return true;
}

////////////////////////////////////////////////////////////////
bool acquisizione(void)
{
  // inizia l'acquisizione analogica
  adc->setAveraging(1);
  adc->setResolution(12);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  adc->setAveraging(1, ADC_1);
  adc->setResolution(12, ADC_1);
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED, ADC_1);
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED, ADC_1);
  
  adc->startSynchronizedContinuousDifferential(readPin0P, readPin0N, readPin1P, readPin1N);

  // attacca il MOS-FET
  digitalWrite(pulsePin, LOW);
  delayMicroseconds(50);// TODO: vedi se va bene e mangiare un panino

  unsigned long t0 = micros();
  for (int i = 0; i < nAcq; i++)
  {
    while(!adc->isComplete());
    result = adc->readSynchronizedContinuous();
    ch1Data[i] = (uint16_t)result.result_adc0;
    ch2Data[i] = (uint16_t)result.result_adc1;
  }
  digitalWrite(pulsePin, HIGH);
  
  //Serial.print("ci ho impiegato tot us per conversione");
  //Serial.println((float)(micros()-t0) / nAcq);
  
  adc->stopSynchronizedContinuous();

  return true;
}

////////////////////////////////////////////////////////////////
bool acquisizione(float capVoltage)
{
  ADC::Sync_result result;
  bool flag = true;

  // carica il condensatore e controlla se ha funzionato
  flag = chargeToVoltage(capVoltage);
  if (flag == false)
    return flag;

  return acquisizione();
}

////////////////////////////////////////////////////////////////
void printData(void)
{
  //Serial.println("# data\nch1\tch2");
  for (int i = 0; i < nAcq; i++)
  {
    Serial.print(ch1Data[i]);
    Serial.print("\t");
    Serial.println(myClamp(ch2Data[i]));
  }
}
