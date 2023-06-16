# rgrader

This program can grade Yildiz Technical University online exams, using "Sınav Detay Raporu" (Exam Detail Report) xlsx file.

Grade calculation goes like round(max(min(120*(p/e)-20*((t-a)/(z-a)), 100),0)) where e is the maximum possible raw points one can get from the exam, p is the students raw points, a is the start time of the exam, z is the end time of the exam, and t is the time student finishes the exam. This approach encourages student to finish the exam as soon as possible. This may prevent students waiting to learn solutions of questions before answering. 

Also, using settings.bad_questions, you can cancel questions with mistakes. 

You need python 3.10 or more, and hatch installed.

To run the program, clone the repo, set the settings in src/rgrader/settings/__init.py (or set them as environment variables), cd into rgrader, then issue 

hatch run rgrader grade ytu-exam-details-report

Only recent xlsx versions with question ids are supported.

Dr. Oğuz Altun.