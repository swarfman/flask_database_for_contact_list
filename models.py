from flask_sqlalchemy import SQLAlchemy
  
db = SQLAlchemy()
  
#Example model Item 
#It represents an Item in a list
#you can use any name, first letter in CAPS
  
contacts = db.Table('contacts',
    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)
        
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    groups = db.relationship('Group', secondary=contacts, lazy='subquery', backref=db.backref('contacts', lazy=True))
    
    def to_dict_simple_cat(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
        }

    
    def to_dict(self):
        temp_array = []
        for g in self.groups:
            temp_array.append(g.to_dict_simple_elephant())   
        return { 
          "id": self.id, 
          "full_name": self.full_name,
          "email": self.email,
          "address": self.address,
          "phone": self.phone,
          "groups": temp_array
        }
        

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    def to_dict_simple_elephant(self):
        return {
            "name": self.name,
            "id": self.id,
        }
    
    def to_dict(self):
        contacts = []
        for c in self.contacts:
            contacts.append(c.to_dict_simple_cat())
        return { 
          "id": self.id, 
          "name": self.name, 
          "contacts": contacts 
        }
    #use this to return return JSON serializable group dictionary
    def list_details(self):
        return{
            'id': self.id,
            'name': self.name
        }