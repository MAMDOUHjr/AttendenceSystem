# Face Recognition Attendance System

![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.12.2-blue)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Introduction
This project is a Face Recognition Attendance System built with Python and integrated with Firebase for real-time data storage. It allows for efficient attendance tracking through facial recognition technology.

## Features
- Real-time face recognition
- Attendance logging in a Firebase database
- Easy to use interface
- Modular design for easy modifications and extensions

## Installation
 - Clone the repository:
   ```bash
   git clone https://github.com/your-username/face-recognition-attendance.git
   cd face-recognition-attendance'

## Usage
- To run the application, use the following command:
 ```bash
  python main.py
```
## Scripts
 - main.py: The main script that runs the application.
 - EncodeGenerator.py: Generates face encodings for new individuals and stores them in a file.
 - AddDataToDataBase.py: Adds user data to the Firebase database.

## Project Structure

   face-recognition-attendance/
 - │
 - ├── Resources/           
 - ├── EncodeFile.p         
 - ├── serviceAccount.json  
 - ├── main.py              
 - ├── EncodeGenerator.py   
 - ├── AddDataToDataBase.py 
 - ├── requirements.txt    
 - └── README.md            

  
## Contributing
 Contributions are welcome! Please follow these steps:

 - Fork the repository.
 - Create a new branch ```git checkout -b feature-branch```
 - Make your changes and commit ```git commit -m 'Add new feature'```
 - Push to the branch ```git push origin feature-branch```.
 - Open a Pull Request.


