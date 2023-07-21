#include "Arduino.h"
#include "config.h"
#include <AFMotor.h>
  
  AF_DCMotor motor1(1);  // The motor number, i.e. 1, 2, 3 or 4
  AF_DCMotor motor2(2);  // The motor number, i.e. 1, 2, 3 or 4  
  AF_DCMotor motor3(3);  // The motor number, i.e. 1, 2, 3 or 4
  AF_DCMotor motor4(4);  // The motor number, i.e. 1, 2, 3 or 4

  char a[5] = {'H','e','l','l','o'};
  char b[5]={'H','i',' ','P','i'};
  char test;




  void quickspeed_set()
  {
    motor1.setSpeed( 255 );
    motor2.setSpeed( 255 );
    motor3.setSpeed( 255 );
    motor4.setSpeed( 255 );
  }

  void slowspeed_set()
  {
    motor1.setSpeed( 100 );
    motor2.setSpeed( 100 );
    motor3.setSpeed( 100 );
    motor4.setSpeed( 100 );
  }

  

  void go_straight()
  {
    slowspeed_set();
    motor1.run( FORWARD );
    motor2.run( FORWARD );
    motor3.run( BACKWARD );
    motor4.run( BACKWARD );
    Serial.print(1);
      Serial.print('\n');
  }

  void go_back()
  {
    slowspeed_set();
    motor1.run( BACKWARD );
    motor2.run( BACKWARD );
    motor3.run( FORWARD );
    motor4.run( FORWARD );
  }

  void turn_right()
  {
    motor1.setSpeed( 160 );
    motor2.setSpeed( 140 );
    motor3.setSpeed( 60 );
    motor4.setSpeed( 80 );
    motor1.run( FORWARD );
    motor2.run( FORWARD );
     motor3.run( BACKWARD );
     motor4.run( BACKWARD );
  }

  void turn_left()
  {
    motor1.setSpeed( 80 );
    motor2.setSpeed( 60 );
    motor3.setSpeed( 140 );
    motor4.setSpeed( 160 );
     motor1.run( FORWARD );
    motor2.run( FORWARD );
     motor3.run( BACKWARD );
     motor4.run( BACKWARD );
  }

  void Turn_Left()
  {
    quickspeed_set();
    motor1.run( BACKWARD );
    motor2.run( BACKWARD );
    motor3.run( BACKWARD );
    motor4.run( BACKWARD );
  }

  void Turn_Right()
  {
    quickspeed_set();
    motor1.run( FORWARD );
    motor2.run( FORWARD );
    motor3.run( FORWARD );
    motor4.run( FORWARD );
  }

  void stop()
  {
    motor1.run( RELEASE );
    motor2.run( RELEASE );
    motor3.run( RELEASE );
    motor4.run( RELEASE );
    // delay(5000);
  }

  void control(char* command) {
    // 判断命令是否是设置速度命令
    if (command[0] == 'M' && command[2] == 'S') {
        // 获取电机编号
        int motorNumber = command[1] - '0';
        // 获取速度值
        int speed = atoi(command + 3);
        // 根据电机编号，设置相应的速度
        switch (motorNumber) {
            case 1:
                motor1.setSpeed(speed);
                break;
            case 2:
                motor2.setSpeed(speed);
                break;
            case 3:
                motor3.setSpeed(speed);
                break;
            case 4:
                motor4.setSpeed(speed);
                break;
            default:
                // 错误的电机编号
                Serial.println("错误的电机编号");
                break;
        }
    }
    else if (command[0] == 'h'){
      for(int i=0;i<5;i++){
        int x = a[i];
        int y = b[i];
        Serial.write(x);
        Serial3.write(y);
      }
    }
    else {
        switch (command[0]) {
            case 'q':
                Turn_Left();
                break;
            case 'e':
                Turn_Right();
                break;
            case 'w':
                go_straight();
                break;
            case 'a':
                turn_left();
                break;
            case 's':
                go_back();
                break;
            case 'd':
                turn_right();
                break;
            case 'm':
            case 'A':
            case 'W':
            case 'S':
            case 'D':
                stop();
                break;
            default:
                Serial.println("无效的命令");
                break;
        }
    }
}