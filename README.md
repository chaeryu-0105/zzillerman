# Boss Fight Game

간단한 2D 보스전 액션 게임. 플레이어는 제한된 공간에서 보스의 공격을 피하고, 공격 타이밍을 잡아 체력을 깎아 승리해야 한다. 보스는 총 여섯 가지 패턴을 번갈아 사용하며 주요 패턴들에선 패턴의 전조와 사운드가 존재하며, 이를 인지하면 피하기 쉬워진다.

---

## 📌 주요 특징

* **두 가지 종류의 주요 보스 패턴 구현**
* **모든 공격에 사운드 적용**
* **플레이어의 직접 조작 기반 근접전 디자인(WASD 이동 + 마우스 공격)**

---

## ▶ 실행 방법

### 요구사항

* Python 3.x
* pygame

### 설치

```bash
pip install pygame
```

### 실행

```bash
python main.py
```

---

## 🎮 조작 방법

| 행동     | 입력                                     |
| ------ | -------------------------------------- |
| 이동     | **W, A, S, D**                         |
| 공격     | **마우스 왼쪽 버튼**                          |
| 게임 재시작 | 게임 오버 후 1.2초 뒤에 **아무 키 또는 마우스 입력** |

---

## ⚔ 게임 시스템 설명

### ● 플레이어

* 일정 거리 내 보스를 공격 가능.
* 체력이 0이 되면 종료.

### ● 보스
* 보스에게 근접하면 플레이어 체력이 주기적으로 감소

* **패턴 1: 총알 공격**
  플레이어가 있는 방향으로 총알을 한발 발사

* **패턴 2: 여러 발 공격**
  플레이어가 있는 방향으로 총알을 세 발 발사

* **패턴 3: 부채꼴 공격**
  플레이어가 있는 방향으로 부채꼴 모양 위험구역을 예고하고 일정 시간 이후 공격

* **패턴 4: 도넛 공격**
  보스 주변에 도넛 모양의 위험 구역을 예고 하고 일정 시간 이후 공격

* **패턴 5: 위험 구역**
  플레이어 주변에 주황색 원형 위험구역을 예고하고 일정 시간 이후 공격

* **패턴 6: 돌진 공격**
  돌진 할 방향(플레이어가 있는 곳)을 미리 위험구역으로 예고하고 일정시간 이후 돌진


### ● 게임 흐름

1. 보스전 시작 → BGM 재생
2. 플레이어/보스 전투 진행
3. 보스 체력 0 → **Victory 화면**, `victory.mp3` 재생
4. 플레이어 체력 0 → **Game Over 화면**
5. 1.2초 대기 → 키보드/마우스 입력 시 **자동으로 보스전 재시작 + BGM 재시작**

---

## 사운드 리소스 출처

### **sword_swing.wav**

* Author: gronnie
* Source: https://freesound.org/s/563171/
* License: Creative Commons Attribution 4.0 (CC BY 4.0)


### **boss_attack.wav**

* Author: Joao_Janz
* Source: https://freesound.org/s/478278/
* License: Creative Commons 0 (CC0)


### **before_attack.wav**

* Author: high_festiva
* Source: https://freesound.org/s/194439/
* License: Creative Commons 0 (CC0)


### **victory.mp3**

* Author: FunWithSound
* Source: https://freesound.org/s/456966/
* License: Creative Commons 0 (CC0)
  

### **bgm.mp3**

* Author: DJARTMUSIC
* Source: https://pixabay.com/ko/music/%eb%b9%84%eb%94%94%ec%98%a4-%ea%b2%8c%ec%9e%84-best-game-console-301284/
* License: Pixabay Content License (Free for commercial and non-commercial use, no attribution required)



## 파일 구성

```
project/
 ├─ main.py       # 게임 실행 및 전체 로직
 ├─ images/       # 플레이어/보스 스프라이트
 ├─ sounds/       # BGM 및 효과음
 ├─ README.md
```

---

## 추가 개발 가능 요소

* 보스 추가
* UI 개선 (체력바, 쿨타임 표시 등)
* 더 다양한 플레이어 무기/스킬