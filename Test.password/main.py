import urwid

def has_digit(password):
    return any(character.isdigit() for character in password)

def has_letters(password):
    return any(character.isalpha() for character in password)

def is_very_long(password):
    if len(password) > 12:
        return True
    return False

def has_upper_letters(password):
    return any(character.isupper() for character in password)

def has_lower_letters(password):
    return any(not character.isupper() for character in password)

def has_symbols(password):
    return any(not character.isalnum() for character in password)

def has_not_only_symbols(password):
    return any(not has_symbols(character) for character in password)

def verification_password(edit, password):
    score = 0
    set_of_verifications = [
        has_lower_letters,
        has_upper_letters,
        has_letters,
        has_digit,
        is_very_long,
        has_not_only_symbols,
        has_symbols,
    ]
    for verification in set_of_verifications:
       if verification(password):
           score += 2
    native_password.set_text("Your password: %s" % password)
    total_score.set_text("Password rating: %s" % score)

if __name__ == '__main__':

    password = urwid.Edit('Enter password: ', mask='*')
    native_password = urwid.Text('')
    total_score = urwid.Text('')
    menu = urwid.Pile([password, native_password, total_score])
    urwid.connect_signal(password, 'change', verification_password)
    menu = urwid.Filler(menu, valign='top')
    urwid.MainLoop(menu).run()