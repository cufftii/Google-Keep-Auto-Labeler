from apis.gkeep import login, DataGetter, LabelController
from apis.openai import completion
from prompts import Prompt

def convert_to_list(response):
    return list(response.replace("new label", "").replace(":", ",").replace("\n", "").lower().split(","))

def initiate_tags():
    dataGetter = DataGetter(keep)
    
    dataGetter.retrieve_all_notes()
    notes_string = dataGetter.all_notes_as_string()
    
    response = completion(Prompt.to_initiate_tags(notes_string))
    tags = convert_to_list(response)
    for tag in tags:
        LabelController(keep).create_label(tag)
    keep.sync()
        
def label_note(note, all_labels_string):
    response = completion(Prompt.to_label_note(str(note), all_labels_string))
    response = response.lower()
    tags = response.replace(" ", "").split(",")[:2]
    print(tags)
    
    labelController = LabelController(keep)
    for tag in tags:
        labelController.put_label(note, tag)
    
def label_all_notes():
    dataGetter = DataGetter(keep)
    
    notes = dataGetter.retrieve_all_notes()
    if len(notes)==0: return False
    
    for note in notes:
        dataGetter.retrieve_all_labels()
        labels_string = dataGetter.all_labels_as_string()
        label_note(note, labels_string)
    keep.sync()
    return True
    
        
def label_new_notes():
    dataGetter = DataGetter(keep)
    
    dataGetter.retrieve_all_notes()
    old_notes, new_notes = dataGetter.check_for_old_and_new_notes()
    if len(new_notes)==0: return False
    
    for note in new_notes:
        dataGetter.retrieve_all_labels()
        labels_string = dataGetter.all_labels_as_string()
        label_note(note, labels_string)
    keep.sync()
    return True

def delete_not_useful_tags():
    dataGetter = DataGetter(keep)
    labels = dataGetter.retrieve_all_labels()
    labelControlller = LabelController(keep)
    
    for label in labels:
        notes = list(keep.find(labels=[label]))
        if len(notes)<3:
            labelControlller.delete(label.name)
    keep.sync()

def delete_all_tags():
    dataGetter = DataGetter(keep)
    labels = dataGetter.retrieve_all_labels()
    
    labelController = LabelController(keep)
    labelController.delete_all(labels)
    keep.sync()

keep = login()
label_new_notes()
delete_not_useful_tags()
label_all_notes()




