from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    context = {"name": "Интернет магазин Домашняя Работа"}
    return render_template("bases.html", **context)

@app.route("/clothes/")
def clothes():
    _list_clothes = [{"name" : "Майка", "price": "35", "amount": "1123"},
                     {"name" : "Шорты", "price": "40", "amount": "729"},
                     {"name" : "Кофта", "price": "55", "amount": "371"}]
    context = {"title": "Одежда", "clothes": _list_clothes}
    return render_template("clothes.html", **context)

@app.route("/shoes/")
def shoes():
    _list_shoes = [{"name" : "Туфли", "price": "75", "amount": "376"},
                     {"name" : "Кеды", "price": "64", "amount": "427"},
                     {"name" : "Кроссовки", "price": "81", "amount": "71"}]
    context = {"title": "Обувь", "shoes": _list_shoes}
    return render_template("shoes.html", **context)

@app.route("/techics/")
def techies():
    _list_techics = [{"name" : "Телефон", "price": "375", "amount": "176"},
                     {"name" : "Ноутбук", "price": "1564", "amount": "427"},
                     {"name" : "Телевизор", "price": "981", "amount": "71"}]
    context = {"title": "Техника", "techics": _list_techics}
    return render_template("techics.html", **context)

if __name__ == "__main__":
    app.run(debug=True)