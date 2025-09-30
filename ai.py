# this ai will summarize and structure content of notes using ollama api
import dspy
print("running...")

lm = dspy.LM('ollama_chat/gemma3:4b', api_base ='http://localhost:11434', api_key = '')

dspy.settings.configure(lm=lm)

class re_write_notes(dspy.Signature):
    """given the notes, organize them into sections with numbered headings followed by the matching content. do not add formatting characters. include all notes"""
    notes = dspy.InputField()
    new_notes: str = dspy.OutputField()


class assist_notes(dspy.Signature):
    """follow user prompt"""
    notes = dspy.InputField()
    prompt = dspy.InputField()
    new_text: str = dspy.OutputField()


def organize_notes(notes):
    notes_maker = dspy.Predict(re_write_notes)
    note_sections = notes_maker(notes=notes).new_notes
    return note_sections

def custom_prompt(notes, prompt):
    helper = dspy.Predict(assist_notes)
    note_sections = helper(notes=notes, prompt = prompt).new_text
    return note_sections