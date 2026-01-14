
from flask import Blueprint,request, redirect
from flask.templating import render_template
from models import Book,Library
from extensions import db
from sqlalchemy import or_, and_, select

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')



@main.route('/book')
def list_books(data):
    
    if data['title'] is not None or data['author'] is not None:
        select_query = select(Book).where(
            or_(Book.title == data['title'], Book.author == data['author'] )
        )
        books = db.session.execute(select_query).scalars().all()
    else:
        books = Book.query.all()

    return books



def validate_add_book(data):
    if data['title'] == '':
        return 'title is empty'
    
    if data['author'] == '':
        return 'author is empty'

    if data['library_id'] == '':
        return 'library id is empty'

    if Library.query.get(data['library_id']) is None:
        return 'library id is invalid'

    return ''



@main.route('/book/add', methods=["GET","POST"])
def add_book():
    
    data = {'title':'','author':'','library_id':None}
    error = ''

    if request.method == "GET":
        return render_template('add_book.html',data=data,error=error)
    else:
        data['title'] = request.form.get("title")
        data['author']  = request.form.get("author")
        data['library_id'] = request.form.get("library_id",type=int)

        error = validate_add_book(data)

        if error == '':
            book = Book(author=data.author, title=data.title,library_id=data.library_id)
            db.session.add(book)
            db.session.commit()
            return redirect('/book')
        else:
            return render_template('add_book.html',data=data,error=error)

@main.route('/book/delete/<int:id>')
def delete_book(id): 
    data = Book.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/book')
    

@main.route('/book/update/<int:id>')
def update_book(id):
    book = Book.query.get_or_404(id)
    return render_template('update_book.html',book=book)

@main.route('/book/update/<int:id>', methods=['POST'])
def commit_update_book(id):
    book = Book.query.get_or_404(id)

    title = request.form.get("title")
    author = request.form.get("author")
    library_id = request.form.get("library_id")

    if title != '':
        book.title = title

    if author != '':
        book.author = author
    
    if library_id != '':
        book.library_id = library_id

    db.session.commit()

    return redirect('/book')



# -----------------------------

@main.route('/library')
def list_libraries():
    libraries = Library.query.all()
    return render_template('list_library.html', libraries=libraries)

@main.route('/library/add')
def add_libraries():
    return render_template('add_library.html')

@main.route('/library/add', methods=["POST"])
def save_library():
    name = request.form.get("name")

    if name != '':
        library = Library(name=name)
        db.session.add(library)
        db.session.commit()
        return redirect('/library')
    else:
        return redirect('/library')

@main.route('/library/delete/<int:id>')
def delete_library(id): 
    data = Library.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/library')
    
@main.route('/library/update/<int:id>')
def update_library(id):
    library = Library.query.get_or_404(id)
    return render_template('update_library.html',library=library)

@main.route('/library/update/<int:id>', methods=['POST'])
def commit_update_library(id):
    library = Library.query.get_or_404(id)

    name = request.form.get("name")

    if name != '':
        library.name = name

    db.session.commit()
    
    return redirect('/library')


@main.route('/library/<int:id>')
def filter_books_by_library(id):
    library = Library.query.get_or_404(id)
    return render_template('filter_books.html', library=library)





