![CDD](https://en.smartautoscan.com/comdata/69843/202401/20240102152404bbfee4.png)

<!-- Repo badges -->
![GitHub stars](https://img.shields.io/github/stars/yasharzavary/car_damage_system?style=flat-square&color=yellow)
![GitHub forks](https://img.shields.io/github/forks/yasharzavary/car_damage_system?style=flat-square&color=blue)
![GitHub issues](https://img.shields.io/github/issues/yasharzavary/car_damage_system?style=flat-square&color=red)
![GitHub last commit](https://img.shields.io/github/last-commit/yasharzavary/car_damage_system?style=flat-square&color=green)
![GitHub repo size](https://img.shields.io/github/repo-size/yasharzavary/car_damage_system?style=flat-square)

<!-- Project / tech stack badges -->
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Inference%20Server-black?style=flat-square&logo=flask&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-C51A4A?style=flat-square&logo=raspberry-pi&logoColor=white)
![Proteus](https://img.shields.io/badge/Proteus-VSM%209-0078D7?style=flat-square&logo=data:image/png;base64,)
![Platform](https://img.shields.io/badge/Platform-Embedded%20System-orange?style=flat-square)

<!-- Project status / type badges -->
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)
![License](https://img.shields.io/github/license/yasharzavary/car_damage_system?style=flat-square)
![Language](https://img.shields.io/github/languages/top/yasharzavary/car_damage_system?style=flat-square)

⭐ Star on GitHub — your support motivates us a lot! 🙏😊

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow-blue?logo=linkedin)](https://www.linkedin.com/in/yashar-zavary-rezaie/)
[![Telegram](https://img.shields.io/badge/Telegram-Join-blue?logo=telegram)](https://t.me/YZR_Computer)


## Table of Contents
1. Introduction
2. Architecture
3. How to use
4. Notes

## 🚀 Introduction
sometimes the cars that park in parking(public or etc.) damaged and after moved, they don't know where it happen! this system is for this purpose, where you want to go parking, it will detect it and take photos from fron and rear and save the damaged in the memory, when you want to go out from parking, it will take pictures again and check the damages, if it have new damages it will notify the security that this car have new damages and you can notify it.

## Architecture
this project is maded by Rasberry PI board simulation in proteus and it can be deploy on boards and used in the real work parkings!
the codes is created by Python.

the image process system is writed by Torch that is run on one server and our board can communicate with it(so you can use this image process in ESP32 or other non-wiered systems)


## How to use
1. clone the project
DO: write clone code

2. open project with proteus

3. change locations settings in 4 file:
- rasberry PI codes(3 file)
- car damage detection file
NOTE: you should do this because proteus can't work with location as a normal locations!

4. run the project in proteus

5. add photos in income section and make HIGH the CAR_IN pin, this will move your files into one location(for now it is 0, in next update we will add licence plate detection), now you can see images go to images folder in data and income folder is empty!

6. now again add images into the income section and hit CAR_OUT, this mean the car is go out, it will check the income images and previous IN images and if it have new damages, the buzzer will sound and the LCD show the result!

7. for exiting the project, first of all make HIGH the STOP logicstate and after seeing "system stop" on LCD, stop the simulation! if you don't do this, the damage detection python file will run in the background!!

## Notes
- the project work just with one type car! in next update it will have licence detection and we can work and handle different cars in and out

- proteus simulation can't handle torch library for rasberry PI, for this we use it outside of code and make connection with "car damage detection" file! if you want to deploy this project one a real-life board, you can add this code into the rasberry PI and run it!

- you can deploy this image process on a ESP32 and connect to image process no-wiered system!


## Contributions & Feedback

Suggestions, improvements, and code reviews are always welcome.  
Feel free to open an issue, submit a pull request, or contact me directly through the platforms below.

[![Telegram](https://img.shields.io/badge/Telegram-Contact-blue?logo=telegram)](https://t.me/YZR_Computer)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/yashar-zavary-rezaie/)

