import sqlite3,os,json,sys,bcrypt
from datetime import datetime,timedelta
from openpyxl import Workbook
def password_hash(value):return bcrypt.hashpw(str(value).encode(),bcrypt.gensalt()).decode()
c=sqlite3.connect(os.getenv('DB_PATH','algorcher.db'))
c.executescript('''drop table if exists submissions;drop table if exists solved;drop table if exists course_problems;drop table if exists enrollments;drop table if exists student_faculties;drop table if exists faculty_courses;drop table if exists problems;drop table if exists courses;drop table if exists users;create table users(id integer primary key,name,email unique,password,role,reg_no,phone,year,dept,section,must_change_pw default 0);create table courses(id integer primary key,code unique,name);create table enrollments(student_id,course_id);create table student_faculties(student_id,faculty_id,unique(student_id,faculty_id));create table faculty_courses(faculty_id,course_id);create table course_problems(course_id,problem_id);create table problems(id integer primary key,title,difficulty,description,starter_code,points,samples,tests);create table solved(student_id,problem_id,course_id,points,solved);create table submissions(id integer primary key,student_id,problem_id,course_id,status,passed_tests,total_tests,runtime_ms,code,created_at);''')
c.execute("insert into users(name,email,password,role) values('Administrator','admin@college.edu',?,'admin')",(password_hash('Admin@123'),))
for code,name in [('PY101','Python Programming'),('DS201','Data Structures')]: c.execute('insert into courses(code,name) values(?,?)',(code,name))
for i in range(1,4): c.execute("insert into users(name,email,password,role,reg_no,dept,year,section) values(?,?,?,?,?,?,?,?)",(['Dr. Anil Sharma','Dr. Kavita Rao','Dr. Mehul Patel'][i-1],f'faculty{i}@college.edu',password_hash(f'F00{i}'),'faculty',f'F00{i}','CSE',2,'A'))
names=['Alice Joseph','Rahul Kumar','Priya Nair','Arjun Menon','Sneha Reddy','Vivek Shah','Ananya Iyer','Rohan Gupta','Kavya Rao','Aditya Singh','Meera Thomas','Karan Patel','Ishita Das','Nikhil Verma','Pooja Krishnan','Sanjay Joshi','Divya Kapoor','Aman Bhat','Neha Pillai','Varun Mehta']
for i in range(1,21):
 q=c.execute("insert into users(name,email,password,role,reg_no,year,dept,section) values(?,?,?,?,?,?,?,?)",(names[i-1],f'alice@college.edu' if i==1 else f's{i}@college.edu',password_hash(f'S{i:03d}'),'student',f'S{i:03d}',2,('CSE' if i<=12 else 'AIDS'),('A' if i<=6 or 13<=i<=16 else 'B'))); c.execute('insert into enrollments values(?,1)',(q.lastrowid,));c.execute('insert into enrollments values(?,2)',(q.lastrowid,))
D=[('Sum of Array','easy',10,'Read n then n integers. Print their sum. Input/Output: stdin/stdout. Constraints: 1<=n<=100000.','import sys\n# write your solution here\n',[('5\n1 2 3 4 5\n','15'),('3\n-2 0 7\n','5'),('1\n9\n','9'),('4\n-1 -2 -3 -4\n','-10')]),('Reverse a String','easy',10,'Read one string line and print it reversed. Input/Output: stdin/stdout. Constraints: length<=100000.','import sys\ns=sys.stdin.readline().rstrip("\\n")\n# write your solution here\n',[('hello\n','olleh'),('Algo Archer\n','rehcrA oglA'),('a\n','a'),('12345\n','54321')]),('Count Vowels','easy',10,'Count a,e,i,o,u case-insensitively. Input/Output: one line to one integer. Constraints: length<=100000.','import sys\ns=sys.stdin.readline().rstrip("\\n")\n# write your solution here\n',[('Hello World\n','3'),('AEIOU\n','5'),('xyz\n','0'),('aEi!\n','3')]),('Two Sum','medium',20,'Input n, array, target. Print smallest-first zero-based pair or -1 -1. Constraints: 2<=n<=100000.','import sys\ndata=sys.stdin.read().split()\n# write your solution here\n',[('4\n2 7 11 15\n9\n','0 1'),('3\n3 2 4\n6\n','1 2'),('2\n1 2\n10\n','-1 -1'),('2\n-1 1\n0\n','0 1')]),('Valid Parentheses','medium',20,'Input brackets ()[]{}. Print true if valid else false. Constraints: length<=100000.','import sys\ns=sys.stdin.readline().strip()\n# write your solution here\n',[('()[]{}\n','true'),('(]\n','false'),('([{}])\n','true'),('((\n','false')]),('Most Frequent Word','medium',20,'Input a line of words. Print most frequent lowercase word; alphabetical first on ties.','import sys\nwords=sys.stdin.readline().lower().split()\n# write your solution here\n',[('red blue red green\n','red'),('cat dog dog cat\n','cat'),('Apple apple pear\n','apple'),('z z a a\n','a')]),('Longest Substring Without Repeating Characters','hard',30,'Input one string. Print longest substring length. Constraints: length<=100000.','import sys\ns=sys.stdin.readline().rstrip("\\n")\n# write your solution here\n',[('abcabcbb\n','3'),('bbbbb\n','1'),('pwwkew\n','3'),('\n','0')]),('Merge Intervals','hard',30,'Input n then n start/end lines. Print merged intervals one per line. Constraints: n<=100000.','import sys\ndata=sys.stdin.read().split()\n# write your solution here\n',[('4\n1 3\n2 6\n8 10\n9 12\n','1 6\n8 12'),('2\n1 4\n5 6\n','1 4\n5 6'),('1\n0 0\n','0 0'),('0\n','')])]
for i,(t,d,p,desc,stub,cases) in enumerate(D,1):
 q=c.execute('insert into problems(title,difficulty,description,starter_code,points,samples,tests) values(?,?,?,?,?,?,?)',(t,d,desc,stub,p,json.dumps([{'input':a,'output':b} for a,b in cases[:2]]),json.dumps([{'input':a,'output':b} for a,b in cases])))
 if i<=5:c.execute('insert into course_problems values(?,?)',(1,q.lastrowid))
 if i>=4:c.execute('insert into course_problems values(?,?)',(2,q.lastrowid))
faculty_ids={x[0]:x[1] for x in c.execute("select reg_no,id from users where role='faculty'").fetchall()}
c.execute('insert into faculty_courses values(?,1)',(faculty_ids['F001'],));c.execute('insert into faculty_courses values(?,1)',(faculty_ids['F002'],));c.execute('insert into faculty_courses values(?,2)',(faculty_ids['F003'],))
for i in range(1,21):
 sid=c.execute("select id from users where role='student' and reg_no=?",(f'S{i:03d}',)).fetchone()[0]
 for faculty_reg,course_id in ((('F001' if i<=12 else 'F002'),1),('F003',2)):c.execute('insert into student_faculties values(?,?)',(sid,faculty_ids[faculty_reg]))
solutions={1:'n=int(input()); print(sum(map(int,input().split())))',2:'print(input().rstrip("\n")[::-1])',3:'print(sum(c.lower() in "aeiou" for c in input()))'}
names=['Alice Joseph', 'Rahul Kumar', 'Priya Nair', 'Arjun Menon', 'Sneha Reddy', 'Vivek Shah', 'Ananya Iyer', 'Rohan Gupta', 'Kavya Rao', 'Aditya Singh', 'Meera Thomas', 'Karan Patel', 'Ishita Das', 'Nikhil Verma', 'Pooja Krishnan', 'Sanjay Joshi', 'Divya Kapoor', 'Aman Bhat', 'Neha Pillai', 'Varun Mehta']
for i in range(1,21):
 solved=set([1,2,3,4,5] if i==1 else list(range(1,(i%6)+1)))
 for pid in solved:
  course=1 if pid<=3 else 2
  c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(i,pid,course,'WRONG_ANSWER',0,4,0,'print(0)',(datetime.now()-timedelta(days=45+pid)).isoformat()))
  day=2-(pid-1) if i==1 and pid in (1,2,3) else (pid*7+i)%55
  if i!=1: c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(i,pid,course,'ACCEPTED',4,4,10,solutions.get(pid,'print(0)'),(datetime.now()-timedelta(days=day)).isoformat()))
  c.execute('insert or ignore into solved values(?,?,?,?,?)',(i,pid,course,10,1))
c.execute("delete from submissions where student_id=5 and status='ACCEPTED'")
for pid in (1,2,3): c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(5,pid,1,'ACCEPTED',4,4,10,solutions.get(pid,'print(0)'),(datetime.now()-timedelta(days=(3-pid))).isoformat()))
for pid in (4,5): c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(5,pid,2,'ACCEPTED',4,4,10,solutions.get(pid,'print(0)'),datetime.now().isoformat()))
for pid in (4,): c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(5,pid,1,'ACCEPTED',4,4,10,solutions.get(pid,'print(0)'),datetime.now().isoformat()))
activity_dates=[72,68,64,61,58,54,51,47,44,39,35,31,27,23,19,15,12,9,6,5,4,3,2,1,0]
for sid in range(6,13):
 for n,days_ago in enumerate(activity_dates):
  if (sid+n)%4==0: continue
  pid=((sid+n)%5)+1; course=1 if pid<=3 else 2; status='WRONG_ANSWER' if (sid+n)%3 else 'ACCEPTED'; code=solutions.get(pid,'print(0)') if status=='ACCEPTED' else 'print(0)'
  c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(sid,pid,course,status,4 if status=='ACCEPTED' else 0,4,10,code,(datetime.now()-timedelta(days=days_ago,hours=(sid+n)%5)).isoformat()))
for n,days_ago in enumerate(activity_dates):
 pid=(n%5)+1; course=1 if pid<=3 else 2; status='ACCEPTED' if days_ago in (0,1,2) else 'WRONG_ANSWER'; code=solutions.get(pid,'print(0)') if status=='ACCEPTED' else 'print(0)'
 c.execute('insert into submissions values(null,?,?,?,?,?,?,?,?,?)',(5,pid,course,status,4 if status=='ACCEPTED' else 0,4,10,code,(datetime.now()-timedelta(days=days_ago,hours=n%3 )).isoformat()))
seed_faculty_ids=','.join(x[0] for x in c.execute("select reg_no from users where role='faculty' order by reg_no").fetchall())
student_faculty_ids=lambda i:'F001,F003' if i<=12 else 'F002,F003'
for fn,cols,items in [('sample_students.xlsx',['reg_no','name','year','dept','section','email','phone','courses','faculty_ids'],[(f'S{i:03d}',names[i-1],2,('CSE' if i<=12 else 'AIDS'),('A' if i<=6 or 13<=i<=16 else 'B'),'alice@college.edu' if i==1 else f's{i}@college.edu','', 'PY101,DS201',student_faculty_ids(i)) for i in range(1,21)]),('sample_faculty.xlsx',['Faculty_Id','Name','Department','Email','Mobile_Number'],[(fid,name,dept,email,mobile) for fid,name,dept,email,mobile in [('F001','Dr. Anil Sharma','CSE','faculty1@college.edu','9876543210'),('F002','Dr. Kavita Rao','AIDS','faculty2@college.edu','9876543211'),('F003','Dr. Mehul Patel','CSE/AIDS','faculty3@college.edu','9876543212')]])]:
 w=Workbook();w.active.append(cols)
 for item in items:w.active.append(item)
 w.save(fn)
c.commit();c.close();print('Seeded 8 real problems')












