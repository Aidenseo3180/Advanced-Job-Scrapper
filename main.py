from flask import Flask, render_template, request, redirect,send_file
from scrapper import get_SO_jobs
from exporter import save_to_file


app = Flask("JobScrapper")

db = {}  #fake db, 여기에 우리가 정보들을 저장할거임
#문제는 프로그램을 끄면 다 날아감 OTL
#db = {'vuejs' : [많은 직업들]} <- 이런 식으로 저장됨


@app.route("/")
def home():
  return render_template("home.html")


@app.route("/report")
def go_report():
  word = request.args.get('word')
  if word:  #if word exists (not null bc can't make null.lower())
    word = word.lower()
    existingJobs = db.get(word)  #db에서 word를 얻어옴
    #word가 이미 있는지 뒤져보는거
    #없으면 None이 fromDb로 들어감

      #if (True)
    if existingJobs:  #만약 이 fake db에 정보가 이미 있으면(word가 존재)
      jobs = existingJobs  #fromDb에 있던것들을 jobs에 넣음
    else:  #만약 없으면
      jobs = get_SO_jobs(word)  #얻어옴
      db[word] = jobs

  else:  #만약 존재하지 않으면 home으로 redirect
      return redirect("/")

  return render_template(
    "report.html", 
    search=word, 
    resultNum=len(jobs),
    job=jobs)
  #변수 word를 search라는 이름으로 넘겨줌
  #그리고 jobs의 길이를 resultNum에게 보냄
  #그리고 jobs도 다 보냄

@app.route("/export")
def export():
  try:
    word = request.args.get("word") #word가 url에 있는지 체크
    if not word:  #없으면 exception이 나옴
      raise Exception()
    word = word.lower() #소문자
    jobs = db.get(word) #db에서 word를 찾아서 jobs에 넣음
    if not jobs:  #만약 word를 못찾으면
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv", attachment_filename='all_jobs.csv', as_attachment=True)
    #저장할 파일이름 : attachment_filename을 바꾸면 우리가 원하는 이름으로 바꿔줌

  except:
    redirect("/") #에러를 잡고, home으로 돌아감


app.run(host="0.0.0.0")
