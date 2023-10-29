from datetime import datetime
import re


def get_birthday(event_date):
    delta_years = datetime.now().year - int(event_date.split('-')[0])
    birthday0 = datetime.strptime(f"{datetime.now().year}-{event_date.split('-')[1]}-"
                                  f"{event_date.split('-')[2]}", '%Y-%m-%d')
    birthday1 = datetime.strptime(f"{datetime.now().year + 1}-{event_date.split('-')[1]}-"
                                  f"{event_date.split('-')[2]}", '%Y-%m-%d')
    if (birthday0.date() - datetime.now().date()).days > 0:
        return birthday0, delta_years
    elif (birthday0.date() - datetime.now().date()).days < 0:
        return birthday1, delta_years+1
    else:
        return None, delta_years


class Events:
    def __init__(self, event_type, filename):
        self.type = event_type
        self.filename = filename

    def __str__(self):
        events = ['']
        try:
            with (open(self.filename, 'r') as file):
                for line in file:
                    event_date = line.rstrip().split(sep='\t')[0]
                    event_text = line.rstrip().split(sep='\t')[1]
                    if self.type == 'note':
                        delta = datetime.strptime(event_date, '%Y-%m-%d %H:%M') - datetime.now()
                        event = (f'Before the event {self.type} "{event_text}" remains: '
                                 f'{delta.days} day(s), {delta.seconds // 3600} hour(s) '
                                 f'and {delta.seconds % 3600 // 60} minute(s).')
                    else:
                        birthday, delta_years = get_birthday(event_date)
                        if birthday is not None:
                            event = (f"{event_text}'s birthday is in {(birthday.date() - datetime.now().date()).days} "
                                     f"days. He (she) turns {delta_years} years old.")
                        else:
                            event = (f"{event_text}'s birthday is today. "
                                     f'He (she) turns {delta_years} years old.')
                    events.append(event)
                return "\n".join(events)
        except FileNotFoundError:
            return ''

    def print(self, event):
        event_date = event.rstrip().split(sep='\t')[0]
        event_text = event.rstrip().split(sep='\t')[1]
        if self.type == 'note':
            delta = datetime.strptime(event_date, '%Y-%m-%d %H:%M') - datetime.now()
            print(f'Before the event {self.type} "{event_text}" remained: '
                  f'{delta.days} day(s), {delta.seconds // 3600} hour(s) '
                  f'and {delta.seconds % 3600 // 60} minute(s).')
        else:
            birthday, delta_years = get_birthday(event_date)
            if birthday is not None:
                print(f'{event_text}\'s birthday is in {(birthday.date() - datetime.now().date()).days} '
                      f'days. He (she) turns {delta_years} years old.')
            else:
                print(f'{event_text}\'s birthday is today. '
                      f'He (she) turns {delta_years} years old.')

    def add(self, event_date, event_text):
        with open(self.filename, 'a') as file:
            file.write(f'{event_date}\t{event_text}\n')

    def create(self, index):
        if self.type == 'note':
            event_text = ''
            event_date = input(f"Enter date and time of note #{index} (in format «YYYY-MM-DD HH:MM»):")
        else:
            event_text = input(f"Enter the name of #{index}:")
            event_date = input(f"Enter the date of birth of #{index} (in format «YYYY-MM-DD»):")
        while True:
            if self.type == 'note' and not re.match('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', event_date):
                event_date = input("Incorrect format. Please try again (use the format «YYYY-MM-DD HH:MM»):")
            elif self.type == 'birthdate' and not re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}', event_date):
                event_date = input("Incorrect format. Please try again (use the format «YYYY-MM-DD»):")
            elif int(event_date.split(' ')[0].split('-')[1]) not in range(1, 13):
                print("Incorrect month value. The month should be in 01-12.")
                event_date = input("Please try again:")
            elif self.type == 'note' and int(event_date.split(' ')[1].split(':')[0]) not in range(0, 24):
                print("Incorrect hour value. The hour should be in 00-23.")
                event_date = input("Please try again:")
            elif self.type == 'note' and int(event_date.split(' ')[1].split(':')[1]) not in range(0, 60):
                print("Incorrect minute value. The minutes should be in 00-59.")
                event_date = input("Please try again:")
            else:
                break
        if self.type == 'note':
            event_text = input(f"Enter text of {self.type} #{index}:")
        return event_date, event_text

    def get_by_date(self, event_date):
        events = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    if self.type == 'note':
                        if event_date == line.rstrip().split(sep='\t')[0].split(sep=' ')[0]:
                            events.append(line)
                    elif self.type == 'birthdate':
                        event_month = line.rstrip().split(sep='\t')[0].split(sep='-')[1]
                        event_day = line.rstrip().split(sep='\t')[0].split(sep='-')[2]
                        if event_date.split('-')[1] == event_month and event_date.split('-')[2] == event_day:
                            events.append(line)
            return events
        except FileNotFoundError:
            return ''

    def get_by_name(self, event_text):
        events = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    if event_text in line.rstrip().split(sep='\t')[1]:
                        events.append(line)
            return events
        except FileNotFoundError:
            return ''

    def delete(self, event):
        with open(self.filename, 'r') as file:
            events = file.readlines()
            events.remove(event)
        with open(self.filename, 'w') as file:
            file.writelines(events)


print("Current date and time:")
print(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'))
notes = Events('note', 'notes.txt')
birthdates = Events('birthdate', 'birthdates.txt')
while True:
    command = input("Enter the command (add, view, delete, exit)")
    if command == "add":
        choice = input("What do you want to add (note, birthday)?")
        if choice == 'note':
            number = int(input("How many notes do you want to add?"))
            for i in range(number):
                date, text = notes.create(i+1)
                notes.add(date, text)
            print("Notes added")
        elif choice == 'birthday':
            number = int(input("How many dates of birth do you want to add? "))
            for i in range(number):
                date, text = birthdates.create(i+1)
                birthdates.add(date, text)
            print("Birthdates added")
    elif command == 'view':
        choice = input("What do you want to view (date, note, name)?")
        if choice == 'date':
            date = input("Enter date (in format «YYYY-MM-DD»):")
            notes_by_date = notes.get_by_date(date)
            birthdates_by_date = birthdates.get_by_date(date)
            print(f"Found {len(notes_by_date)} note(s) and {len(birthdates_by_date)} date(s) of birth on this date:\n")
            for note in notes_by_date:
                notes.print(note)
            for birthdate in birthdates_by_date:
                birthdates.print(birthdate)
        elif choice == 'name':
            birthdates_by_date = []
            name = input("Enter name:")
            while True:
                birthdates_by_date = birthdates.get_by_name(name)
                if len(birthdates_by_date) == 0:
                    name = input("No such person found. Try again:")
                else:
                    break
            print(f"Found {len(birthdates_by_date)} date(s) of birth on this date:\n")
            for birthdate in birthdates_by_date:
                birthdates.print(birthdate)
        elif choice == 'note':
            text = input("Enter text of note:")
            while True:
                notes_by_date = notes.get_by_name(text)
                if len(notes_by_date) == 0:
                    text = input("No such note found. Try again:")
                else:
                    break
            print(f"Found {len(notes_by_date)} note(s) that contain \"{text}\":\n")
            for note in notes_by_date:
                notes.print(note)
    elif command == 'delete':
        choice = input("What do you want to delete (date, note, name)?")
        if choice == 'date':
            date = input("Enter date (in format «YYYY-MM-DD»):")
            notes_by_date = notes.get_by_date(date)
            birthdates_by_date = birthdates.get_by_date(date)
            print(f"Found {len(notes_by_date)} note(s) and {len(birthdates_by_date)} date(s) of birth on this date:\n")
            for note in notes_by_date:
                notes.print(note)
            for birthdate in birthdates_by_date:
                birthdates.print(birthdate)
            for note in notes_by_date:
                text = note.split(sep='\t')[1].rstrip()
                answer = input(f"Are you sure you want to delete \"{text}\"?")
                if answer == "yes":
                    notes.delete(note)
                    print("Note deleted!")
                else:
                    print("Deletion canceled.")
            for birthdate in birthdates_by_date:
                name = birthdate.split(sep='\t')[1].rstrip()
                answer = input(f"Are you sure you want to delete \"{name}\"?")
                if answer == "yes":
                    birthdates.delete(birthdate)
                    print("Birthdate deleted!")
                else:
                    print("Deletion canceled.")
        elif choice == 'name':
            name = input("Enter name:")
            while True:
                birthdates_by_date = birthdates.get_by_name(name)
                if len(birthdates_by_date) == 0:
                    name = input("No such person found. Try again:")
                else:
                    break
            print(f"Found {len(birthdates_by_date)} date(s) of birth on this date:\n")
            birthdates.print(birthdates_by_date[0])
            answer = input(f"Are you sure you want to delete \"{name}\"?")
            if answer == "yes":
                birthdates.delete(birthdates_by_date[0])
                print("Birthdate deleted!")
            else:
                print("Deletion canceled.")
        elif choice == 'note':
            text = input("Enter text of note:")
            while True:
                notes_by_date = notes.get_by_name(text)
                if len(notes_by_date) == 0:
                    text = input("No such note found. Try again:")
                else:
                    break
            notes_by_date = notes.get_by_name(text)
            print(f"Found {len(notes_by_date)} note(s) that contain \"{text}\":\n")
            for note in notes_by_date:
                notes.print(note)
            answer = input(f"Are you sure you want to delete \"{text}\"?")
            if answer == "yes":
                notes.delete(notes_by_date[0])
                print("Note deleted!")
            else:
                print("Deletion canceled.")
    elif command == 'exit':
        break
    else:
        print("This command is not in the menu")
