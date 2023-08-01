#include "Arduino.h"
#include "config.h"
#include <AFMotor.h>

AF_DCMotor motor1(1); // The motor number, i.e. 1, 2, 3 or 4
AF_DCMotor motor2(2); // The motor number, i.e. 1, 2, 3 or 4
AF_DCMotor motor3(3); // The motor number, i.e. 1, 2, 3 or 4
AF_DCMotor motor4(4); // The motor number, i.e. 1, 2, 3 or 4

char a[5] = {'H', 'e', 'l', 'l', 'o'};
char b[5] = {'H', 'i', ' ', 'P', 'i'};
char test;
int forward_speed = 100;
int backward_speed = 100;
int turn_left_speed[4] = {80, 60, 140, 160};
int turn_right_speed[4] = {160, 140, 60, 80};
int Turn_Left_speed[4] = {255, 255, 255, 255};
int Turn_Right_speed[4] = {255, 255, 255, 255};

// void quickspeed_set()
// {
//   motor1.setSpeed( 255 );
//   motor2.setSpeed( 255 );
//   motor3.setSpeed( 255 );
//   motor4.setSpeed( 255 );
// }

// void slowspeed_set()
// {
//   motor1.setSpeed( 100 );
//   motor2.setSpeed( 100 );
//   motor3.setSpeed( 100 );
//   motor4.setSpeed( 100 );
// }

void go_straight()
{
  motor1.setSpeed(forward_speed);
  motor2.setSpeed(forward_speed);
  motor3.setSpeed(backward_speed);
  motor4.setSpeed(backward_speed);

  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);

  Serial.print(1);
  Serial.print('\n');
}

void go_back()
{
  motor1.setSpeed(backward_speed);
  motor2.setSpeed(backward_speed);
  motor3.setSpeed(forward_speed);
  motor4.setSpeed(forward_speed);

  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void turn_right()
{
  motor1.setSpeed(turn_right_speed[0]);
  motor2.setSpeed(turn_right_speed[1]);
  motor3.setSpeed(turn_right_speed[2]);
  motor4.setSpeed(turn_right_speed[3]);

  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void turn_left()
{
  motor1.setSpeed(turn_left_speed[0]);
  motor2.setSpeed(turn_left_speed[1]);
  motor3.setSpeed(turn_left_speed[2]);
  motor4.setSpeed(turn_left_speed[3]);

  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void Turn_Left()
{
  motor1.setSpeed(Turn_Left_speed[0]);
  motor2.setSpeed(Turn_Left_speed[1]);
  motor3.setSpeed(Turn_Left_speed[2]);
  motor4.setSpeed(Turn_Left_speed[3]);

  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}
void Turn_Right()
{
  motor1.setSpeed(Turn_Right_speed[0]);
  motor2.setSpeed(Turn_Right_speed[1]);
  motor3.setSpeed(Turn_Right_speed[2]);
  motor4.setSpeed(Turn_Right_speed[3]);

  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void stop()
{
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  // delay(5000);
}

void control(char *command)
{
  if (command[0] == 'M')
{
  // 获取电机编号
  int motorNumber = command[1] - '0';
  // 获取方向标识符
  char direction = command[2];
  // 获取速度值
  int speed = atoi(command + 3);
  
  if (speed > 255) {
    speed = 255;
  } else if (speed < 0) {
    speed = 0;
  }

  // 根据电机编号和方向，设置相应的速度
  switch (motorNumber)
  {
  case 0:
    if (direction == 'F') {
      forward_speed = speed;
    } else if (direction == 'L') {
      Turn_Left_speed[0] = speed;
    } else if (direction == 'R') {
      Turn_Right_speed[0] = speed;
    }else if (direction == 'l') {
      turn_left_speed[0] = speed;
    } else if (direction == 'r') {
      turn_right_speed[0] = speed;
    }
    break;

  case 1:
    if (direction == 'F') {
      forward_speed = speed;
    } else if (direction == 'L') {
      Turn_Left_speed[1] = speed;
    } else if (direction == 'R') {
      Turn_Right_speed[1] = speed;
    }else if (direction == 'l') {
      turn_left_speed[1] = speed;
    } else if (direction == 'r') {
      turn_right_speed[1] = speed;
    }
    break;

  case 2:
    if (direction == 'F') {
      backward_speed = speed;
    }  else if (direction == 'L') {
      Turn_Left_speed[2] = speed;
    } else if (direction == 'R') {
      Turn_Right_speed[2] = speed;
    }else if (direction == 'l') {
      turn_left_speed[2] = speed;
    } else if (direction == 'r') {
      turn_right_speed[2] = speed;
    }
    break;

  case 3:

    if (direction == 'F') {
      backward_speed = speed;
    } else if (direction == 'L') {
      Turn_Left_speed[3] = speed;
    } else if (direction == 'R') {
      Turn_Right_speed[3] = speed;
    }else if (direction == 'l') {
      turn_left_speed[3] = speed;
    } else if (direction == 'r') {
      turn_right_speed[3] = speed;
    }
    break;

  default:
    // 错误的电机编号
    Serial.println("错误的电机编号");
    break;
  }
}
  else if (command[0] == 'h')
  {
    for (int i = 0; i < 5; i++)
    {
      int x = a[i];
      int y = b[i];
      Serial.write(x);
      Serial3.write(y);
    }
  }
  else
  {
    switch (command[0])
    {
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