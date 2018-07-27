// THIS CODE IS ONLY FOR ESP32
// Has hard-coded thresholds and will output six values!!
// Remember to disable buzzer and/or thresholds when not in use.

const int SAMPLENUM = 20;
const int SAMPLEEVERYNMILISECONDS = 10;
const int ENABLEBUZZER = 1;
const int BUZZERDURATIONMS = 500;
const int BUZZERCOOLDOWNMS = 3000;

int HORIZONTAL_THRESHOLD_HIGH = 0;
int HORIZONTAL_THRESHOLD_LOW = 0;
int VERTICAL_THRESHOLD_HIGH = 0;
int VERTICAL_THRESHOLD_LOW = 0;

const int horizontalBack = A17;
const int verticalBack = A10;
const int horizontalBackPower = 13;
const int verticalBackPower = 18;
const int buzzerPin = 16;
const int LEDpin = 22;

int samples = 0;
int toggle = 0;
int counter = 0;
int poorposturehb = 0;
int poorposturevb = 0;
int buzzerduration = 0;
int buzzercooldown = 0;

int temp_hb;
int temp_vb;
int hb_val;
int vb_val;
int stored_hb_val;
int stored_vb_val;

void setup() {
  
  // Configuring pinmodes for ESP32
  pinMode(horizontalBack, INPUT);
  pinMode(verticalBack, INPUT);
  
  pinMode(horizontalBackPower, OUTPUT);
  pinMode(verticalBackPower, OUTPUT);
  digitalWrite(horizontalBackPower, HIGH);
  digitalWrite(verticalBackPower, HIGH);

  pinMode(buzzerPin, OUTPUT);
  pinMode(LEDpin, OUTPUT);
  
  // Initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  
  // LED is an indicator of poor posture
  if (poorposturehb > 0 || poorposturevb > 0) {
    digitalWrite(LEDpin, HIGH);
  } else {
    digitalWrite(LEDpin, LOW);
  }
  
  // Need to manually PWM the buzzer since no tone func for this board
  // Once buzzer is triggered, it will ring for BUZZERDURATIONMS and then not ring again for BUZZERCOOLDOWNMS
  if (buzzerduration > 0 && buzzercooldown == 0 && ENABLEBUZZER > 0) {
    if (toggle) {
      digitalWrite(buzzerPin, HIGH);
      toggle = 0;
    } else {
      digitalWrite(buzzerPin, LOW);
      toggle = 1;
    }
    buzzerduration = buzzerduration - 1;
    if (buzzerduration == 0) {
      buzzercooldown = BUZZERCOOLDOWNMS;
    }
  } else {
    digitalWrite(buzzerPin, LOW);
    if (buzzercooldown > 0) {
      buzzercooldown = buzzercooldown - 1;
      buzzerduration = 0;
    }
  }

  // Read sensors every SAMPLEEVERYNMILISECONDS
  if (counter % SAMPLEEVERYNMILISECONDS == 0) {
    temp_hb = analogRead(horizontalBack);
    temp_vb = analogRead(verticalBack);

    // Error detection for short or open circuits
    if (temp_hb==0 || temp_hb==4095) { 
      Serial.println("HB error");
    }
    if (temp_vb==0 || temp_vb==4095) { 
      Serial.println("VB error");
    }

    hb_val = hb_val + temp_hb;
    vb_val = vb_val + temp_vb;
    samples = samples + 1;
  }

  // Calculate average sensor values every SAMPLENUM samples collected
  if (samples == SAMPLENUM) {
    stored_hb_val = hb_val/SAMPLENUM;
    stored_vb_val = vb_val/SAMPLENUM;

    // Clear the sums
    hb_val = 0;
    vb_val = 0;
    samples = 0;

    // Update poorposture status
    if (poorposturehb > 0 || poorposturevb > 0) {
      // It's considered good posture once value rises above high threshold again
      if (stored_hb_val > HORIZONTAL_THRESHOLD_HIGH) {
        poorposturehb = 0;
      }
      if (stored_vb_val > VERTICAL_THRESHOLD_HIGH) {
        poorposturevb = 0;
      }
    } else {
      // It's considered poor posture once value drops below low threshold
      if (stored_hb_val < HORIZONTAL_THRESHOLD_LOW) {
        poorposturehb = 1;
        buzzerduration = BUZZERDURATIONMS;
      }
      if (stored_vb_val < VERTICAL_THRESHOLD_LOW) {
        poorposturevb = 1;
        buzzerduration = BUZZERDURATIONMS;
      }
    }

//    // REMOVED DUE TO LATENCY
//    // Listen for threshold values from GUI
//    if (Serial.available()) {
//      delay(1);
//      serial_says = Serial.readString();
//      
//      cm1 = serial_says.indexOf(',');
//      HORIZONTAL_THRESHOLD_HIGH = (serial_says.substring(0,cm1)).toInt();
//      cm2 = serial_says.indexOf(',', cm1+1);
//      HORIZONTAL_THRESHOLD_LOW = (serial_says.substring(cm1+1,cm2)).toInt();
//      cm3 = serial_says.indexOf(',', cm2+1);
//      VERTICAL_THRESHOLD_HIGH = (serial_says.substring(cm2+1,cm3)).toInt();
//      cm4 = serial_says.indexOf(',', cm3+1);
//      VERTICAL_THRESHOLD_LOW = (serial_says.substring(cm3+1)).toInt();
//    }
      
    // print the results to the Serial Monitor:
    Serial.print(stored_hb_val);
    Serial.print(",");
    Serial.print(stored_vb_val);
    Serial.print(",");
    Serial.print(HORIZONTAL_THRESHOLD_HIGH);
    Serial.print(",");
    Serial.print(HORIZONTAL_THRESHOLD_LOW);
    Serial.print(",");
    Serial.print(VERTICAL_THRESHOLD_HIGH);
    Serial.print(",");
    Serial.println(VERTICAL_THRESHOLD_LOW);
  }

  // Delay and increment counter for next loop
  delay(1);
  if (counter > 1000) {
    counter = 0;
  } else {
    counter = counter + 1;
  }
}
