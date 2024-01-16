from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.list import ThreeLineListItem, MDList

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class TopicApp(MDApp):
    def build(self):
        self.topics = {}
        self.theme_cls.theme_style = "Dark"  
        self.subtopic_count = 0

        return Builder.load_string(
            """
BoxLayout:
    orientation: "vertical"

    MDToolbar:
        title: "Topic App"
        elevation: 10

    MDBoxLayout:
        orientation: "vertical"
        spacing: "12dp"
        padding: "8dp"

        MDTextField:
            id: topic_input
            hint_text: "Enter a topic"
            helper_text: "Press 'Enter' to add"
            helper_text_mode: "on_focus"
            on_text_validate: app.add_topic()

        MDTextField:
            id: subtopic_count_input
            hint_text: "Enter number of subtopics"
            helper_text: "Press 'Enter' to continue"
            helper_text_mode: "on_focus"
            on_text_validate: app.set_subtopic_count()

        MDTextField:
            id: subtopic_input
            hint_text: "Enter a subtopic"
            helper_text: "Press 'Enter' to add"
            helper_text_mode: "on_focus"
            on_text_validate: app.add_subtopic()

        MDTextField:
            id: subject_input
            hint_text: "Enter a subject"
            helper_text: "Press 'Enter' to add"
            helper_text_mode: "on_focus"
            on_text_validate: app.add_subject()

        MDBoxLayout:
            spacing: "12dp"

            MDRaisedButton:
                text: "Done"
                on_press: app.done_button_pressed()

            MDFlatButton:
                text: "New"
                on_press: app.reset_inputs()

            MDRaisedButton:
                text: "Create PDF"
                on_press: app.create_pdf()
    """
        )

    def add_topic(self):
        topic = self.root.ids.topic_input.text
        if topic:
            self.current_topic = topic
            self.root.ids.subtopic_count_input.focus = True

    def set_subtopic_count(self):
        try:
            count = int(self.root.ids.subtopic_count_input.text)
            if count > 0:
                self.subtopic_count = count
                self.root.ids.subtopic_input.focus = True
        except ValueError:
            pass

    def add_subtopic(self):
        subtopic = self.root.ids.subtopic_input.text
        if subtopic:
            if self.current_topic not in self.topics:
                self.topics[self.current_topic] = {}
            self.topics[self.current_topic][subtopic] = []
            self.subject_count = 1
            self.root.ids.subject_input.focus = True

    def add_subject(self):
        subject = self.root.ids.subject_input.text
        if subject and self.current_topic in self.topics:
            subtopic = list(self.topics[self.current_topic].keys())[-1]
            self.topics[self.current_topic][subtopic].append(subject)
            self.subject_count += 1
            self.root.ids.subject_input.text = f"Subject {self.subject_count}"

    def done_button_pressed(self):
        self.reset_inputs()

    def reset_inputs(self):
        self.root.ids.topic_input.text = ""
        self.root.ids.subtopic_count_input.text = ""
        self.root.ids.subtopic_input.text = ""
        self.root.ids.subject_input.text = ""
        self.root.ids.topic_input.focus = True

    def create_pdf(self):
        # Call the create_pdf function with the collected data
        create_pdf(self.topics)

def create_pdf(topics):
    # Create a PDF document
    pdf_filename = "topic_document.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Create a list to hold the content of the PDF
    content = []

    # Add topics to the content list
    for topic, subtopics in topics.items():
        content.append([topic])
        for subtopic, subjects in subtopics.items():
            content.append(["", subtopic])
            for subject in subjects:
                content.append(["", "", subject])

    # Create a table and apply styles
    table_style = [('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                   ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]

    table = Table(content)
    table.setStyle(TableStyle(table_style))

    # Add the table to the PDF document
    doc.build([table])

    print(f"PDF created successfully: {pdf_filename}")

if __name__ == "__main__":
    TopicApp().run()
