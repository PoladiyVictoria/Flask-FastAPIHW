from flask import Flask, render_template, request, make_response, url_for,redirect

app = Flask(__name__)
app.secret_key = '362565f48a6b78e11f491290087ce9d9818d26c9418df7db8c6380565ed50549'
'''
Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет создан cookie-файл с данными пользователя,
а также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными пользователя 
и произведено перенаправление на страницу ввода имени и электронной почты.
'''
@app.route("/", methods=["GET", "POST"])
def index():
    context = {"title": "Главная страница"}
    if request.method == "POST":
        context = {"title": "Страница Входа"}
        return redirect(url_for("login")) 
    return render_template("index.html", **context)

@app.route("/login/", methods=["GET", "POST"])
def login():
    context = {"title": "Страница Входа"}
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        context["name"] = name
        response = make_response(redirect(url_for("hello")))
        response.set_cookie("username", name)
        response.set_cookie("usermail", email)
        return response
    return render_template("login.html", **context)

@app.route("/hello/", methods=["GET", "POST"])
def hello():
    name = request.cookies.get('username')
    context = {"title": "Приветствие" , "name": name}
    if request.method == "POST":
        response = make_response(redirect(url_for("index")))
        response.delete_cookie("username")
        response.delete_cookie("usermail")
        return response
    return render_template("hello.html", **context)

if __name__ == "__main__":
    app.run(debug=True)