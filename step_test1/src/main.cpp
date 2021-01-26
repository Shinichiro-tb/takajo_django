#include <Arduino.h>

/*ピンの定義*/
#define step_cam_1 2  //カム
#define step_cam_2 3
#define step_cam_3 4
#define step_cam_4 5

#define step_gear_1 8 //ギア
#define step_gear_2 9
#define step_gear_3 10
#define step_gear_4 11

#define cam_sw 43  //リミット
#define gear_sw 41

#define LED_1 22  //LED
#define LED_2 23
#define LED_3 24
#define LED_4 25
#define LED_5 26
#define LED_6 27
#define LED_7 28
#define LED_8 29
#define LED_9 30
#define LED_10 31
#define LED_11 32
#define LED_12 33

#define ir_1 51  //リミット
#define lm_2 36
#define ir_3 50
#define lm_4 38
#define ir_5 49
#define lm_6 37
#define ir_7 48
#define lm_8 42
#define ir_9 47
#define lm_10 40
#define ir_11 46
#define lm_12 39

/*ステッピングモーター速度決定*/
const int cam_delay  = 3;
const int gear_delay = 3;

/*鍵の位置を配列に格納*/
int key_place_list[13][4] = {  //左右方向の位置, 上下方向の位置, 鍵確認用物理スイッチ, LED
  {  0 ,  0,   0  ,   0   },

  {-688,  1, ir_1 , LED_1 },  //鍵番号1
  {-452,  1, lm_2 , LED_2 },
  {-118,  1, ir_3 , LED_3 },
  { 118,  1, lm_4 , LED_4 },
  { 452,  1, ir_5 , LED_5 },
  { 688,  1, lm_6 , LED_6 },
  {-688, -1, ir_7 , LED_7 },
  {-452, -1, lm_8 , LED_8 },
  {-118, -1, ir_9 , LED_9 },
  { 118, -1, lm_10, LED_10 },
  { 452, -1, ir_11, LED_11 },
  { 688, -1, lm_12, LED_12 },
};

/*関数宣言*/
void step_cam_CCW(void);
void step_cam_CW(void);
void step_cam_stop(void);
void step_cam(int, int);

void step_gear_CCW(void);
void step_gear_CW(void);
void step_gear_stop(void);
void step_gear_reset(void);
void step_gear(int);

void check_key(int);

/*cam(上下)を制御する関連*/
void step_cam_CCW(void){  //カム用ステッピングモーター反時計回り
  digitalWrite(step_cam_1, HIGH);
  digitalWrite(step_cam_2, HIGH);
  digitalWrite(step_cam_3, LOW);
  digitalWrite(step_cam_4, LOW);
  delay(cam_delay);
  
  digitalWrite(step_cam_1, LOW);
  digitalWrite(step_cam_2, HIGH);
  digitalWrite(step_cam_3, HIGH);
  digitalWrite(step_cam_4, LOW);
  delay(cam_delay);
  
  digitalWrite(step_cam_1, LOW);
  digitalWrite(step_cam_2, LOW);
  digitalWrite(step_cam_3, HIGH);
  digitalWrite(step_cam_4, HIGH);
  delay(cam_delay);
  
  digitalWrite(step_cam_1, HIGH);
  digitalWrite(step_cam_2, LOW);
  digitalWrite(step_cam_3, LOW);
  digitalWrite(step_cam_4, HIGH);
  delay(cam_delay);
}

void step_cam_CW(void){  //カム用ステッピングモーター時計回り
  digitalWrite(step_cam_1, HIGH);
  digitalWrite(step_cam_2, LOW);
  digitalWrite(step_cam_3, LOW);
  digitalWrite(step_cam_4, HIGH);
  delay(cam_delay);
  
  digitalWrite(step_cam_1, LOW);
  digitalWrite(step_cam_2, LOW);
  digitalWrite(step_cam_3, HIGH);
  digitalWrite(step_cam_4, HIGH);
  delay(cam_delay);
  
  digitalWrite(step_cam_1, LOW);
  digitalWrite(step_cam_2, HIGH);
  digitalWrite(step_cam_3, HIGH);
  digitalWrite(step_cam_4, LOW);
  delay(cam_delay);
  
  digitalWrite(step_cam_1, HIGH);
  digitalWrite(step_cam_2, HIGH);
  digitalWrite(step_cam_3, LOW);
  digitalWrite(step_cam_4, LOW);
  delay(cam_delay);
}

void step_cam_stop(void){  //カム用ステッピングモーターパルス停止
  digitalWrite(step_cam_1, LOW);
  digitalWrite(step_cam_2, LOW);
  digitalWrite(step_cam_3, LOW);
  digitalWrite(step_cam_4, LOW);
}

void step_cam(int select_ud, int number){  //
  int count = 0;

  if (select_ud == 1){  //鍵が上の段
    Serial.println("step_cam_upper");
    while (count<133){
      step_cam_CW();
      count++;
    }
    step_cam_stop();
    count = 0;

    check_key(number);  //鍵チェック！！

    while(digitalRead(cam_sw)==HIGH){
      step_cam_CCW();
    }
    while(count<19){
      step_cam_CCW();
      count++;
    }
  }

  else if (select_ud == -1){  //鍵が下の段
  Serial.println("step_cam_down");
    while (count<128){
      step_cam_CCW();
      count++;
    }
    step_cam_stop();
    count=0;

    check_key(number);  //鍵チェック！！

    while(digitalRead(cam_sw)==HIGH){
      step_cam_CW();
    }
    while(count<12){
      step_cam_CW();
      count++;
    }
  }
  step_cam_stop();
  delay(500);
}

/*gear(左右)を制御する関連*/
void step_gear_CCW(void){
  digitalWrite(step_gear_1, HIGH);
  digitalWrite(step_gear_2, HIGH);
  digitalWrite(step_gear_3, LOW);
  digitalWrite(step_gear_4, LOW);
  delay(gear_delay);
  
  digitalWrite(step_gear_1, LOW);
  digitalWrite(step_gear_2, HIGH);
  digitalWrite(step_gear_3, HIGH);
  digitalWrite(step_gear_4, LOW);
  delay(gear_delay);
  
  digitalWrite(step_gear_1, LOW);
  digitalWrite(step_gear_2, LOW);
  digitalWrite(step_gear_3, HIGH);
  digitalWrite(step_gear_4, HIGH);
  delay(gear_delay);
  
  digitalWrite(step_gear_1, HIGH);
  digitalWrite(step_gear_2, LOW);
  digitalWrite(step_gear_3, LOW);
  digitalWrite(step_gear_4, HIGH);
  delay(gear_delay);
}

void step_gear_CW(void){
  digitalWrite(step_gear_1, HIGH);
  digitalWrite(step_gear_2, LOW);
  digitalWrite(step_gear_3, LOW);
  digitalWrite(step_gear_4, HIGH);
  delay(gear_delay);

  digitalWrite(step_gear_1, LOW);
  digitalWrite(step_gear_2, LOW);
  digitalWrite(step_gear_3, HIGH);
  digitalWrite(step_gear_4, HIGH);
  delay(gear_delay);

  digitalWrite(step_gear_1, LOW);
  digitalWrite(step_gear_2, HIGH);
  digitalWrite(step_gear_3, HIGH);
  digitalWrite(step_gear_4, LOW);
  delay(gear_delay);

  digitalWrite(step_gear_1, HIGH);
  digitalWrite(step_gear_2, HIGH);
  digitalWrite(step_gear_3, LOW);
  digitalWrite(step_gear_4, LOW);
  delay(gear_delay);
}

void step_gear_stop(void){
  digitalWrite(step_gear_1, LOW);
  digitalWrite(step_gear_2, LOW);
  digitalWrite(step_gear_3, LOW);
  digitalWrite(step_gear_4, LOW);
}

void step_gear_reset(void){  //原点合わせ
  int count = 0;
  Serial.println("RESET!!");
  while(digitalRead(gear_sw)==LOW){
    step_gear_CW();
  }
  delay(500);
  Serial.println("Go To Origin");
  while(count<684){
    step_gear_CCW();
    count++;
  }
  step_gear_stop();
}

void step_gear(int select_lr){
  int count = 0;

  if(select_lr>0){  //右に移動
  Serial.println("step_gear_R");
    while(count<select_lr){
      step_gear_CW();
      count++;

      if (digitalRead(gear_sw) == HIGH){  //リミットスイッチに当たったら
        break;
      }
    }
  }

  else if(select_lr<0){  //左に移動
    Serial.println("step_gear_L");
    select_lr *= -1;
    while(count<select_lr){
      step_gear_CCW();
      count++;
    }
  }
  delay(500);
}

void check_key(int select_key){
  unsigned long start_time = millis();
  while(digitalRead(key_place_list[select_key][2]) == LOW){
    Serial.println("Checking_1");
    digitalWrite(key_place_list[select_key][3], HIGH);
    delay(25);
    digitalWrite(key_place_list[select_key][3], LOW);
    delay(25);
    if(millis()-start_time > 15000){  //15秒経過したら抜ける
      break;
    }
  }
  while(digitalRead(key_place_list[select_key][2]) == HIGH){
    Serial.println("Checking_2");
    digitalWrite(key_place_list[select_key][3], HIGH);
    delay(25);
    digitalWrite(key_place_list[select_key][3], LOW);
    delay(25);
  }
  delay(2000);
}

void setup(){
  Serial.begin(9600);
  Serial.println("Set Up");

  pinMode(step_cam_1, OUTPUT);
  pinMode(step_cam_2, OUTPUT);
  pinMode(step_cam_3, OUTPUT);
  pinMode(step_cam_4, OUTPUT);
  pinMode(step_gear_1, OUTPUT);
  pinMode(step_gear_2, OUTPUT);
  pinMode(step_gear_3, OUTPUT);
  pinMode(step_gear_4, OUTPUT);
  pinMode(cam_sw, INPUT);
  pinMode(gear_sw, INPUT);
  step_cam_stop();
  step_gear_stop();

  for (int i=1; i<13; i++){
    pinMode(key_place_list[i][2], INPUT);
  }
  for (int i=1; i<13; i++){
    pinMode(key_place_list[i][3], OUTPUT);
  }

  step_gear_reset();

  for (int i=1; i<13; i++){
    digitalWrite(key_place_list[i][3], HIGH);
    delay(50);
  }
  delay(500);
  for (int i=1; i<13; i++){
    digitalWrite(key_place_list[i][3], LOW);
    delay(50);
  }
}

void loop(){
  Serial.println("MAIN");

  int LR = 0, UD = 0, bike_number;
  unsigned long time_fin, time_d;

  bike_number = Serial.parseInt();
  Serial.println(bike_number);

  if(Serial.available()>0 && bike_number<13){

    LR = key_place_list[bike_number][0];
    UD = key_place_list[bike_number][1];
 
    Serial.println("");
    Serial.println(bike_number);

    step_gear(LR);  //左右の場所ぎめ

    step_cam(UD, bike_number);  //カムを回す

    LR *= -1;
    step_gear(LR);
    step_gear_stop();

    time_fin = millis();
  }

  time_d = millis() - time_fin;
  Serial.println(time_d);
  Serial.println("");

  if(60000<time_d && time_d<65000){  //約60秒経過したら原点合わせ
    step_gear_reset();
  }

  for (int i=1; i<13; i++){
    digitalWrite(key_place_list[i][3], HIGH);
    delay(10);
  }
  for (int i=1; i<13; i++){
    digitalWrite(key_place_list[i][3], LOW);
    delay(10);
  }
}