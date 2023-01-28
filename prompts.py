class Prompt:
    def to_create_tags(all_notes):
        prompt = "These are notes stored in a notepad. \
            Create four tags to classify and systematically manage the notes. \
            , regarding to a subject or a purpose of the notes. Tags must cover all of the topics in all of the notes.\
            List tags separated by commas, and don't write any other words.\
            {} Labels : ".format(all_notes)
        return prompt
    
    def to_label_note(note, all_labels, create_new=True):
        additional_text = ""
        if(create_new):
            additional_text = "If there's no tag that can represent this note, you may create a new tag."
        prompt = "Select tags to classify this note. Tags must be up to three 3!! \
            Choose from the existing tags below. Refer to previous labeling of the notes.\
            {} List only the tags separated by commas, and don't write any other words.\
            {} {} Labels : ".format(additional_text, note, all_labels)
        return prompt
    