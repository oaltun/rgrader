# rgrader

`rgrader` consists of subcommands explained in later subsections.

You need `python 3.10` or more, and `hatch` installed.

To run the program, clone the repo, cd into `rgrader`, then issue one of

  * `hatch run rgrader merge xlsx  --help`
  * `hatch run rgrader grade ytu-exam-details-report --help`

The automatic help will tell you options, arguments, defaults, etc..


## grade

This subprogram can grade Yildiz Technical University online exams, using "Sınav Detay Raporu" (Exam Detail Report) xlsx file.

Grade calculation goes like 

`round(max(min(120*(p/e)-20*((t-a)/(z-a)), 100),0))` 

where `e` is the maximum possible raw points one can get from the exam, `p` is the students raw points, `a` is the start time of the exam, `z` is the end time of the exam, and `t` is the time student finishes the exam. This approach encourages student to finish the exam as soon as possible. This may prevent students waiting to learn solutions of questions before answering. 

Also, using `bad_questions`, you can cancel questions with mistakes. 

Only recent xlsx versions with question ids are supported.


## merge
This subcommand can merge xlsx documents based on a common column. Can help e.g. if exam results are on different files and you need to merge them based on student number. Needs polishing, e.g. the xlsx file must have clean format, etc. 

Dr. Oğuz Altun.