from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validates_author_name(self, key, check_name):

        if not check_name:
            raise ValueError("name can not empty")
        

        # Check if the name already exists in the database
        existing_author = Author.query.filter_by(name=check_name).first()
        if existing_author:
            raise ValueError("This name is already taken by another author")

        return check_name
    
    @validates('phone_number')
    def validates_phone_number(self, key, check_number):
        if len(check_number) != 10:
            raise ValueError("Author phone number must be exactly ten digits")

        if not check_number.isdigit():
            raise ValueError("Author phone number must contain only digits")

        return check_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def validates_post_title(self, key, check_title):

        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]

        if not check_title:
            raise ValueError("post must have a title")
        
        for word in clickbait_words:
            if word in check_title:
                return check_title
        
        raise ValueError("Title sound clickbait-y")

    @validates('content')
    def validates_post_content(self, key, check_content):

        if len(check_content) < 250:
            raise ValueError("content must be greater then 250 chracters")
        
        return check_content

    @validates('summary')
    def validates_post_summary(self, key, check_summary):

        if len(check_summary) > 250:
            raise ValueError("summary max is 250")
        
        return check_summary

    @validates('category')
    def validates_post_category(self, key, check_category):

        if check_category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return check_category 


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
