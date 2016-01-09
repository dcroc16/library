
# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request, redirect
import requests
import json
import os
import sqlite3


class Library:

    def __init__(self):
        self.upc_list = []
        self.API_KEY = os.environ['KEY']

    def get_upc(self, upc):
        self.upc_list.append(upc)

    def lookup_upc(self, upc, db_name):
        outpan_path = "https://api.outpan.com/v2/products/" + upc + "?apikey=" + self.API_KEY
        print(outpan_path)
        response = requests.get(outpan_path)
        print(response.text)
        response = json.loads(response.text)

        title = None
        if 'name' in response:
            title = response['name']
        if 'images' in response:
            image_link = ''
            if len(response['images']) > 0:
                image_link = response['images'][0]
        if 'attributes' in response:
            author = ''
            book_format = ''
            isbn_10 = ''
            publish_date = ''
            publisher = ''
            page_count = ''
            if 'Author(s)' in response['attributes']:
                author = response['attributes']['Author(s)']
            if 'Format' in response['attributes']:
                book_format = response['attributes']['Format']
            if 'ISBN-10' in response['attributes']:
                isbn_10 = response['attributes']['ISBN-10']
            if 'Publication Date' in response:
                publish_date = str(response['attributes']['Publication Date'])
            if 'Publisher' in response['attributes']:
                publisher = response['attributes']['Publisher']
            if 'Page Count' in response['attributes']:
                page_count = response['attributes']['Page Count']

        if title:
            self.add_book(title, author, isbn_10, image_link, publish_date, publisher, page_count, book_format, db_name)
            self.view_books()
            return [title, author, isbn_10, image_link, publish_date, publisher, page_count, book_format]
        else:
            print("Not Found")
            return ["Not Found","","","","","","",""]

    def list_upcs(self):
        for i in self.upc_list:
            print(i)

    def add_book(self, title, author, isbn_10, image_link, publish_date, publisher, page_count, book_format, db_name):
        if db_name == 'lexi':
            dbc = sqlite3.connect('library.db')
        elif db_name == 'abby':
            dbc = sqlite3.connect('library_abby.db')
        c = dbc.cursor()
        c.execute('''
        insert into books(title,author,format,isbn_10,page_count,publish_date,publisher,image_link)
        values (?,?,?,?,?,?,?,?)
        ''', (title, author, book_format, isbn_10, page_count, publish_date, publisher, image_link))
        dbc.commit()
        dbc.close()

    def view_books(self):
        dbc = sqlite3.connect('library.db')
        c = dbc.cursor()
        c.execute('''select * from books''' )
        for i in c.fetchall():
            print(i)

        dbc.close()


app = Flask(__name__)


@app.route('/')
def home():
    dbc = sqlite3.connect('library.db')
    c = dbc.cursor()
    c.execute("select * from books where available=? order by title;",('Y',))
    book_data = c.fetchall()
    c.execute('''select * from books order by id desc limit 1''')
    current_book_data = c.fetchone()
    c.execute("select * from books where available=? order by title;",('N',))
    checked_out_books = c.fetchall()
    c.execute('''select count(*) from books where image_link != "" ''')
    count_books = c.fetchone()[0]
    c.execute('''select count(*) from books where image_link = "" ''')
    count_books_no_pic = c.fetchone()[0]
    c.execute(''' select count(*) from books; ''')
    total_books = c.fetchone()[0]
    dbc.close()
    return render_template('index.html', msg='', bookData=book_data,
                                         checkedOutBooks=checked_out_books,
                                         getPassword=False,
                                         currentBook=current_book_data,
                                         count_of_books=count_books,
                                         count_books_no_pic=count_books_no_pic,
                                         total_books = total_books)

@app.route('/GetPassword', methods=['POST'])
def getPassword():
    current_book_id = request.form['deleteID']
    dbc = sqlite3.connect('library.db')
    c = dbc.cursor()
    c.execute('''select * from books order by title;''')
    book_data = c.fetchall()

    c.execute('select * from books where id="' + str(current_book_id) + '";')
    current_book_data = c.fetchone()
    dbc.close()
    return render_template('index.html',
                        msg = '',
                        bookData=book_data,
                        getPassword=True,
                        currentBook=current_book_data)


@app.route('/CheckOutBook', methods=['POST'])
def checkOutBook():
    current_book_id = request.form['checkOut']
    borrower = request.form['bName']
    dbc = sqlite3.connect('library.db')
    c = dbc.cursor()
    c.execute('''update books SET available=? where id=?''',('N',str(current_book_id)))
    dbc.commit()
    c.execute('''update books SET borrower=? where id=?''',(borrower,str(current_book_id)))
    dbc.commit()
    dbc.close()
    return redirect('/', code=302)

@app.route('/CheckIn', methods=['POST'])
def checkInBook():
    current_book_id = request.form['checkIn']
    dbc = sqlite3.connect('library.db')
    c = dbc.cursor()
    c.execute('''update books SET available=? where id=?''',('Y',str(current_book_id)))
    dbc.commit()
    c.execute('''update books SET borrower=? where id=?''',('',str(current_book_id)))
    dbc.commit()
    dbc.close()
    return redirect('/', code=302)


@app.route('/EnterBook')
def newbook():
    dbc = sqlite3.connect('library.db')
    c = dbc.cursor()
    c.execute('''select * from books order by title;''')
    book_data = c.fetchall()
    dbc.close()
    return render_template('index.html', msg='', bookData=book_data, enterNewBook=True,
                            currentBook=('','','','','','','',''))


@app.route('/SubmitNewBook', methods=['POST'])
def submitnewbook():
    isbn = request.form['ISBN']
    l = Library()
    new_book_data = l.lookup_upc(isbn, 'lexi')
    if new_book_data[0] != 'Not Found':
        return redirect('/', code=302)
    else:
        dbc = sqlite3.connect('library.db')
        c = dbc.cursor()
        c.execute('''select * from books order by title;''')
        book_data = c.fetchall()
        c.execute('''select * from books order by id desc''')
        current_book_data = c.fetchone()
        dbc.close()
        msg = 'Not Found'
        return render_template('index.html', msg=msg, bookData=book_data, getPassword=False, currentBook=current_book_data)


@app.route('/RemoveBook', methods=['POST'])
def removebook():
    if request.form['password'] == os.environ['DELETE_PASSWORD']:
        dbc = sqlite3.connect('library.db')
        c = dbc.cursor()
        book_id = request.form['bID']
        c.execute('delete from books where id=' + str(book_id) + ';')
        dbc.commit()
        dbc.close()
    return redirect("/", code=302)


########################################### ABBY'S PART #################

@app.route('/Abby')
def homeAbby():
    dbc = sqlite3.connect('library_abby.db')
    c = dbc.cursor()
    c.execute('''select * from books order by title;''')
    book_data = c.fetchall()
    c.execute('''select * from books order by id desc''')
    current_book_data = c.fetchone
    c.execute('''select count(*) from books where image_link != "" ''')
    count_books = c.fetchone()[0]
    c.execute('''select count(*) from books where image_link = "" ''')
    count_books_no_pic = c.fetchone()[0]
    c.execute(''' select count(*) from books; ''')
    total_books = c.fetchone()[0]
    dbc.close()
    return render_template('index_abby.html', msg='',
                                         bookData=book_data,
                                         getPassword=False,
                                         currentBook=current_book_data,
                                         count_of_books=count_books,
                                         count_books_no_pic=count_books_no_pic,
                                         total_books = total_books)

@app.route('/GetPasswordAbby', methods=['POST'])
def getPasswordAbby():
    current_book_id = request.form['deleteID']
    dbc = sqlite3.connect('library_abby.db')
    c = dbc.cursor()
    c.execute('''select * from books order by title;''')
    book_data = c.fetchall()

    c.execute('select * from books where id="' + str(current_book_id) + '";')
    current_book_data = c.fetchone()
    dbc.close()
    return render_template('index_abby.html',
                        msg = '',
                        bookData=book_data,
                        getPassword=True,
                        currentBook=current_book_data)


@app.route('/EnterBookAbby')
def newbookAbby():
    dbc = sqlite3.connect('library_abby.db')
    c = dbc.cursor()
    c.execute('''select * from books order by title;''')
    book_data = c.fetchall()
    dbc.close()
    return render_template('index_abby.html', msg='', bookData=book_data, enterNewBook=True,
                            currentBook=('','','','','','','',''))


@app.route('/SubmitNewBookAbby', methods=['POST'])
def submitnewbookAbby():
    isbn = request.form['ISBN']
    l = Library()
    new_book_data = l.lookup_upc(isbn, 'abby')
    if new_book_data[0] != 'Not Found':
        return redirect('/Abby', code=302)
    else:
        dbc = sqlite3.connect('library_abby.db')
        c = dbc.cursor()
        c.execute('''select * from books order by title;''')
        book_data = c.fetchall()
        c.execute('''select * from books order by id desc''')
        current_book_data = c.fetchone()
        dbc.close()
        msg = 'Not Found'
        return render_template('index_abby.html', msg=msg, bookData=book_data, getPassword=False, currentBook=current_book_data)


@app.route('/RemoveBookAbby', methods=['POST'])
def removebookAbby():
    if request.form['password'] == os.environ['DELETE_PASSWORD_ABBY']:
        dbc = sqlite3.connect('library_abby.db')
        c = dbc.cursor()
        book_id = request.form['bID']
        c.execute('delete from books where id=' + str(book_id) + ';')
        dbc.commit()
        dbc.close()
    return redirect("/Abby", code=302)



##########################################################################

@app.route('/OldHome')
def OldHome():
    KEY = os.environ['KEY']
    db = sqlite3.connect('testdb.db')
    c = db.cursor()
    c.execute(''' insert into user (name) values ('david')''')
    db.commit()
    c.execute('''select * from user''')

    data = c.fetchall()

    db.close()

    return render_template('new_home.html', key=KEY, data=data)

@app.route('/lexi')
def Lexi():
    return render_template('lexi.com.html',User='David')

@app.route('/AllAboutMe')
def aam():
    return render_template('AllAboutMe.html',words1='This is a story about Lexi', words2='she loves to play all day')

@app.route('/MakeYourOwnTree')
def myot():
    return render_template('tree.html')

@app.route('/MakeYourOwnPumpkin')
def myop():
    return render_template('pumpkin.html')

@app.route('/PutMakeupOnMe')
def pmom():
    return render_template('makeup.html')

@app.route('/DressUp')
def du():
    return render_template('dressUp.html')

@app.route('/Music')
def music():
    return render_template('music.html')


@app.route('/calc')
def Calc():
    return render_template('calculator.html',User='David')

@app.route('/colorpicker')
def Picker():
    return render_template('colorpicker.html',User='David')

@app.route('/AWS')
def AWS():
    return render_template('index.html',User='David')

@app.route("/maps")
def Maps():
	a = requests.get(u'https://data.cityofchicago.org/api/views/tj8h-mnuv/rows.json')
	p = a.json()
	return render_template("maps.html", payload=p)
