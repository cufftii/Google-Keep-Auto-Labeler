import os
from dotenv import load_dotenv
import gkeepapi

def login():
    load_dotenv()
    keep = gkeepapi.Keep()
    google_email = os.getenv('GOOGLE_EMAIL')
    google_password = os.getenv('GOOGLE_PASSWORD')
    success = keep.login(google_email, google_password)

    if(not success): 
        raise Exception("Cannot login google account")
    return keep

class Label:
    def __init__(self, label):
        self.id = label.id
        self.name = label.name
    
    def __str__(self): return self.name
    
class Note:
    def __init__(self, note, all_labels):
        self.id = note.id
        self.title = note.title
        self.text = note.text
        labels = filter(lambda label: note.labels.get(label.id) != None, all_labels)
        self.labels = set(Label(label) for label in labels)
        
    def __str__(self):
        labels_string = ""
        for label in self.labels: labels_string += label.name+", "
        labels_string = labels_string.rstrip(", ")
        return "<Note Informations>\nTitle: {}\nText:\n{}\n\nLabels: {}\n".format(self.title, self.text, labels_string)
        
class DataGetter:
    def __init__(self, keep):
        self.keep = keep
    
    def retrieve_all_labels(self):
        self.keep.sync()
        self.labels = set(self.keep.labels())
        return self.labels
    
    def all_labels_as_string(self):
        labels_string = "Existing Labels : "
        for label in self.labels:
            labels_string += label.name+", "
        labels_string = labels_string.rstrip(", ")
        return labels_string

    def notes_as_string(self, notes):
        notes_string = ""
        for note in notes:
            notes_string += "\n"+str(note)
        return notes_string
    
    def retrieve_all_notes(self):
        self.keep.sync()
        all_notes = self.keep.all()
        all_labels = self.retrieve_all_labels()
        self.notes = [Note(note, all_labels) for note in all_notes]
        return self.notes
    
    def all_notes_as_string(self):
        notes_string = "Existing Notes :\n"+self.notes_as_string(self.notes)
        return notes_string
    
    def check_for_old_and_new_notes(self):
        old_notes = []
        new_notes = []
        for note in self.notes:
            if len(note.labels) > 0:
                old_notes.append(note)
            else:
                new_notes.append(note)
        self.old_notes = old_notes
        self.new_notes = new_notes
        return old_notes, new_notes
    
    def old_notes_as_string(self):
        notes_string = "Existing Notes :\n"+self.notes_as_string(self.old_notes)
        return notes_string
    
    def new_notes_as_string(self):
        notes_string = "New Notes :\n"+self.notes_as_string(self.new_notes)
        return notes_string

class LabelController:
    def __init__(self, keep):
        self.keep = keep
        
    def create_label(self, label_name):
        if self.keep.findLabel(label_name) == None:
            label = self.keep.createLabel(label_name)
        return label
    
    def put_label(self, note, label_name):
        label = self.keep.findLabel(label_name)
        if(label==None):
            label = self.create_label(label_name)
        
        note = self.keep.get(note.id)
        if(note==None):
            raise Exception("No such existing note. It may have been removed during the process")
        
        note.labels.add(label)
        
    def delete(self, label_name):
        label = self.keep.findLabel(label_name)
        if(label != None):
            label.delete()
            self.keep.sync()
        
    def delete_all(self, labels):
        for label_obj in labels:
            label = self.keep.findLabel(label_obj.name)
            if(label != None):
                label.delete()
        self.keep.sync()
    
