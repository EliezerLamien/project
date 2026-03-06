from flask import Flask, request, render_template_string

app = Flask(__name__)
students = {}

HTML = """
<h2>Course Management</h2>
<form method="post" action="/add_student">
  <input name="student" placeholder="Student name">
  <button>Add Student</button>
</form>

<form method="post" action="/add_course">
  <input name="student" placeholder="Student name">
  <input name="course" placeholder="Course">
  <button>Add Course</button>
</form>

<h3>Students</h3>
<pre>{{students}}</pre>
"""

@app.get("/")
def home():
    return render_template_string(HTML, students=students)

@app.post("/add_student")
def add_student():
    s = request.form["student"].strip()
    students.setdefault(s, [])
    return home()

@app.post("/add_course")
def add_course():
    s = request.form["student"].strip()
    c = request.form["course"].strip()
    if s in students and c and c not in students[s]:
        students[s].append(c)
    return home()

if __name__ == "__main__":
    app.run(debug=True)
