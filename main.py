from flask import Flask, render_template, request, redirect,send_file
from scrapper import get_SO_jobs
from exporter import save_to_file


app = Flask("JobScrapper")

db = {} 
@app.route("/")
def home():
  return render_template("home.html")


@app.route("/report")
def go_report():
  word = request.args.get('word')
  if word:  #if word exists (not null bc can't make null.lower())
    word = word.lower()
    existingJobs = db.get(word)  
   
      #if (True)
    if existingJobs: 
      jobs = existingJobs 
    else:  
      jobs = get_SO_jobs(word) 
      db[word] = jobs

  else: 
      return redirect("/")

  return render_template(
    "report.html", 
    search=word, 
    resultNum=len(jobs),
    job=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:  
      raise Exception()
    word = word.lower() 
    jobs = db.get(word)
    if not jobs:  
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv", attachment_filename='all_jobs.csv', as_attachment=True)

  except:
    redirect("/") 


app.run(host="0.0.0.0")
